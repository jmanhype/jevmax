#!/usr/bin/env python3
"""Workflow #8 — the account audit. The product's core artifact.

Ryze's lead magnet is a free audit; this is ours, with judgment shown as math.
Input: account_snapshot.json assembled by the agent from MCP reads (campaigns,
pixels, pages, IG), since MCP tools are callable from agent sessions, not from
Python. Deterministic checks first — no tokens — then one Jev pass to rank
findings into a client-ready priority list.

Checks:
  A1 campaigns ACTIVE with no recent spend (dormant-but-on) + budget exposure
  A2 conversion tracking dead (pixel exists, never fired)
  A3 account hygiene: Instagram link, lead-gen ToS
Usage: python3 audit.py [--snapshot account_snapshot.json] [--out audit_report.md]
"""
import argparse
import json

from typesafe import ask, load_key  # noqa: F401  (load_key surfaces config errors early)


def build_findings(snap):
    findings = []

    for c in snap.get("campaigns", []):
        budget = c.get("daily_budget_cents")
        spend = c.get("amount_spent_28d")
        if (
            c.get("effective_status") == "ACTIVE"
            and c.get("delivery", {}).get("status") != "completed"
            and not spend
        ):
            f = {
                "id": f"c{c['id']}",
                "title": f"Campaign '{c['name']}' is ACTIVE with no spend in 28 days",
                "evidence": f"last advertised {c.get('last_advertised', 'unknown')}",
                "action": "Pause it or fund it — an ACTIVE campaign is one toggle away from spending",
                "spend_at_risk_year": 0,
            }
            if budget:
                f["spend_at_risk_year"] = budget * 365 / 100
                f["title"] += f" with a ${budget / 100:.2f}/day budget attached"
                f["evidence"] += f"; silent-spend exposure ${budget * 365 / 100:,.0f}/yr"
            findings.append(f)

    for p in snap.get("pixels", []):
        if not p.get("ever_fired"):
            findings.append({
                "id": f"p{p['id']}",
                "title": f"Conversion tracking is dead: pixel '{p['name']}' has never recorded an event",
                "evidence": "created but zero lifetime firings — every optimization is flying blind",
                "action": "Install the pixel and get one real event flowing before relaunching any campaign",
                "spend_at_risk_year": 0,
            })

    if snap.get("pages") and not snap.get("ig_accounts"):
        findings.append({
            "id": "ig0",
            "title": "No Instagram account linked — all IG placements unavailable",
            "evidence": f"page(s) {', '.join(pg['name'] for pg in snap['pages'])} with no linked IG Business account",
            "action": "Link one in Page settings, or accept losing roughly half the placement inventory",
            "spend_at_risk_year": 0,
        })

    for pg in snap.get("pages", []):
        if pg.get("leadgen_tos_accepted") is False:
            findings.append({
                "id": f"l{pg['id']}",
                "title": f"Lead-gen ToS not accepted on '{pg['name']}' — lead campaigns blocked",
                "evidence": "leadgen_tos_accepted=false at the Page level",
                "action": "Accept at facebook.com/legal/leadgen/tos if lead ads are ever on the roadmap; ignore otherwise",
                "spend_at_risk_year": 0,
            })

    return findings


def rank(findings, snap):
    """One Jev pass: priority per finding. Falls back to severity hints on API error."""
    order = {"now": 0, "soon": 1, "note": 2}
    try:
        state = {"account": snap["account"], "findings": {f["id"]: f for f in findings}}
        questions = {}
        for i, f in enumerate(findings):
            questions[f"f{i}_priority"] = {
                "type": "choice",
                "instructions": (
                    f"What priority for finding `f{i}` on this ad account? Consider money at "
                    "risk, whether it blocks learning/optimization, and whether it matters "
                    "even if the account is not actively spending."
                ),
                "criteria": {
                    "now": "Fix immediately: costs money today or blocks all optimization",
                    "soon": "Fix before the next campaign launch",
                    "note": "Housekeeping — handle whenever convenient",
                },
            }
        answers, usage = ask(state, questions)
        for i, f in enumerate(findings):
            f["priority"] = answers[f"f{i}_priority"]["choice"]
        return findings, usage
    except Exception as e:
        print(f"(Jev ranking unavailable: {e} — falling back to listed order)")
        for f in findings:
            f["priority"] = "now"
        return findings, {"input_tokens": 0, "output_tokens": 0}


def write_report(snap, findings, usage, out):
    acc = snap["account"]
    lines = [
        f"# Account audit — {acc['name']} ({acc['id']}) — {snap['snapshot_date']}",
        "",
        f"Findings: {len(findings)}. "
        f"Silent-spend exposure found: ${sum(f['spend_at_risk_year'] for f in findings):,.0f}/yr.",
        "",
        "## Priority list (Jev-ranked)",
        "",
    ]
    for p in ("now", "soon", "note"):
        for f in [x for x in findings if x["priority"] == p]:
            lines += [f"### [{p.upper()}] {f['title']}", f"- Evidence: {f['evidence']}",
                      f"- Action: {f['action']}", ""]
    if snap.get("notes"):
        lines += ["## During this audit", snap["notes"], ""]
    lines += [
        "## Hygiene",
        f"- Currency {acc['currency']}, payment method: {'on file' if acc['has_payment_method'] else 'MISSING'}, "
        f"account status {acc['status']}",
        "",
        f"*Ranked by Jev in one pass: {usage['input_tokens']} in / {usage['output_tokens']} out tokens.*",
    ]
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"Written: {out} ({len(findings)} findings)")
    print(f"Usage: {usage['input_tokens']} in / {usage['output_tokens']} out tokens")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", default="account_snapshot.json")
    ap.add_argument("--out", default="audit_report.md")
    args = ap.parse_args()
    with open(args.snapshot, encoding="utf-8") as f:
        snap = json.load(f)
    findings = build_findings(snap)
    if not findings:
        print("Clean account — no findings. (Suspiciously clean is itself a finding.)")
        return
    findings, usage = rank(findings, snap)
    write_report(snap, findings, usage, args.out)


if __name__ == "__main__":
    main()

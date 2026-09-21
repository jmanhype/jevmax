#!/usr/bin/env python3
"""Workflow #2 on the MCP route — longitudinal survival via snapshot diffs.

ads_library_search is newest-first with no cursor, so one scan never reaches
the 60-day tail. This builds the tail a different way: record the live-ad ID
set after every scan day, then measure what survived.

    python3 survival.py snapshot <mcp_dump.json> [more.json...]  # after each scan
    python3 survival.py report [--tags ad_library_mcp_tagged.csv]
    python3 survival.py selftest                                 # verify the math

Snapshots live in snapshots/YYYY-MM-DD.json (one file per scan day, IDs merged
across that day's queries). "Live after 60 days" = present in the newest
snapshot among IDs seen in a baseline snapshot taken >= 60 days ago. An ad
that paused and resumed between scans still counts as alive; one that churned
is detected dead at the first scan after it happened.
"""
import argparse
import csv
import json
import os
import sys
from datetime import date, datetime, timedelta

SNAPDIR = "snapshots"


def load_snapshots(d):
    out = []
    for name in sorted(os.listdir(d)):
        if name.endswith(".json"):
            with open(os.path.join(d, name), encoding="utf-8") as f:
                out.append((datetime.strptime(name[:10], "%Y-%m-%d").date(), set(json.load(f))))
    return out


def survival_table(snaps, today, min_age=60):
    """[(baseline_date, n_baseline, n_alive, pct)] for baselines >= min_age days old."""
    if len(snaps) < 2:
        return []
    latest_ids = snaps[-1][1]
    rows = []
    for d, ids in snaps[:-1]:
        if (today - d).days >= min_age and ids:
            alive = ids & latest_ids
            rows.append((d, len(ids), len(alive), len(alive) / len(ids)))
    return rows


def load_tags(path):
    tags = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tags[row["id"]] = (row.get("hook") or "(untagged)", row.get("offer") or "(untagged)")
    return tags


def load_ads(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # Official MCP results may be an ads array or an object containing one.
    ads = data.get("ads", []) if isinstance(data, dict) else data
    if not isinstance(ads, list):
        raise ValueError(f"{path} must contain an ads array")
    return ads


def cmd_snapshot(inputs, snapdir):
    ids = set()
    for path in inputs:
        ids |= {str(ad["id"]) for ad in load_ads(path)}
    os.makedirs(snapdir, exist_ok=True)
    out = os.path.join(snapdir, f"{date.today().isoformat()}.json")
    if os.path.exists(out):
        with open(out, encoding="utf-8") as f:
            ids |= set(json.load(f))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(sorted(ids), f)
    print(f"{len(ids)} unique live IDs -> {out}")


def cmd_report(snapdir, tags_path, min_age, today):
    if not os.path.isdir(snapdir):
        sys.exit(f"No {snapdir}/ yet — run `survival.py snapshot <json>` after a scan first")
    snaps = load_snapshots(snapdir)
    if not snaps:
        sys.exit(f"{snapdir}/ is empty")
    rows = survival_table(snaps, today, min_age)
    print(f"{len(snaps)} snapshot(s), {snaps[0][0]} .. {snaps[-1][0]}; "
          f"newest has {len(snaps[-1][1])} live IDs")
    if not rows:
        age = (today - snaps[0][0]).days
        readable = snaps[0][0] + timedelta(days=min_age)
        print(f"No baseline is {min_age}+ days old yet (earliest is {age}d). "
              f"First survival number readable on {readable}.")
        return

    total_n = sum(r[1] for r in rows)
    total_alive = sum(r[2] for r in rows)
    print(f"SURVIVAL (live {min_age}+ days, baseline vs newest snapshot): "
          f"{total_alive}/{total_n} overall ({total_alive / total_n:.0%})")
    for d, n, alive, pct in rows:
        print(f"  baseline {d}  n={n:<4} alive={alive:<4} {pct:.0%}")

    if tags_path:
        tags = load_tags(tags_path)
        base_d, base_ids = next((d, ids) for d, ids in snaps[:-1] if (today - d).days >= min_age)
        latest_ids = snaps[-1][1]
        for label, idx in (("BY HOOK", 0), ("BY OFFER", 1)):
            groups = {}
            for i in base_ids:
                if i in tags:
                    groups.setdefault(tags[i][idx], []).append(i in latest_ids)
            print(f"\n{label} (tagged at baseline only):")
            for key, flags in sorted(groups.items(), key=lambda kv: -len(kv[1])):
                print(f"  {key:<16} n={len(flags):<4} {sum(flags) / len(flags):.0%}")


def cmd_selftest():
    today = date(2026, 9, 20)
    snaps = [
        (date(2026, 6, 1), {"a", "b", "c", "d"}),   # 111d old: a,c survive -> 50%
        (date(2026, 8, 10), {"a", "b", "e"}),       # 41d old: below min_age, excluded
        (date(2026, 9, 20), {"a", "c", "e", "f"}),
    ]
    rows = survival_table(snaps, today)
    assert rows == [(date(2026, 6, 1), 4, 2, 0.5)], rows
    assert survival_table([], today) == []
    assert survival_table([(today, {"x"})], today) == []
    # min_age boundary: >= 60 days qualifies. Day-of-year check (2026, non-leap):
    # Sep 20 = 263; Jul 22 = 203 -> 60d (qualifies); Jul 23 = 204 -> 59d (excluded).
    assert survival_table([(date(2026, 7, 21), {"a"}), (today, {"a"})], today)[0][2] == 1  # 61d
    assert survival_table([(date(2026, 7, 22), {"a"}), (today, {"a"})], today)[0][2] == 1  # 60d
    assert survival_table([(date(2026, 7, 23), {"a"}), (today, {"a"})], today) == []       # 59d
    print("selftest OK")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_snap = sub.add_parser("snapshot")
    p_snap.add_argument("inputs", nargs="+")
    p_snap.add_argument("--dir", default=SNAPDIR)

    p_rep = sub.add_parser("report")
    p_rep.add_argument("--dir", default=SNAPDIR)
    p_rep.add_argument("--tags", default=None)
    p_rep.add_argument("--min-age", type=int, default=60)

    sub.add_parser("selftest")
    args = ap.parse_args()

    if args.cmd == "snapshot":
        cmd_snapshot(args.inputs, args.dir)
    elif args.cmd == "report":
        cmd_report(args.dir, args.tags, args.min_age, date.today())
    else:
        cmd_selftest()


if __name__ == "__main__":
    main()

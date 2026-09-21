#!/usr/bin/env python3
"""Unified command-line interface for the local Jevmax toolkit."""
from __future__ import annotations

import argparse
import csv
import json
import py_compile
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKFLOWS = {
    "1": ("Ad Library tagging", "ad_library_scan.py"),
    "2": ("Survival snapshots", "survival.py"),
    "3": ("Brief scoring", "score_briefs.py"),
    "4": ("Buyer search-term sorting", "sort_search_terms.py"),
    "5": ("Creative fatigue", "fatigue.py"),
    "6": ("Ad/page promise match", "page_match.py"),
    "7": ("Lead scoring", "score_leads.py"),
    "8": ("Read-only account audit", "audit.py"),
    "9": ("SEO/GEO export analysis", "seo_geo.py"),
    "10": ("Bounded Ad Library sampler", "ad_library_sampler.py"),
}


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, check=True, **kwargs)


def status(json_out: bool = False) -> dict:
    def exists(name: str) -> bool:
        return (ROOT / name).exists()

    benchmark = json.loads((ROOT / "benchmark_results.json").read_text()) if exists("benchmark_results.json") else None
    snapshots = sorted((ROOT / "snapshots").glob("*.json")) if (ROOT / "snapshots").exists() else []
    result = {
        "root": str(ROOT),
        "python": sys.version.split()[0],
        "workflows": [
            {"id": int(k), "name": v[0], "script": v[1], "exists": exists(v[1])}
            for k, v in WORKFLOWS.items()
        ],
        "benchmark": None if not benchmark else {
            "passed": benchmark.get("total_passed"),
            "cases": benchmark.get("total_cases"),
            "mode": benchmark.get("mode"),
        },
        "artifacts": {
            name: exists(name)
            for name in (
                "dashboard.html", "benchmark_results.json", "seo_geo_report.json",
                "citation_report.json", "samples/local_regression_combined.json",
                "icp_airpods.md", "google_ads_search_terms_template.csv"
            )
        },
        "snapshots": [{"date": p.stem, "path": str(p)} for p in snapshots],
        "missing_real_inputs": [
            "Google Ads search-terms CSV",
            "Search Console export for production domain",
            "AI-citation export for production domain",
            "60-day later Ad Library snapshot",
        ],
        "live_ad_changes": "disabled in status/selftest commands",
    }
    if json_out:
        print(json.dumps(result, indent=2))
    else:
        print("Jevmax local toolkit")
        print(f"Root: {result['root']}")
        print(f"Python: {result['python']}")
        print("Workflows:")
        for workflow in result["workflows"]:
            print(f"  {workflow['id']:>2}. {workflow['name']}: {workflow['script']}")
        if benchmark:
            print(f"Benchmark: {benchmark.get('total_passed')}/{benchmark.get('total_cases')} passed ({benchmark.get('mode')})")
        print("Missing real inputs:")
        for item in result["missing_real_inputs"]:
            print(f"  - {item}")
    return result


def selftest() -> int:
    errors = []
    commands = [
        ("compile", [sys.executable, "-c", "import py_compile,glob; [py_compile.compile(f,doraise=True) for f in glob.glob('*.py')]"]),
        ("benchmark", [sys.executable, "benchmark.py", "--min-pass-rate", "0.99"]),
        ("survival", [sys.executable, "survival.py", "selftest"]),
        ("sampler-plan", [sys.executable, "ad_library_sampler.py", "plan", "--plan", "ad_library_sample_plan.json", "--out", "samples/plan_manifest.json"]),
        ("sampler-combine", [sys.executable, "ad_library_sampler.py", "combine", "ad_library_mcp_raw.json", "ad_library_mcp_raw_deep.json", "ad_library_mcp_comfrt.json", "--plan", "ad_library_sample_plan.json", "--out", "samples/local_regression_combined.json"]),
        ("sampler-diff", [sys.executable, "ad_library_sampler.py", "diff", "ad_library_mcp_raw.json", "samples/local_regression_combined.json", "--out", "samples/local_regression_diff.json"]),
        ("sampler-report", [sys.executable, "ad_library_sampler.py", "report", "samples/local_regression_combined.json", "--tags", "ad_library_mcp_tagged.csv", "--out", "samples/local_regression_report.json"]),
        ("seo", [sys.executable, "seo_geo.py", "search-console", "benchmarks/search_console_sample.csv", "--own-domain", "example.com", "--out", "seo_geo_report.json"]),
        ("citations", [sys.executable, "seo_geo.py", "citations", "benchmarks/citation_sample.csv", "--own-domain", "example.com", "--out", "citation_report.json"]),
        ("dashboard", [sys.executable, "dashboard.py", "--out", "dashboard.html"]),
    ]
    for name, cmd in commands:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        print(f"{name}: {'PASS' if proc.returncode == 0 else 'FAIL'}")
        if proc.returncode:
            errors.append({"name": name, "stderr": proc.stderr, "stdout": proc.stdout})
            print(proc.stdout)
            print(proc.stderr, file=sys.stderr)
    if errors:
        (ROOT / "selftest_failures.json").write_text(json.dumps(errors, indent=2) + "\n")
        return 1
    fail_path = ROOT / "selftest_failures.json"
    if fail_path.exists():
        fail_path.unlink()
    summary = {
        "status": "PASS",
        "commands": [x[0] for x in commands],
        "live_ad_changes": False,
        "api_calls": False,
    }
    (ROOT / "selftest_results.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").add_argument("--json", action="store_true")
    sub.add_parser("selftest")
    sub.add_parser("benchmark")
    dash = sub.add_parser("dashboard")
    dash.add_argument("--out", default="dashboard.html")
    wf = sub.add_parser("workflow")
    wf.add_argument("id", choices=sorted(WORKFLOWS, key=int))
    wf.add_argument("args", nargs=argparse.REMAINDER)
    args = ap.parse_args()

    if args.cmd == "status":
        status(getattr(args, "json", False))
        return 0
    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "benchmark":
        run([sys.executable, "benchmark.py"])
        return 0
    if args.cmd == "dashboard":
        run([sys.executable, "dashboard.py", "--out", args.out])
        return 0
    script = WORKFLOWS[args.id][1]
    run([sys.executable, script, *args.args])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

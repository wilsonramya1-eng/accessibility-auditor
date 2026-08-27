from __future__ import annotations

import argparse
from pathlib import Path

import requests

from .checks import audit_html
from .report import html_report, json_report, write_report


def load_source(source: str) -> str:
    if source.startswith(("http://", "https://")):
        response = requests.get(source, timeout=15, headers={"User-Agent": "AccessibilityAuditor/1.0"})
        response.raise_for_status()
        return response.text
    return Path(source).read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a URL or HTML file for common accessibility issues.")
    parser.add_argument("source")
    parser.add_argument("--format", choices=["json", "html"], default="html")
    parser.add_argument("--output", default="accessibility-report.html")
    parser.add_argument("--fail-on-high", action="store_true")
    args = parser.parse_args()
    findings = audit_html(load_source(args.source))
    content = json_report(findings) if args.format == "json" else html_report(findings, args.source)
    write_report(args.output, content)
    print(f"Wrote {len(findings)} finding(s) to {args.output}")
    if args.fail_on_high and any(item.severity == "high" for item in findings):
        raise SystemExit(2)


if __name__ == "__main__":
    main()


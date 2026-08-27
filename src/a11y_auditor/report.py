from __future__ import annotations

import html
import json
from pathlib import Path

from .checks import Finding


def json_report(findings: list[Finding]) -> str:
    return json.dumps({"summary": summary(findings), "findings": [item.to_dict() for item in findings]}, indent=2)


def summary(findings: list[Finding]) -> dict[str, int]:
    return {severity: sum(item.severity == severity for item in findings) for severity in ("high", "medium", "low")}


def html_report(findings: list[Finding], source: str) -> str:
    cards = "".join(
        f"<article class='finding {item.severity}'><h2>{html.escape(item.message)}</h2>"
        f"<p><strong>WCAG {item.wcag}</strong> · {item.severity.upper()} · <code>{html.escape(item.selector)}</code></p>"
        f"<p>{html.escape(item.fix)}</p><pre><code>{html.escape(item.example)}</code></pre></article>"
        for item in findings
    ) or "<p class='pass'>No issues were detected by these automated checks.</p>"
    counts = summary(findings)
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'>
<title>Accessibility audit report</title><style>
body{{font:16px/1.5 system-ui;max-width:900px;margin:40px auto;padding:0 20px;color:#17202a}}header{{border-bottom:3px solid #0b7285}}
.finding{{margin:20px 0;padding:18px;border-left:6px solid #d97706;background:#f8f9fa}}.finding.high{{border-color:#c92a2a}}code{{overflow-wrap:anywhere}}pre{{white-space:pre-wrap;background:#212529;color:#f8f9fa;padding:12px}}.pass{{padding:20px;background:#d3f9d8}}
</style></head><body><header><h1>Accessibility audit</h1><p>{html.escape(source)}</p><p>{counts['high']} high · {counts['medium']} medium · {counts['low']} low</p></header>{cards}</body></html>"""


def write_report(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")


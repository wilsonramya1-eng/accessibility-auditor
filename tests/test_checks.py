from a11y_auditor.checks import audit_html
from a11y_auditor.report import html_report, json_report


BROKEN = """<!doctype html><html><head></head><body>
<h1>Dashboard</h1><h3>Revenue</h3>
<img src='chart.png'><input id='email'><a href='/help'></a><button> </button>
</body></html>"""


def test_detects_common_accessibility_failures():
    rules = {finding.rule for finding in audit_html(BROKEN)}
    assert {"document-language", "page-title", "image-alt", "form-label", "empty-link", "empty-button", "heading-order"} <= rules


def test_accessible_sample_has_no_findings():
    good = """<!doctype html><html lang='en'><head><title>Contact</title></head><body>
    <h1>Contact</h1><img src='logo.png' alt=''><label for='email'>Email</label><input id='email'>
    <a href='/help'>Help</a><button aria-label='Close'>×</button></body></html>"""
    assert audit_html(good) == []


def test_reports_escape_user_content():
    findings = audit_html(BROKEN)
    assert '"summary"' in json_report(findings)
    assert "Accessibility audit" in html_report(findings, "<unsafe>")
    assert "&lt;unsafe&gt;" in html_report(findings, "<unsafe>")


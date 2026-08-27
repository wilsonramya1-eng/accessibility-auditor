from __future__ import annotations

from dataclasses import asdict, dataclass

from bs4 import BeautifulSoup, Tag


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    message: str
    selector: str
    wcag: str
    fix: str
    example: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def selector(tag: Tag) -> str:
    if tag.get("id"):
        return f"{tag.name}#{tag['id']}"
    classes = tag.get("class", [])
    return tag.name + ("." + ".".join(classes[:2]) if classes else "")


def audit_html(html: str) -> list[Finding]:
    soup = BeautifulSoup(html, "html.parser")
    findings: list[Finding] = []
    root = soup.find("html")
    if not root or not root.get("lang"):
        findings.append(Finding("document-language", "high", "The page language is not declared.", "html", "3.1.1", "Add a lang attribute so screen readers use the correct pronunciation rules.", '<html lang="en">'))
    if not soup.title or not soup.title.get_text(strip=True):
        findings.append(Finding("page-title", "high", "The page has no descriptive title.", "head", "2.4.2", "Add a concise title that identifies the page or task.", "<title>Account settings</title>"))
    for image in soup.find_all("img"):
        if image.get("alt") is None:
            findings.append(Finding("image-alt", "high", "An image has no alternative text.", selector(image), "1.1.1", "Describe informative images. Use an empty alt value only for decorative images.", '<img src="chart.png" alt="Sales increased 18% in Q2">'))
    for field in soup.find_all(["input", "select", "textarea"]):
        if field.get("type") == "hidden":
            continue
        field_id = field.get("id")
        has_label = bool(field_id and soup.find("label", attrs={"for": field_id}))
        has_name = bool(field.get("aria-label") or field.get("aria-labelledby"))
        if not has_label and not has_name:
            findings.append(Finding("form-label", "high", "A form control has no accessible name.", selector(field), "3.3.2", "Connect a visible label with for/id, or provide an appropriate ARIA label.", '<label for="email">Email</label><input id="email">'))
    for anchor in soup.find_all("a"):
        if not anchor.get_text(" ", strip=True) and not anchor.get("aria-label"):
            findings.append(Finding("empty-link", "high", "A link has no accessible name.", selector(anchor), "2.4.4", "Add meaningful link text or an aria-label that describes its destination.", '<a href="/reports">View reports</a>'))
    headings = [int(tag.name[1]) for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
    for previous, current in zip(headings, headings[1:]):
        if current > previous + 1:
            findings.append(Finding("heading-order", "medium", f"Heading level jumps from h{previous} to h{current}.", f"h{current}", "1.3.1", "Use heading levels to represent hierarchy without skipping levels.", f"<h{previous + 1}>Section title</h{previous + 1}>"))
            break
    for button in soup.find_all("button"):
        if not button.get_text(" ", strip=True) and not button.get("aria-label"):
            findings.append(Finding("empty-button", "high", "A button has no accessible name.", selector(button), "4.1.2", "Give icon-only buttons an aria-label that describes the action.", '<button aria-label="Close dialog">×</button>'))
    return findings


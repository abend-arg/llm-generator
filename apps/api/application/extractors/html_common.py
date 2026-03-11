import logging
from dataclasses import dataclass
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup, Comment, Declaration, ProcessingInstruction

from domain import FileSection, HtmlPolicies, LinkItem

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class TextParagraph:
    text: str
    has_heading: bool

def extract_title(soup: BeautifulSoup) -> str | None:
    if soup.title and soup.title.string:
        raw_title = soup.title.string.strip()
        if raw_title:
            return raw_title
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)
    return None


def extract_summary_and_info(
    soup: BeautifulSoup, policies: HtmlPolicies
) -> tuple[str | None, str | None]:
    paragraphs = collect_candidates(soup, policies)
    for paragraph in sorted(paragraphs, key=lambda p:len(p.text), reverse=True):
        _LOGGER.info("candidate_len=%s has_title=%s candidate=%s", len(paragraph.text), "Yes" if paragraph.has_heading else "No", paragraph.text)
    summary_candidates = [p.text for p in paragraphs if p.has_heading][:3]
    summary = policies.select_summary(summary_candidates)
    info_candidates = [p.text for p in paragraphs if p.has_heading] + [
        p.text for p in paragraphs if not p.has_heading
    ]
    info = policies.select_info(info_candidates, summary)
    _LOGGER.info("SUMMARYL: %s /n/n/n/n/nINFO: %s", summary, info)
    return summary, info


def extract_useful_links(
    soup: BeautifulSoup, base_url: str, max_items: int, policies: HtmlPolicies
) -> list[FileSection]:
    base = urlsplit(base_url)
    if not base.scheme or not base.netloc:
        return []

    raw_items: list[tuple[str, str]] = []
    seen: set[str] = set()

    for a in soup.find_all("a", href=True):
        href_val = a.get("href")
        href = href_val if isinstance(href_val, str) else ""
        href = href.strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        absolute = urljoin(base_url, href)
        if not policies.is_useful_link(absolute, base.netloc):
            continue
        text = a.get_text(" ", strip=True)
        if not text:
            continue
        if absolute in seen:
            continue
        seen.add(absolute)
        raw_items.append((text, absolute))
        if len(raw_items) >= max_items * 3:
            break

    if not raw_items:
        return []

    ranked = policies.select_useful_links(raw_items, max_items)
    items = [LinkItem(name=name, url=link) for name, link in ranked]
    return [FileSection(title="Useful Links", items=items)]


def collect_candidates(soup: BeautifulSoup, policies: HtmlPolicies) -> list[TextParagraph]:
    candidates: list[TextParagraph] = []
    seen: set[str] = set()
    containers = soup.find_all(["main", "article", "section", "div"])
    for tag in containers:
        if is_rejected_tree(tag, policies):
            continue
        has_heading = has_hs(tag) or has_rich_text(tag)
        nodes = tag.find_all(["p", "ul", "span", "div"], recursive=False)
        if not nodes:
            continue
        text = "\n".join(
            _text_without_headings(n)
            for n in nodes
            if not is_rejected_tree(n, policies)
        ).strip()
        if text and not policies.is_rejected_text(text):
            normalized = " ".join(text.lower().split())
            if normalized in seen:
                continue
            seen.add(normalized)
            candidates.append(TextParagraph(text=text, has_heading=has_heading))

    return candidates


def _text_without_headings(tag) -> str:
    parts: list[str] = []
    for node in tag.find_all(string=True):
        if node.find_parent(["script", "style", "noscript"]) is not None:
            continue
        if node.find_parent(["h1", "h2", "h3"]) is not None:
            continue
        if isinstance(node, (Comment, Declaration, ProcessingInstruction)):
            continue
        parent = node.parent
        if parent:
            classes = parent.get("class") or []
            if any("img" in cls or "image" in cls or "icon" in cls for cls in classes):
                continue
        text = node.strip()
        if text and len(text) >= 25:
            parts.append(text)
    return "\n".join(parts)


def is_rejected_node(tag, policies: HtmlPolicies) -> bool:
    classes = tag.get("class") or []
    tag_id = tag.get("id") or ""
    return policies.is_rejected_node(classes, tag_id)


def is_rejected_tree(tag, policies: HtmlPolicies) -> bool:
    current = tag
    while current:
        if is_rejected_node(current, policies):
            return True
        current = current.parent
    return False


def has_hs(tag) -> bool:
    if tag.find(["h1", "h2", "h3"], recursive=False) is not None:
        return True
    return _has_heading_within_depth(tag, max_depth=3)


def has_rich_text(tag) -> bool:
    if tag.find(attrs={"data-testid": "richTextElement"}) is not None:
        return True
    return tag.find(class_=lambda cls: isinstance(cls, str) and "rich-text" in cls) is not None


def _has_heading_within_depth(tag, max_depth: int) -> bool:
    for heading in tag.find_all(["h1", "h2", "h3"]):
        depth = 0
        current = heading.parent
        while current is not None and current is not tag and depth < max_depth:
            current = current.parent
            depth += 1
        if current is tag:
            return True
    return False

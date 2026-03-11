from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup

from domain import FileSection, HtmlPolicies, LinkItem


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
    candidates = collect_candidates(soup, policies)
    summary = policies.select_summary(candidates)
    info = policies.select_info(candidates, summary)
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


def collect_candidates(soup: BeautifulSoup, policies: HtmlPolicies) -> list[str]:
    candidates: list[str] = []
    containers = soup.find_all(["main", "article", "section", "div"])
    for tag in containers:
        if is_rejected_tree(tag, policies) or not has_hs(tag):
            continue
        nodes = tag.find_all(["p", "ul", "span", "div"], recursive=False)
        if not nodes:
            continue
        text = "\n".join(
            _text_without_headings(n)
            for n in nodes
            if not is_rejected_tree(n, policies)
        ).strip()
        if text:
            candidates.append(text)

    if not candidates:
        for n in soup.find_all(["p", "li", "span", "div"]):
            if is_rejected_tree(n, policies):
                continue
            text = _text_without_headings(n)
            if text:
                candidates.append(text)

    return candidates


def _text_without_headings(tag) -> str:
    parts: list[str] = []
    for node in tag.find_all(string=True):
        if node.find_parent(["h1", "h2", "h3"]) is not None:
            continue
        text = node.strip()
        if text:
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
    for child in tag.find_all(recursive=False):
        if child.name in {"div", "header"} and child.find(
            ["h1", "h2", "h3"], recursive=False
        ):
            return True
    return False

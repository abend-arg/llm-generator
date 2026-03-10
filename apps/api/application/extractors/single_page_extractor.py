import httpx
from bs4 import BeautifulSoup

from domain import ExtractedContent, ExtractionStrategy, HtmlPolicies

from .contracts import CouldNotExtract
from .html_common import extract_summary_and_info, extract_title, extract_useful_links


class SinglePageExtractor:
    _POLICIES = HtmlPolicies.default()
    _USER_AGENT = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
    )

    def extract(self, url: str) -> ExtractedContent:
        if not url:
            raise CouldNotExtract("missing url")

        response = self._fetch(url)
        if response is None:
            raise CouldNotExtract("html fetch failed")

        soup = BeautifulSoup(response.text, "html.parser")
        title = extract_title(soup)
        summary, info = extract_summary_and_info(soup, self._POLICIES)
        sections = extract_useful_links(soup, url, max_items=12, policies=self._POLICIES)

        links_count = sum(len(section.items) for section in sections)
        if not self._POLICIES.is_sufficient(summary, info, links_count):
            raise CouldNotExtract("html extraction not sufficient")

        if not any([title, summary, info, sections]):
            raise CouldNotExtract("html extraction produced no data")

        return ExtractedContent(
            source_url=url,
            extraction_strategy=ExtractionStrategy.HTML,
            title=title,
            summary=summary,
            info=info,
            sections=sections,
        )

    def _fetch(self, url: str) -> httpx.Response | None:
        try:
            response = httpx.get(
                url,
                timeout=5.0,
                follow_redirects=True,
                headers={"User-Agent": self._USER_AGENT},
            )
        except httpx.RequestError:
            return None
        if response.status_code != 200:
            return None
        return response

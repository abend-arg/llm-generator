from fastapi import Depends

from .contracts import ExtractorProtocol
from .crawler_extractor import CrawlerExtractor
from .default_title_extractor import DefaultTitleExtractor
from .single_page_extractor import SinglePageExtractor
from .llms_txt_extractor import LlmsTxtExtractor


def get_extractors(
    llms: LlmsTxtExtractor = Depends(LlmsTxtExtractor),
    html: SinglePageExtractor = Depends(SinglePageExtractor),
    crawler: CrawlerExtractor = Depends(CrawlerExtractor),
    default_title: DefaultTitleExtractor = Depends(DefaultTitleExtractor),
) -> list[ExtractorProtocol]:
    return [llms, html, crawler, default_title]

from .models import ExtractionStrategy

EXTRACTOR_ORDER: list[ExtractionStrategy] = [
    ExtractionStrategy.LLMS_TXT,
    ExtractionStrategy.HTML,
    ExtractionStrategy.CRAWLER,
    ExtractionStrategy.DEFAULT,
]

from domain import ExtractedContent


class LlmsTxtRenderer:
    def render(self, data: ExtractedContent) -> tuple[str, str]:
        _ = data
        return "llms.txt", ""

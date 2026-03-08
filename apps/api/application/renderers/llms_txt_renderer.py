from domain import ExtractedContent


class LlmsTxtRenderer:
    def render(self, data: ExtractedContent) -> tuple[str, str]:
        lines: list[str] = []

        title = data.title or "Untitled"
        lines.append(f"# {title}")

        if data.summary:
            lines.append("")
            lines.append(f"> {data.summary}")

        for note in data.notes:
            lines.append("")
            lines.append(note)

        for section in data.sections:
            lines.append("")
            lines.append(f"## {section.title}")
            for item in section.items:
                if item.notes:
                    lines.append(f"- [{item.name}]({item.url}): {item.notes}")
                else:
                    lines.append(f"- [{item.name}]({item.url})")

        content = "\n".join(lines).strip() + "\n"
        return "llms.txt", content

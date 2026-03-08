from dataclasses import dataclass
from urllib.parse import urlsplit


@dataclass(frozen=True, slots=True)
class HtmlPolicies:
    reject_keywords: set[str]
    reject_link_keywords: set[str]
    min_summary_len: int
    min_info_len: int

    @classmethod
    def default(cls) -> "HtmlPolicies":
        return cls(
            reject_keywords={
                "testimonial",
                "testimonials",
                "review",
                "reviews",
                "quote",
                "quotes",
                "social-proof",
                "case-study",
                "customer",
            },
            reject_link_keywords={
                "/privacy",
                "/terms",
                "/login",
                "/signup",
                "/sign-up",
                "/sign-in",
                "/signin",
                "/register",
            },
            min_summary_len=100,
            min_info_len=80,
        )

    def is_rejected_node(self, classes: list[str], node_id: str) -> bool:
        haystack = " ".join(classes + [node_id]).lower()
        return any(word in haystack for word in self.reject_keywords)

    def is_useful_link(self, absolute_url: str, base_netloc: str) -> bool:
        parts = urlsplit(absolute_url)
        if parts.netloc != base_netloc:
            return False
        if any(keyword in parts.path for keyword in self.reject_link_keywords):
            return False
        return True

    def select_summary(self, candidates: list[str]) -> str | None:
        if not candidates:
            return None
        best = max(candidates, key=len)
        if len(best) < self.min_summary_len:
            return None
        return best

    def select_info(self, candidates: list[str], summary: str | None) -> str | None:
        if not candidates:
            return None
        if not summary:
            return None
        info_candidates = [
            c for c in candidates if c != summary and len(c) >= self.min_info_len
        ]
        if not info_candidates:
            return None
        return "\n\n".join(info_candidates)

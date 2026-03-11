from dataclasses import dataclass
from urllib.parse import urlsplit


@dataclass(frozen=True, slots=True)
class HtmlPolicies:
    reject_keywords: set[str]
    reject_link_keywords: set[str]
    min_summary_len: int
    max_summary_len: int
    min_info_len: int
    min_links: int
    link_rank_keywords: dict[str, int]

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
            max_summary_len=600,
            min_info_len=80,
            min_links=3,
            link_rank_keywords={
                "about": 5,
                "company": 4,
                "documentation": 8,
                "docs": 7,
                "api": 6,
                "faq": 7,
                "help": 5,
                "support": 5,
                "pricing": 5,
                "product": 4,
                "features": 4,
                "contact": 3,
                "blog": 2,
                "changelog": 2,
                "status": 2,
                "security": -3,
                "privacy": -3,
                "legal": -3,
                "terms": -2,
            },
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

    def link_rank(self, text: str, url: str) -> int:
        haystack = f"{text} {url}".lower()
        score = 0
        for keyword, weight in self.link_rank_keywords.items():
            if keyword in haystack:
                score += weight
        return score

    def select_useful_links(
        self, items: list[tuple[str, str]], max_items: int
    ) -> list[tuple[str, str]]:
        ranked = sorted(
            items,
            key=lambda item: (self.link_rank(item[0], item[1]), len(item[0])),
            reverse=True,
        )
        return ranked[:max_items]

    def select_summary(self, candidates: list[str]) -> str | None:
        if not candidates:
            return None
        filtered = [c for c in candidates if len(c) <= self.max_summary_len]
        if not filtered:
            return None
        best = max(filtered, key=len)
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

    def is_sufficient(
        self, summary: str | None, info: str | None, links_count: int
    ) -> bool:
        if not summary or len(summary) < self.min_summary_len:
            return False
        if not info or len(info) < self.min_info_len:
            return False
        return links_count >= self.min_links

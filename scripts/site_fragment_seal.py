from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "index.html", *sorted((ROOT / "modules").glob("*.html"))]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: set[str] = set()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k: v for k, v in attrs}
        node_id = data.get("id")
        node_name = data.get("name")
        if node_id:
            self.anchors.add(node_id)
        if node_name:
            self.anchors.add(node_name)
        if tag == "a" and data.get("href"):
            self.hrefs.append(data["href"] or "")


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def main() -> None:
    page_set = {p.resolve() for p in PAGES}
    parsed = {p.resolve(): parse_page(p) for p in PAGES}
    failures: list[str] = []
    checked_files = 0
    checked_fragments = 0

    for page in PAGES:
        source = page.resolve()
        for href in parsed[source].hrefs:
            parts = urlsplit(href)
            if parts.scheme or parts.netloc or href.startswith(("mailto:", "javascript:", "data:")):
                continue

            path_part = unquote(parts.path)
            fragment = unquote(parts.fragment)
            if path_part:
                target = (page.parent / path_part).resolve()
                if target.suffix.lower() != ".html":
                    continue
                checked_files += 1
                if target not in page_set or not target.exists():
                    failures.append(f"{page.relative_to(ROOT)}: missing HTML target {href}")
                    continue
            else:
                target = source

            if fragment:
                checked_fragments += 1
                target_parser = parsed.get(target)
                if target_parser is None:
                    failures.append(f"{page.relative_to(ROOT)}: fragment target is not a scanned HTML page: {href}")
                    continue
                if fragment not in target_parser.anchors:
                    failures.append(
                        f"{page.relative_to(ROOT)}: missing fragment #{fragment} in "
                        f"{Path(target).relative_to(ROOT)} (href={href})"
                    )

    if failures:
        print("SITE FRAGMENT SEAL FAIL")
        for item in failures:
            print(" -", item)
        raise SystemExit(f"{len(failures)} local HTML/fragment link failures")

    print(
        f"SITE FRAGMENT SEAL PASS: {len(PAGES)} pages scanned; "
        f"{checked_files} local HTML links and {checked_fragments} fragments resolved."
    )


if __name__ == "__main__":
    main()

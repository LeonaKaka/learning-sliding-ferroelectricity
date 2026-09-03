from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "index.html", *sorted((ROOT / "modules").glob("*.html"))]
OUT = ROOT / "search-index.json"

SKIP_TAGS = {"script", "style", "pre", "code", "kbd", "samp", "math"}
SKIP_CLASSES = {"source-text", "eq"}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def runtime_slug(text: str) -> str:
    value = clean(text).lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value).strip("-")[:48]
    return value or "section"


class IdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.add(data["id"] or "")


class SearchParser(HTMLParser):
    def __init__(self, existing_ids: set[str]) -> None:
        super().__init__(convert_charrefs=True)
        self.existing_ids = set(existing_ids)
        self.generated_ids: set[str] = set()
        self.page_title = ""
        self.entries: list[dict[str, str]] = []
        self.inside_main = 0
        self.skip_depth = 0
        self.stack: list[tuple[str, bool, bool]] = []
        self.capture_heading: str | None = None
        self.heading_parts: list[str] = []
        self.pending_h2_id: str | None = None
        self.current_heading = "导读"
        self.current_anchor = ""
        self.current_text: list[str] = []

    def _finalize(self) -> None:
        text = clean(" ".join(self.current_text))
        if len(text) >= 24:
            self.entries.append({
                "heading": self.current_heading,
                "anchor": self.current_anchor,
                "text": text[:1600],
            })
        self.current_text = []

    def _allocate_h2_id(self, raw_id: str | None, heading: str) -> str:
        if raw_id:
            return raw_id
        base = runtime_slug(heading)
        candidate = base
        n = 2
        occupied = self.existing_ids | self.generated_ids
        while candidate in occupied:
            candidate = f"{base}-{n}"
            n += 1
        self.generated_ids.add(candidate)
        return candidate

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        classes = set((data.get("class") or "").split())
        enters_main = tag == "main"
        if enters_main:
            self.inside_main += 1

        skip_here = tag in SKIP_TAGS or bool(classes & SKIP_CLASSES)
        if skip_here:
            self.skip_depth += 1
        self.stack.append((tag, enters_main, skip_here))

        if not self.inside_main or self.skip_depth:
            return
        if tag == "h1":
            self.capture_heading = "h1"
            self.heading_parts = []
        elif tag == "h2":
            self._finalize()
            self.capture_heading = "h2"
            self.heading_parts = []
            self.pending_h2_id = data.get("id")

    def handle_endtag(self, tag: str) -> None:
        if self.inside_main and not self.skip_depth and self.capture_heading == tag:
            heading = clean(" ".join(self.heading_parts))
            if tag == "h1":
                if heading:
                    self.page_title = heading
            elif tag == "h2":
                self.current_heading = heading or "未命名分节"
                self.current_anchor = self._allocate_h2_id(self.pending_h2_id, self.current_heading)
                self.pending_h2_id = None
            self.capture_heading = None
            self.heading_parts = []

        # Pop through the matching tag so malformed-but-browser-tolerated HTML
        # cannot leave the parser permanently inside a skipped region.
        while self.stack:
            open_tag, entered_main, skipped = self.stack.pop()
            if skipped:
                self.skip_depth = max(0, self.skip_depth - 1)
            if entered_main:
                self.inside_main = max(0, self.inside_main - 1)
            if open_tag == tag:
                break

    def handle_data(self, data: str) -> None:
        if not self.inside_main or self.skip_depth:
            return
        text = clean(data)
        if not text:
            return
        if self.capture_heading:
            self.heading_parts.append(text)
        else:
            self.current_text.append(text)

    def finish(self) -> None:
        self._finalize()


def parse_page(path: Path) -> tuple[str, list[dict[str, str]]]:
    raw = path.read_text(encoding="utf-8")
    ids = IdParser()
    ids.feed(raw)
    parser = SearchParser(ids.ids)
    parser.feed(raw)
    parser.finish()
    title = parser.page_title or path.stem
    return title, parser.entries


def main() -> None:
    rows: list[dict[str, str]] = []
    page_counts: dict[str, int] = {}
    for page in PAGES:
        title, entries = parse_page(page)
        rel = page.relative_to(ROOT).as_posix()
        page_counts[rel] = len(entries)
        for entry in entries:
            anchor = entry.pop("anchor")
            href = rel + (f"#{anchor}" if anchor else "")
            rows.append({"page": title, "href": href, **entry})

    if len(PAGES) < 20 or len(rows) < 70:
        raise RuntimeError(f"search index unexpectedly small: {len(PAGES)} pages / {len(rows)} sections")
    if any(count == 0 for count in page_counts.values()):
        empty = [name for name, count in page_counts.items() if count == 0]
        raise RuntimeError(f"pages produced no searchable teaching text: {empty}")

    payload = {
        "version": 1,
        "pages": len(PAGES),
        "sections": len(rows),
        "entries": rows,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"SEARCH INDEX PASS: {len(PAGES)} pages / {len(rows)} searchable sections -> {OUT.name}")


if __name__ == "__main__":
    main()

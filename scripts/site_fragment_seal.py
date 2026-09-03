from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "index.html", *sorted((ROOT / "modules").glob("*.html"))]
TERMS = ROOT / "terms.js"
NAV = ROOT / "site-nav.js"
NAV_CSS = ROOT / "site-nav.css"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: set[str] = set()
        self.hrefs: list[str] = []
        self.script_srcs: list[str] = []

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
        if tag == "script" and data.get("src"):
            self.script_srcs.append(data["src"] or "")


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def script_basename(src: str) -> str:
    return Path(urlsplit(src).path).name


def main() -> None:
    page_set = {p.resolve() for p in PAGES}
    parsed = {p.resolve(): parse_page(p) for p in PAGES}
    failures: list[str] = []
    checked_files = 0
    checked_fragments = 0
    checked_runtime_pages = 0

    terms_raw = TERMS.read_text(encoding="utf-8")
    nav_raw = NAV.read_text(encoding="utf-8")
    nav_css = NAV_CSS.read_text(encoding="utf-8")
    runtime_locked = (
        ("terms.js", "if (document.querySelector('script[data-site-nav]')) return;"),
        ("terms.js", "js.dataset.siteNav = '1'"),
        ("terms.js", "js.src = `${base}site-nav.js`"),
        ("terms.js", "css.href = `${base}site-nav.css`"),
        ("site-nav.js", "if(document.documentElement.dataset.siteNavInitialized==='1') return;"),
        ("site-nav.js", "document.documentElement.dataset.siteNavInitialized='1';"),
    )
    for owner, marker in runtime_locked:
        haystack = terms_raw if owner == "terms.js" else nav_raw
        if marker not in haystack:
            failures.append(f"{owner}: navigation runtime guard/injection marker drifted: {marker}")

    css_locked = (
        ".mobile-toc{display:none}",
        "@media(max-width:760px){.mobile-toc{display:block}",
        "main h2[id]{scroll-margin-top:116px}",
        "table{display:block;max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch}",
        ".eq,pre{max-width:100%;overflow-x:auto}",
    )
    for marker in css_locked:
        if marker not in nav_css:
            failures.append(f"site-nav.css: mobile reading guard drifted: {marker}")
    if ".mobile-toc{display:none!important}" in nav_css:
        failures.append("site-nav.css: legacy !important rule would suppress the mobile chapter navigation")

    for page in PAGES:
        source = page.resolve()
        page_parser = parsed[source]

        # Runtime ownership contract: source HTML may load the terminology
        # runtime at most once, and must never load site-nav.js directly.
        # terms.js is the single owner that injects site-nav.css/site-nav.js;
        # Pages may add terms.js later only when the source page omits it.
        basenames = [script_basename(src) for src in page_parser.script_srcs]
        terms_count = basenames.count("terms.js")
        nav_count = basenames.count("site-nav.js")
        checked_runtime_pages += 1
        if terms_count > 1:
            failures.append(
                f"{page.relative_to(ROOT)}: terms.js loaded {terms_count} times; source HTML allows at most one"
            )
        if nav_count:
            failures.append(
                f"{page.relative_to(ROOT)}: direct site-nav.js load forbidden; terms.js owns navigation runtime"
            )

        for href in page_parser.hrefs:
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
        print("SITE FRAGMENT / RUNTIME SEAL FAIL")
        for item in failures:
            print(" -", item)
        raise SystemExit(f"{len(failures)} site routing/runtime contract failures")

    print(
        f"SITE FRAGMENT / RUNTIME SEAL PASS: {len(PAGES)} pages scanned; "
        f"{checked_files} local HTML links and {checked_fragments} fragments resolved; "
        f"{checked_runtime_pages} source pages obey single-owner navigation runtime; "
        "terms.js/site-nav.js idempotence plus mobile chapter-nav/anchor/table/equation guards locked."
    )


if __name__ == "__main__":
    main()

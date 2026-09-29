from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "modules"
OVERVIEW = MODULES / "open-source-modeling.html"
PROJECTS = sorted(MODULES.glob("open-source-*.html"))
PROJECTS = [p for p in PROJECTS if p.name != OVERVIEW.name]

REQUIRED_LEVEL_IDS = ["level-1", "level-2", "level-3", "level-4", "level-5"]
REQUIRED_PHRASES = [
    "Modeling Taste",
    "Exercises",
    "Source ledger",
    "Frozen commit",
    "Worked example",
    "real space 怎样变成 stacking phase",
    "verification tests",
]

def main() -> None:
    failures: list[str] = []
    if not OVERVIEW.exists():
        failures.append("missing Open-Source Modeling Lab overview")

    overview = OVERVIEW.read_text(encoding="utf-8") if OVERVIEW.exists() else ""
    if "open-source-moire-metrology.html" not in overview:
        failures.append("overview does not link first repository page")

    if not PROJECTS:
        failures.append("no repository learning pages found")

    for page in PROJECTS:
        text = page.read_text(encoding="utf-8")
        rel = page.relative_to(ROOT)
        if text.lower().count("<h1") != 1:
            failures.append(f"{rel}: expected exactly one h1")
        repo = re.search(r'data-upstream-repo="([^"]+)"', text)
        commit = re.search(r'data-upstream-commit="([0-9a-f]{40})"', text)
        if not repo:
            failures.append(f"{rel}: missing data-upstream-repo")
        if not commit:
            failures.append(f"{rel}: missing frozen 40-char commit SHA")
        for ident in REQUIRED_LEVEL_IDS:
            if f'id="{ident}"' not in text:
                failures.append(f"{rel}: missing {ident}")
        for phrase in REQUIRED_PHRASES:
            if phrase not in text:
                failures.append(f"{rel}: missing required section marker {phrase!r}")
        if text.count("class=\"evidence\"") < 6:
            failures.append(f"{rel}: fewer than 6 evidence/provenance blocks")
        if text.count("data-source-path=") < 10:
            failures.append(f"{rel}: fewer than 10 formula/code source anchors")
        if "<pre><code>" not in text:
            failures.append(f"{rel}: missing small source-code walkthrough")
        if "Relevance to my project" not in text:
            failures.append(f"{rel}: missing explicit short project bridge")
        if "TODO" in text or "TBD" in text:
            failures.append(f"{rel}: unfinished TODO/TBD marker")
        if 'href=""' in text:
            failures.append(f"{rel}: empty link")

    if failures:
        print("OPEN-SOURCE MODELING SEAL FAIL")
        for item in failures:
            print(" -", item)
        raise SystemExit(f"{len(failures)} Open-Source Modeling contract failures")

    print(
        f"OPEN-SOURCE MODELING SEAL PASS: overview + {len(PROJECTS)} repository page(s); "
        "frozen commits, five-level pedagogy, provenance blocks, geometry chain, worked example, verification tests, formula/code anchors, "
        "source walkthroughs, Modeling Taste, exercises and project bridges present."
    )

if __name__ == "__main__":
    main()

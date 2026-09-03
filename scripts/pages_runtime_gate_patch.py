from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / ".github" / "workflows" / "pages.yml"

marker = "      - name: Validate static site and Reproduction Lab evidence\n"
insert = (
    "      - name: Validate site structure and navigation runtime\n"
    "        run: python scripts/site_fragment_seal.py\n\n"
    + marker
)

raw = TARGET.read_text(encoding="utf-8")
if raw.count(marker) != 1:
    raise RuntimeError(f"expected one Pages validation marker, found {raw.count(marker)}")
if "Validate site structure and navigation runtime" in raw:
    raise RuntimeError("Pages runtime gate appears to be already installed")
updated = raw.replace(marker, insert, 1)

# Do not alter or duplicate the existing evidence validator/deploy chain.
for required in (
    "- name: Inject terminology runtime",
    "- name: Validate static site and Reproduction Lab evidence",
    "print('STATIC SITE + LAB07-12 EVIDENCE CONTRACT = PASS')",
    "uses: actions/configure-pages@v5",
    "uses: actions/upload-pages-artifact@v3",
    "uses: actions/deploy-pages@v4",
):
    if updated.count(required) != raw.count(required):
        raise RuntimeError(f"existing Pages contract marker drifted: {required}")
if updated.count("python scripts/site_fragment_seal.py") != 1:
    raise RuntimeError("expected exactly one site structure/runtime gate")

TARGET.write_text(updated, encoding="utf-8")
print("PAGES STRUCTURE/RUNTIME PREDEPLOY GATE PATCH = PASS")

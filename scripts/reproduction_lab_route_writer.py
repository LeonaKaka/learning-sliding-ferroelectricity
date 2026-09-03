from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "modules" / "numerical-modeling.html"

old = '<a href="reproduction-lab.html">Reproduction Lab</a>'
new = '<a href="reproduction-lab-overview.html">Reproduction Lab</a>'

raw = PAGE.read_text(encoding="utf-8")
if raw.count(old) != 1:
    raise RuntimeError(f"expected exactly one legacy Module 07 Lab entry, found {raw.count(old)}")
updated = raw.replace(old, new)
if updated.count(new) != 1:
    raise RuntimeError("new Lab overview route was not written exactly once")
PAGE.write_text(updated, encoding="utf-8")
print("MODULE 07 LAB OVERVIEW ROUTE WRITER PASS")

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "modules" / "reproduction-lab-overview.html"

old = '<script src="../terms.js"></script><script src="../site-nav.js"></script>'
new = '<script src="../terms.js"></script>'

raw = PAGE.read_text(encoding="utf-8")
if raw.count(old) != 1:
    raise RuntimeError(f"expected one duplicate Lab overview runtime chain, found {raw.count(old)}")
updated = raw.replace(old, new)
if '../site-nav.js' in updated:
    raise RuntimeError("Lab overview still directly loads site-nav.js")
PAGE.write_text(updated, encoding="utf-8")
print("LAB OVERVIEW NAV CLEANUP PASS")

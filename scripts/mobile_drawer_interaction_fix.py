from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "site-nav.js"

old = """  const mkBtn=(side,label,target)=>{const b=document.createElement('button');b.className=`nav-drawer-btn ${side}`;b.type='button';b.setAttribute('aria-label',label);b.textContent=side==='left'?'☰':'≡';b.onclick=()=>{document.getElementById(target).classList.toggle('open');document.body.classList.toggle('nav-drawer-open',document.querySelector('.site-sidebar.open,.page-toc.open'))};document.body.appendChild(b)};\n  mkBtn('left','打开全站导航','siteSidebar'); mkBtn('right','打开本页目录','pageToc');\n  document.addEventListener('click',e=>{if(innerWidth>=1280)return; const a=e.target.closest('.site-sidebar a,.page-toc a'); if(a){left.classList.remove('open');right.classList.remove('open');document.body.classList.remove('nav-drawer-open')}});\n"""

new = """  const drawerButtons=new Map();\n  const syncDrawerState=()=>{\n    const anyOpen=!!document.querySelector('.site-sidebar.open,.page-toc.open');\n    document.body.classList.toggle('nav-drawer-open',anyOpen);\n    for(const [target,b] of drawerButtons){\n      const expanded=document.getElementById(target)?.classList.contains('open')||false;\n      b.setAttribute('aria-expanded',expanded?'true':'false');\n      b.setAttribute('aria-label',expanded?b.dataset.closeLabel:b.dataset.openLabel);\n    }\n  };\n  const closeDrawers=()=>{left.classList.remove('open');right.classList.remove('open');syncDrawerState()};\n  const mkBtn=(side,label,target)=>{\n    const b=document.createElement('button');\n    b.className=`nav-drawer-btn ${side}`;\n    b.type='button';\n    b.dataset.openLabel=label;\n    b.dataset.closeLabel=label.replace(/^打开/,'关闭');\n    b.setAttribute('aria-label',label);\n    b.setAttribute('aria-controls',target);\n    b.setAttribute('aria-expanded','false');\n    b.textContent=side==='left'?'☰':'≡';\n    drawerButtons.set(target,b);\n    b.onclick=()=>{\n      const drawer=document.getElementById(target);\n      const opening=!drawer.classList.contains('open');\n      (target==='siteSidebar'?right:left).classList.remove('open');\n      drawer.classList.toggle('open',opening);\n      syncDrawerState();\n    };\n    document.body.appendChild(b);\n  };\n  mkBtn('left','打开全站导航','siteSidebar'); mkBtn('right','打开本页目录','pageToc');\n  document.addEventListener('click',e=>{if(innerWidth>=1280)return; const a=e.target.closest('.site-sidebar a,.page-toc a'); if(a)closeDrawers()});\n  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&document.querySelector('.site-sidebar.open,.page-toc.open'))closeDrawers()});\n"""

raw = TARGET.read_text(encoding="utf-8")
if raw.count(old) != 1:
    raise RuntimeError(f"expected exactly one legacy drawer block, found {raw.count(old)}")
if "aria-expanded" in raw or "drawerButtons" in raw:
    raise RuntimeError("mobile drawer interaction patch appears to be already applied")
updated = raw.replace(old, new)

required = [
    "aria-controls",
    "aria-expanded",
    "e.key==='Escape'",
    "target==='siteSidebar'?right:left",
    "closeDrawers",
]
for marker in required:
    if marker not in updated:
        raise RuntimeError(f"missing mobile drawer marker after patch: {marker}")

TARGET.write_text(updated, encoding="utf-8")
print("MOBILE DRAWER INTERACTION FIX = PASS")

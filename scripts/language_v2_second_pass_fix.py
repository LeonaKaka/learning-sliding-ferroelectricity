from __future__ import annotations

from bs4 import BeautifulSoup
from language_v2_second_pass import ROOT

TARGET = ROOT / "modules/reproduction-lab.html"

OLD = '<div class="eq">profile RMSE = √⟨(φ<sub>num</sub>−φ<sub>exact</sub>)²⟩　；　w<sub>num</sub>=|φ₀/φ′(0)|</div>'
NEW = '<div class="eq">剖面 RMSE = √⟨(φ<sub>num</sub>−φ<sub>exact</sub>)²⟩　；　w<sub>num</sub>=|φ₀/φ′(0)|</div>'

LOCKED_SCIENCE = (
    'φ*(x)=−φ₀ tanh(x/w)',
    'φ₀=√(α/δ)',
    'w=√(2γ/α)',
    'assert rmse &lt; 5e-4',
    'assert width_error &lt; 5e-3',
    '1.415395；误差 0.0835%',
    '9.75×10<sup>−5</sup>',
    '已知答案测试通过后才跑阈值批量扫描',
)

FORBIDDEN_VISIBLE = (
    'profile RMSE =',
    ' gate ', ' authority ', 'fit window', ' workflow ', ' checkpoint ',
    '热圆滑', 'Numerical 模型ing', '普适ity', 'De钉扎',
)


def main() -> None:
    raw = TARGET.read_text(encoding='utf-8')
    before = BeautifulSoup(raw, 'html.parser')
    images_before = [(x.get('src'), x.get('alt')) for x in before.find_all('img')]
    hrefs_before = [x.get('href') for x in before.find_all('a')]
    code_before = [str(x) for x in before.find_all('pre')]
    science_counts = {token: raw.count(token) for token in LOCKED_SCIENCE}

    if raw.count(OLD) != 1:
        raise RuntimeError(f'Lab 01 expected exactly one visible profile RMSE formula, found {raw.count(OLD)}')
    out = raw.replace(OLD, NEW, 1)

    after = BeautifulSoup(out, 'html.parser')
    if images_before != [(x.get('src'), x.get('alt')) for x in after.find_all('img')]:
        raise RuntimeError('Lab 01 Figure wiring changed')
    if hrefs_before != [x.get('href') for x in after.find_all('a')]:
        raise RuntimeError('Lab 01 href wiring changed')
    if code_before != [str(x) for x in after.find_all('pre')]:
        raise RuntimeError('Lab 01 code/terminal output changed')
    for token, count in science_counts.items():
        if out.count(token) != count:
            raise RuntimeError(f'Lab 01 scientific statement/result drifted: {token}')

    visible_no_code = BeautifulSoup(out, 'html.parser')
    for node in visible_no_code.find_all('pre'):
        node.decompose()
    outside_code = str(visible_no_code)
    for token in FORBIDDEN_VISIBLE:
        if token in outside_code:
            raise RuntimeError(f'Lab 01 final-audit residue found outside code: {token}')
    if '剖面 RMSE =' not in after.get_text(' ', strip=True):
        raise RuntimeError('Lab 01 Chinese RMSE label missing')

    TARGET.write_text(out, encoding='utf-8')
    print('Lab 01 final Language V2 residue repaired; code/terminal output/Figures/links/scientific results unchanged.')


if __name__ == '__main__':
    main()

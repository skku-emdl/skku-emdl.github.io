#!/usr/bin/env python3
"""EMDL homepage generator.

Edit the files in data/ (and the text in this file), then run:
    python3 build.py
All *.html pages in the repository root are regenerated.
"""
import json, html, re, pathlib

ROOT = pathlib.Path(__file__).parent

# 공식 오픈 전: 검색엔진 수집 막기. 오픈할 때 False 로 바꾸고 다시 빌드.
HIDE_FROM_SEARCH = False
D = lambda n: json.loads((ROOT / 'data' / n).read_text(encoding='utf-8'))
e = html.escape


def V(path):
    # cache-busting query from file content
    import hashlib
    return path + '?v=' + hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


def rich(t):
    # escape, then turn **text** into <b>text</b>
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', e(t))

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700&amp;'
         'family=Noto+Sans+KR:wght@400;500;700&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap" rel="stylesheet">')
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' "
           "fill='%23111418'/%3E%3Ctext x='16' y='22' font-family='serif' font-size='16' font-weight='700' fill='%23fff' "
           "text-anchor='middle'%3EE%3C/text%3E%3C/svg%3E")

MENU = [
    ('ABOUT', 'professor.html', [('Professor', 'professor.html'), ('Members', 'members.html')]),  # Alumni hidden for now: re-add ('Alumni', 'alumni.html') and SHOW_ALUMNI
    ('RESEARCH', 'research.html', [('Oxide & Hybrid Semiconductor Materials', 'research.html#synthesis'), ('Perovskite Optoelectronics', 'research.html#applications'),
                                   ('Sustainable Battery Materials', 'research.html#waste'), ('Facilities', 'facilities.html')]),
    ('PUBLICATIONS', 'publications.html', [('Selected Papers', 'publications.html#selected'), ('All Papers', 'publications.html#all'), ('Patents', 'patents.html')]),
    ('COMMUNITY', 'news.html', [('News', 'news.html'), ('Media', 'media.html'), ('Gallery', 'gallery.html')]),
    ('CONTACT', 'contact.html', [('Location', 'contact.html#location'), ('Recruitment', 'contact.html#recruit')]),
]
CHEVRON = '<svg aria-hidden="true" width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 3.5l3 3 3-3"></path></svg>'


def header(active):
    items = []
    for top, href, subs in MENU:
        cur = ' aria-current="page"' if top == active else ''
        sub = ''.join(f'<a href="{h}">{e(t)}</a>' for t, h in subs)
        items.append(f'<div class="item"><a class="top" href="{href}"{cur}>{top}{CHEVRON}</a><div class="sub">{sub}</div></div>')
    return f'''<header class="site-header">
<div class="wrap bar">
<a class="brand" href="index.html" aria-label="EMDL 홈">
<img src="assets/img/logo/skku-saint.png" alt="Sungkyunkwan University SAINT" width="307" height="65">
<span class="sep" aria-hidden="true"></span>
<span class="name"><b>EMDL</b><span>Energy Material and Device Lab</span></span>
</a>
<button class="menu-btn" type="button" aria-label="메뉴 열기" aria-expanded="false" aria-controls="nav">
<svg aria-hidden="true" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 6h14M3 10h14M3 14h14"/></svg>
</button>
<nav class="nav" id="nav" aria-label="주 메뉴">{''.join(items)}</nav>
</div>
</header>'''


FOOTER = f'''<footer class="site-footer">
<div class="wrap top">
<div class="addr"><b>Energy Material and Device Laboratory</b><br>성균관대학교 제2종합연구동 83240호 · 경기도 수원시 장안구 서부로 2066<br>Tel. 031-299-4180 · <a href="mailto:sss85@skku.edu">sss85@skku.edu</a></div>
<div class="partners">
<a href="https://saint.skku.edu/saint/index.do" aria-label="SAINT"><img src="assets/img/logo/saint.png" alt="SAINT 성균나노과학기술원" loading="lazy"></a>
<a href="https://www.krict.re.kr/" aria-label="KRICT"><img src="assets/img/logo/krict.png" alt="한국화학연구원 KRICT" loading="lazy"></a>
<a href="https://www.nrf.re.kr/index" aria-label="NRF"><img src="assets/img/logo/nrf.webp" alt="한국연구재단 NRF" loading="lazy"></a>
<a href="https://www.ketep.re.kr/" aria-label="KETEP"><img src="assets/img/logo/ketep.webp" alt="한국에너지기술평가원 KETEP" loading="lazy"></a>
</div>
</div>
<div class="wrap copy">© Energy Material and Device Laboratory, Sungkyunkwan University</div>
</footer>
<script src="{V('assets/js/site.js')}"></script>'''


def page(fname, title, active, body, desc=None, head_extra=''):
    desc = desc or 'Energy Material and Device Laboratory (EMDL), SAINT & Department of Nano Engineering, Sungkyunkwan University.'
    ROBOTS = '<meta name="robots" content="noindex, nofollow">\n' if HIDE_FROM_SEARCH else ''
    full = 'Energy Material and Device Lab | SKKU' if title is None else f'{title} | EMDL, SKKU'
    out = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ROBOTS}<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON}">
{FONTS}
<link rel="stylesheet" href="{V('assets/css/site.css')}">
{head_extra}
</head>
<body>
{header(active)}
<main>
{body}
</main>
{FOOTER}
</body>
</html>
'''
    (ROOT / fname).write_text(out, encoding='utf-8')


def page_head(crumb, h1, lead=''):
    lead = f'<p>{lead}</p>' if lead else ''
    return f'<section class="page-head"><div class="wrap"><p class="crumb">{crumb}</p><h1>{h1}</h1>{lead}</div></section>'


def bold_pi(a):
    a = e(a)
    return re.sub(r'(Seong ?[Ss]ik Shin\*?|SS Shin\*?)', r'<b>\1</b>', a)


# ---------- data ----------
PUBS = D('publications.json')
NEWS = D('news.json')
MEDIA = D('media.json')

# Selected papers: Nature, Science, Nature sister journals, Joule (as listed on the lab site)
SELECTED = [
    # 메인 화면 슬라이드: 2021 Nature 이후 + 2017 Science (BaSnO3, 제1저자)
    (66, 'Science', 'assets/img/pubs/science-2026.webp', '#8C1D18'),
    (62, 'Nature Photonics', 'assets/img/pubs/natphoton-2026.webp', '#0B3B5C'),
    (61, 'Joule', 'assets/img/pubs/joule-2025.webp', '#C2410C'),
    (59, 'Nature Energy', 'assets/img/pubs/natenergy-2025-cover.webp', '#0F5E52'),
    (50, 'Joule', 'assets/img/pubs/joule-2024-cover.webp', '#C2410C'),
    (49, 'Nature Energy', 'assets/img/pubs/natenergy-2024.webp', '#0F5E52'),
    (44, 'Nature', 'assets/img/pubs/nature-2021-cover.webp', '#111418'),
    (25, 'Science', 'assets/img/pubs/science-2017-6334.webp', '#8C1D18'),
]
PUB_BY_N = {p['n']: p for p in PUBS}


def pub_card(n, jn, img, color, fit='cover', hidden=False):
    p = PUB_BY_N[n]
    attrs = ' aria-hidden="true" tabindex="-1"' if hidden else ''
    ph = (f'<img src="{img}" alt="" loading="lazy" class="fit-{fit}">' if img
          else f'<span class="jn">{e(jn)}</span>')
    style = '' if img else f' style="background:{color}"'
    badge = '<em class="badge">FRONT COVER</em>' if p.get('cover') else ''
    url = p.get('url') or 'publications.html'
    return (f'<a class="pcard" href="{e(url)}"{attrs}><div class="ph"{style}>{ph}</div>'
            f'<div class="meta"><b>{e(jn)}</b><span>{p["year"]}</span></div>{badge}'
            f'<span class="t">{e(p["title"])}</span></a>')


def selected_slider():
    cards = ''.join(pub_card(*s) for s in SELECTED)
    dup = ''.join(pub_card(*s, hidden=True) for s in SELECTED)
    return ('<div class="slider">'
            '<button type="button" class="sl-btn prev" aria-label="이전 논문"><svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></button>'
            f'<div class="marquee"><div class="track">{cards}{dup}</div></div>'
            '<button type="button" class="sl-btn next" aria-label="다음 논문"><svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></button></div>')


# Publications 페이지 그리드에만 추가로 보이는 논문 (메인 슬라이드에는 미포함)
EXTRA_GRID = [
    (38, 'Energy & Environmental Science', 'assets/img/pubs/ees-2020-13-12.webp', '#1E5A46'),
    (36, 'Joule', 'assets/img/pubs/joule-2019.webp', '#C2410C'),
    (33, 'Energy & Environmental Science', 'assets/img/pubs/ees-2019-12-07.webp', '#1E5A46'),
    (32, 'Energy & Environmental Science', 'assets/img/pubs/ees-2019-12-03.webp', '#1E5A46'),
    (26, 'Science', 'assets/img/pubs/science-2017-6345.webp', '#8C1D18'),
]


def selected_grid():
    items = sorted(SELECTED + EXTRA_GRID, key=lambda s: (-PUB_BY_N[s[0]]['year'], -s[0]))
    return '<div class="pgrid">' + ''.join(pub_card(*s) for s in items) + '</div>'


# ---------- home ----------
HERO_FIG = (ROOT / 'data' / 'hero_figure.html').read_text(encoding='utf-8')

RESEARCH = [
    ('synthesis', '01', 'Oxide & Hybrid Semiconductor Materials', 'assets/img/research/topic-1.webp',
     '다양한 기능성 산화물 반도체 나노입자와 박막, 유무기 하이브리드 페로브스카이트 반도체 소재를 용액 공정과 진공 증착 등 여러 방법으로 합성하고, 그 원리와 계면을 규명합니다.'),
    ('applications', '02', 'Perovskite Optoelectronics: Large-Area & Flexible', 'assets/img/research/topic-2.webp',
     '고효율 페로브스카이트 태양전지와 페로브스카이트/페로브스카이트 탠덤 태양전지, LED, 최대 900 cm² 대면적 플렉서블 모듈, 태양전지–LED 양방향 융합 소자를 개발합니다.'),
    ('waste', '03', 'Sustainable Battery Materials', 'assets/img/research/topic-3.webp',
     '리튬이온전지와 안전한 아연 수계 이차전지, 폐타이어 재활용 카본블랙 도전재 등 지속가능한 배터리 소재와 태양전지–에너지 저장 하이브리드 시스템을 연구합니다.'),
]


def build_home():
    topics = ''.join(f'''<a class="topic" href="research.html#{k}"><div class="ph"><img src="{img}" alt="{e(t)} 연구 개요" loading="lazy"></div>
<span class="num">{num}</span><h3>{e(t)}</h3><p>{e(d)}</p></a>''' for k, num, t, img, d in RESEARCH)
    nitems = ''
    for n in NEWS[:5]:
        tag = 'a' if n['url'] else 'div'
        href = f' href="{e(n["url"])}"' if n['url'] else ''
        nitems += f'<{tag} class="nitem"{href}><span class="d">{e(n["date"] or "—")}</span><span>{rich(n["title"])}</span></{tag}>'
    v = MEDIA[0]
    body = f'''<section class="wrap hero" aria-label="연구실 소개">
<div class="text">
<p class="eyebrow">Sungkyunkwan University · SAINT · Dept. of Nano Engineering</p>
<h1><span>Energy Material</span><span>and Device Laboratory</span></h1>
<p class="en">Functional oxide semiconductors and hybrid perovskites for next-generation energy devices</p>
<p class="ko">산화물 반도체와 유무기 하이브리드 페로브스카이트 소재를 기반으로, 고효율 태양전지부터 발광소자, 이차전지, 대면적 모듈까지 차세대 에너지 소자를 연구합니다.</p>
<p class="aff">성균관대학교 나노공학과 · 성균나노과학기술원(SAINT)</p>
</div>
{HERO_FIG}
</section>

<section class="section soft" id="research">
<div class="wrap">
<div class="h2-row"><h2 class="h2">Research Areas</h2><a class="more" href="research.html">자세히 보기 →</a></div>
<div class="grid-3">{topics}</div>
</div>
</section>

<section class="section" id="publications">
<div class="wrap">
<div class="h2-row"><h2 class="h2">Selected Publications</h2><a class="more" href="publications.html">전체 논문 보기 →</a></div>
{selected_slider()}
</div>
</section>

<section class="section" id="news">
<div class="wrap news-row">
<div class="list">
<div class="h2-row"><h2 class="h2">Recent News</h2><a class="more" href="news.html">전체 소식 보기 →</a></div>
<div>{nitems}</div>
</div>
<div class="media">
<p class="eyebrow" style="color:var(--muted);margin-bottom:4px">In the Media</p>
<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{v['id']}" title="{e(v['title'])}" loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div>
<p style="margin:0;font-size:15px">{e(v['title'])}</p>
<p style="margin:0;font-size:14px" class="muted">{e(v['channel'])} · <a href="media.html">영상 더 보기 →</a></p>
</div>
</div>
</section>

<section class="section soft" id="contact">
<div class="wrap recruit">
<div class="l">
<h2 class="h2 ko" style="margin-bottom:16px">함께할 대학원생을 찾습니다</h2>
<p style="margin:0 0 24px;max-width:560px;color:var(--ink-2)">학부연구생, 석사, 석박통합, 박사과정을 모집합니다. 신소재, 화공, 기계, 나노, 에너지뿐 아니라 다양한 전공의 지원을 환영합니다.</p>
<a class="btn" href="mailto:sss85@skku.edu">sss85@skku.edu 로 문의하기</a>
</div>
</div>
</section>'''
    page('index.html', None, '', body,
         desc='Energy Material and Device Laboratory (EMDL), SAINT & Department of Nano Engineering, Sungkyunkwan University. Functional oxide semiconductors and hybrid perovskites for next-generation energy devices.',
         head_extra=f'<link rel="stylesheet" href="{V("assets/css/hero.css")}">')


# ---------- professor ----------
REVIEWED = ['Nature', 'Nature Energy', 'Nature Materials', 'Nature Nanotechnology', 'Nature Communications', 'Joule',
            'Journal of the American Chemical Society', 'Energy & Environmental Science', 'Advanced Materials', 'Advanced Energy Materials',
            'Advanced Functional Materials', 'ACS Energy Letters', 'ACS Applied Materials & Interfaces', 'Small', 'The Innovation']


def build_professor():
    exp = [('2024–', 'Associate Professor, SKKU Advanced Institute of Nano Technology (SAINT) & Department of Nano Engineering, Sungkyunkwan University'),
           ('2022–2024', 'Assistant Professor, SKKU Advanced Institute of Nano Technology (SAINT) & Department of Nano Engineering, Sungkyunkwan University'),
           ('2017–2022', 'Senior Researcher, Division of Advanced Materials, Korea Research Institute of Chemical Technology (KRICT)'),
           ('2016–2017', 'Postdoctoral Researcher, Department of Mechanical Engineering, Massachusetts Institute of Technology (MIT)')]
    edu = [('2012–2017', 'Ph.D. in Materials Science & Engineering, Seoul National University (Advisor: Prof. Young-Chang Joo)'),
           ('2004–2008', 'B.S. in Chemical Engineering, Kyung Hee University')]
    honors = [('2024', '장관표창 (과학기술정책 유공), 과학기술정보통신부'), ('2023', '젊은 과학자 자문위원 선정'),
              ('2022', '국가연구개발 우수성과 100선 에너지·환경 분야 최우수 성과 선정, 과학기술정보통신부'), ('2022', '자랑스러운 영락인상 (영락재단)'),
              ('2022', '공로상, 한국화학연구원'), ('2022', '장관상, 과학기술정보통신부'),
              ('2021', 'Highly Cited Author, Royal Society of Chemistry (RSC)'), ('2021', '우수직원상, 한국화학연구원'),
              ('2021', '공로상, 한국화학연구원'), ('2020', '장관표창, 과학기술정보통신부'), ('2020', '이사장상, 국가과학기술연구회'),
              ('2016', 'KRICT 창의상 (한국화학연구원)'), ('2015', '삼성휴먼테크 논문대상 (삼성전자)')]
    sel = [(66, 'Science'), (62, 'Nature Photonics'), (61, 'Joule'), (59, 'Nature Energy'), (50, 'Joule (Front Cover)'),
           (49, 'Nature Energy'), (44, 'Nature (Front Cover)'), (38, 'Energy & Environmental Science'),
           (36, 'Joule'), (33, 'Energy & Environmental Science'), (32, 'Energy & Environmental Science'), (26, 'Science'), (25, 'Science')]
    li = lambda rows: ''.join(f'<li><span class="y">{y}</span><span>{e(t)}</span></li>' for y, t in rows)
    sel_li = ''.join(f'<li><span class="y">{PUB_BY_N[n]["year"]}</span><span><a href="{e(PUB_BY_N[n]["url"] or "publications.html")}" class="plain">{e(PUB_BY_N[n]["title"])}</a>. <b><i>{e(j)}</i></b></span></li>' for n, j in sel)
    body = page_head('About · Professor', 'Principal Investigator') + f'''
<section class="section"><div class="wrap">
<div class="prof">
<div class="photo"><img src="assets/img/people/prof-shin.webp" alt="신성식 교수" width="642" height="900"></div>
<div class="info">
<h2>신성식<small>Seong Sik Shin</small></h2>
<p class="role">Associate Professor<br>SKKU Advanced Institute of Nano Technology (SAINT) &amp; Department of Nano Engineering, Sungkyunkwan University</p>
<dl class="kv">
<dt>OFFICE</dt><dd>Research Complex 2, 2F #83240, Sungkyunkwan University, Suwon, Korea</dd>
<dt>TEL</dt><dd>+82-31-299-4180</dd>
<dt>E-MAIL</dt><dd><a href="mailto:sss85@skku.edu">sss85@skku.edu</a></dd>
</dl>
<div class="cv cv-in">
<div><h3>Professional Experience</h3><ul>{li(exp)}</ul></div>
<div><h3>Education</h3><ul>{li(edu)}</ul></div>
</div>
</div>
</div>
<div class="cv">
<div><h3>Selected Journal Articles</h3><ul>{sel_li}</ul></div>
<div><h3>Honors &amp; Awards</h3><ul>{li(honors)}</ul></div>
</div>
<div class="cv">
<div class="wide"><h3>Professional Activities</h3>
<p class="act-h">Journal Reviewer</p>
<p class="act">{', '.join(f'<i>{e(j)}</i>' for j in REVIEWED)}, and others</p>
<p class="act-h">Advisory</p>
<p class="act">젊은 과학자 자문위원 (2023)</p>
</div>
</div>
</div></section>'''
    page('professor.html', 'Professor', 'ABOUT', body)


def person(p, alumni=False, show_course=True):
    ph = (f'<img src="{p["photo"]}" alt="{e(p["ko"])}" loading="lazy">' if p.get('photo')
          else f'<span class="ini" aria-hidden="true">{e(p["ko"][0])}</span>')
    en = f'<small>{e(p["en"])}</small>' if p.get('en') else ''
    course = f'<p class="course">{e(p["course"])}</p>' if p.get('course') and show_course else ''
    extra = ''
    if alumni:
        if p.get('note'):
            extra = f'<ul><li>{e(p["note"])}</li></ul>'
    else:
        extra = '<ul>' + ''.join(f'<li>{e(t)}</li>' for t in p.get('topics', [])) + '</ul>'
    mail = f'<a class="mail" href="mailto:{e(p["email"])}">{e(p["email"])}</a>' if p.get('email') else ''
    return f'<article class="person"><div class="ph">{ph}</div><h3>{e(p["ko"])}{en}</h3>{course}{extra}{mail}</article>'


def build_members():
    ms = D('members.json')
    groups = [('Postdoctoral Researchers', ('Postdoctoral Researcher',)),
              ('Ph.D. Candidates', ('Ph.D. Candidate',)),
              ('Combined M.S./Ph.D. Candidates', ('Combined M.S./Ph.D. Candidate',)),
              ('M.S. Candidates', ('M.S. Candidate',)),
              ('Interns', ('Intern',))]
    known = {c for _, cs in groups for c in cs}
    out = ''
    for title, cs in groups + [('Members', None)]:
        sel = [m for m in ms if (m.get('course') in cs if cs else m.get('course') not in known)]
        if sel:
            out += (f'<h2 class="sub-h">{title}</h2>'
                    f'<div class="people">{"".join(person(m, show_course=False) for m in sel)}</div>')
    body = page_head('About · Members', 'Current Members', '에너지 소재와 소자를 함께 연구하는 EMDL 구성원입니다.') + \
        f'<section class="section"><div class="wrap members">{out}</div></section>'
    page('members.html', 'Members', 'ABOUT', body)


def alum(p):
    en = f'<small>{e(p["en"])}</small>' if p.get('en') else ''
    course = f'<span class="course">{e(p.get("course", ""))}</span>'
    note = f'<span class="note">{e(p["note"])}</span>' if p.get('note') else ''
    mail = f'<a class="mail" href="mailto:{e(p["email"])}">{e(p["email"])}</a>' if p.get('email') else ''
    return f'<article class="alum"><h3>{e(p["ko"])}{en}</h3>{note}{mail}</article>'


SHOW_ALUMNI = False


def build_alumni():
    if not SHOW_ALUMNI:
        (ROOT / 'alumni.html').unlink(missing_ok=True)
        return
    al = D('alumni.json')
    body = page_head('About · Alumni', 'Alumni') + \
        f'<section class="section"><div class="wrap"><div class="alumni">{"".join(alum(a) for a in al)}</div></div></section>'
    page('alumni.html', 'Alumni', 'ABOUT', body)


# ---------- research ----------
OVERVIEW = ('<figure class="overview"><div class="ov-wrap"><img src="assets/img/research/overview-flow.webp" alt="연구 흐름: 산화물·페로브스카이트 소재, 태양전지, 대면적 플렉서블 모듈, 에너지 저장, 발광 소자"><span class="ov-l l" style="left:3%;top:90%"><i>1</i><em>산화물 · 페로브스카이트 소재</em></span><span class="ov-l c" style="left:30%;top:61%"><i>2</i><em>태양전지 · 탠덤</em></span><span class="ov-l c" style="left:53.5%;top:60.5%"><i>3</i><em>대면적 플렉서블 모듈</em></span><span class="ov-l c" style="left:68.6%;top:67.5%"><i>4</i><em>에너지 저장</em></span><span class="ov-l c" style="left:84%;top:90%"><i>5</i><em>발광 (LED)</em></span></div><ol class="ov-key"><li>산화물 · 페로브스카이트 소재</li><li>태양전지 · 탠덤</li><li>대면적 플렉서블 모듈</li><li>에너지 저장</li><li>발광 (LED)</li></ol></figure>')


def build_research():
    blocks = f'''
<div class="rblock" id="synthesis">
<p class="eyebrow">01</p>
<h2>Oxide &amp; Hybrid Semiconductor Materials</h2>
<p class="lead">새로운 산화물 반도체와 유무기 하이브리드 페로브스카이트 반도체 소재를 탐색하고 합성합니다. 저온·고속 합성 공정과 대면적 공정을 개발하고, 합성 원리와 소재 간 계면을 규명해 고성능 에너지 소자의 기반을 만듭니다.</p>
<ul class="chips"><li>Oxide Nanoparticles</li><li>Oxide Thin Films</li><li>Hybrid Perovskite Materials</li><li>Solution &amp; Vacuum Processes</li><li>Interface Engineering</li></ul>
<figure><img src="assets/img/research/oxide-nanomaterials.webp" alt="산화물 나노소재 연구 개요: 소재, 공정, 소자" loading="lazy"></figure>
<figure><img src="assets/img/research/oxide-synthesis.webp" alt="주석 기반 산화물 반도체 합성 및 메커니즘 규명" loading="lazy"></figure>
</div>
<div class="rblock" id="applications">
<p class="eyebrow">02</p>
<h2>Perovskite Optoelectronics: Large-Area &amp; Flexible</h2>
<p class="lead">산화물 전자수송층을 기반으로 고효율 페로브스카이트 태양전지, 페로브스카이트/페로브스카이트 탠덤 태양전지, LED를 만들고, 이를 최대 900 cm² 대면적 플렉서블 모듈과 태양전지–LED 양방향 융합 소자로 확장합니다. 태양전지–에너지 저장장치 하이브리드 시스템도 함께 연구합니다.</p>
<ul class="chips"><li>Perovskite Solar Cells</li><li>All-Perovskite Tandem Solar Cells</li><li>Flexible Perovskite Solar Cells</li><li>Large-Area (Flexible) Solar Modules</li><li>Perovskite LEDs</li><li>Solar Cell–LED</li><li>Solar Cell–Battery</li><li>Solar Cell–Supercapacitor</li><li>Solar Cell–Water Splitting</li></ul>
<figure><img src="assets/img/research/applications-oxide.webp" alt="산화물 반도체 소재 응용: 태양전지, LED, 태양-연료, 에너지 저장" loading="lazy"></figure>
<figure><img src="assets/img/research/large-area-modules.webp" alt="단위소자에서 대면적 모듈까지: 30x30 유연 모듈" loading="lazy"></figure>
<figure><img src="assets/img/research/hybrid-system.webp" alt="태양전지-에너지 저장장치 및 태양전지-LED 일체형 하이브리드 소자" loading="lazy"></figure>
</div>
<div class="rblock" id="waste">
<p class="eyebrow">03</p>
<h2>Sustainable Battery Materials</h2>
<p class="lead">리튬이온전지와 물 기반 전해질을 쓰는 안전한 아연 수계 이차전지, 그리고 폐타이어를 재활용한 고성능 전도성 카본블랙 도전재 등 지속가능한 배터리 소재를 연구합니다.</p>
<ul class="chips"><li>Li-ion Batteries</li><li>Aqueous Zinc Batteries</li><li>Conductive Carbon Black from Waste Tires</li><li>Solar Cell–Battery Hybrids</li></ul>
<figure><img src="assets/img/research/waste-recovery.webp" alt="폐타이어 재활용 및 고성능 전도성 카본블랙 개발" loading="lazy"></figure>
</div>'''
    body = page_head('Research', 'Research', '기능성 산화물 소재와 유무기 하이브리드 소재의 합성 원리를 규명하고, 이를 태양전지, 발광다이오드, 수소 생산, 이차전지와 하이브리드 에너지 시스템으로 확장합니다.') + \
        f'<section class="section"><div class="wrap">{OVERVIEW}{blocks}</div></section>'
    page('research.html', 'Research', 'RESEARCH', body)


def build_facilities():
    f = D('facilities.json')
    def grid(lab, start):
        return '<div class="fgrid">' + ''.join(
            f'<figure><img src="assets/img/facilities/f{start + i:02d}.webp" alt="{e(n)}" loading="lazy"><figcaption>{e(n)}</figcaption></figure>'
            for i, n in enumerate(lab['items'])) + '</div>'
    body = page_head('Research · Facilities', 'Facilities', '2023년 2월 실험실 구축 완료. 소재 합성실과 항온·항습 소자 제작 및 측정실을 운영합니다.') + f'''
<section class="section"><div class="wrap">
<figure style="margin:0 0 8px"><img src="assets/img/facilities/f00.webp" alt="실험실 1 소재 합성실과 실험실 2 소자 제작실 전경" style="border:1px solid var(--line)"></figure>
<h2 class="sub-h" style="margin-top:48px">{e(f['lab1']['name'])}<br><small class="mono muted" style="font-size:14px;font-weight:400">{e(f['lab1']['en'])}</small></h2>
{grid(f['lab1'], 1)}
<h2 class="sub-h">{e(f['lab2']['name'])}<br><small class="mono muted" style="font-size:14px;font-weight:400">{e(f['lab2']['en'])}</small></h2>
{grid(f['lab2'], 11)}
</div></section>'''
    page('facilities.html', 'Facilities', 'RESEARCH', body)


# ---------- publications ----------
def build_publications():
    years = sorted({p['year'] for p in PUBS}, reverse=True)
    chips = ''.join(f'<a href="#y{y}">{y}</a>' for y in years)
    out = ''
    for y in years:
        items = ''
        for p in [q for q in PUBS if q['year'] == y]:
            t = e(p['title'])
            t = f'<a href="{e(p["url"])}">{t}</a>' if p['url'] else t
            tag = '<span class="tag">FRONT COVER</span>' if p.get('cover') else ''
            press = ''
            if p.get('press'):
                li = [f'<li><a href="{e(x["url"])}">{e(x["text"])}</a></li>' for x in p['press']]
                press = '<ul class="press">' + ''.join(li[:3]) + '</ul>'
                if len(li) > 3:
                    press += (f'<details class="press-box"><summary>언론 보도 {len(li) - 3}건 더보기</summary><ul class="press">'
                              + ''.join(li[3:]) + '</ul></details>')
            items += (f'<li class="pub"><span class="n">{p["n"]}</span><div><p class="tt">{t}</p>'
                      f'<p class="au">{bold_pi(p["authors"])}</p><p class="vn">{e(p["venue"])}{tag}</p>{press}</div></li>')
        out += f'<div class="year"><h2 id="y{y}">{y}</h2><ol>{items}</ol></div>'
    body = page_head('Publications', 'Publications', '* Corresponding author') + f'''
<section class="section" id="selected"><div class="wrap">
<div class="h2-row"><h2 class="h2">Selected Papers</h2></div>
{selected_grid()}
</div></section>
<section class="section" id="all"><div class="wrap">
<div class="h2-row"><h2 class="h2">All Papers</h2></div>
<nav class="filters" aria-label="연도별 이동">{chips}</nav>
{out}
</div></section>'''
    page('publications.html', 'Publications', 'PUBLICATIONS', body)


# ---------- community ----------
def build_news():
    cards = ''
    for n in NEWS:
        title = f'<a class="plain" href="{e(n["url"])}">{rich(n["title"])}</a>' if n['url'] else rich(n['title'])
        press = ''
        if n.get('press'):
            li = [f'<li><a href="{e(u)}"><b>{e(src)}</b> {e(t)}</a></li>' for src, t, u in n['press']]
            press = '<ul>' + ''.join(li[:3]) + '</ul>'
            if len(li) > 3:
                press += f'<details class="press-box"><summary>기사 {len(li) - 3}건 더보기</summary><ul>' + ''.join(li[3:]) + '</ul></details>'
        ph = (f'<img src="{n["img"]}" alt="" loading="lazy">' if n.get('img')
              else f'<span class="ph-label">{e(n.get("label", "News"))}</span>')
        cards += (f'<article class="news-card"><div class="ph">{ph}</div><div>'
                  f'<span class="mono muted" style="font-size:14px">{e(n["date"])}</span><h3>{title}</h3><p>{e(n["desc"])}</p>{press}</div></article>')
    body = page_head('Community · News', 'News') + f'<section class="section"><div class="wrap">{cards}</div></section>'
    page('news.html', 'News', 'COMMUNITY', body)


def build_media():
    items = ''.join(f'''<div><div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{v['id']}" title="{e(v['title'])}" loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div>
<p class="ch">{e(v['channel'])} · {e(v.get('date', ''))}</p><p class="vt">{e(v['title'])}</p></div>''' for v in MEDIA)
    body = page_head('Community · Media', 'Media', '방송과 인터뷰로 소개된 EMDL의 연구입니다.') + f'<section class="section"><div class="wrap"><div class="vgrid">{items}</div></div></section>'
    page('media.html', 'Media', 'COMMUNITY', body)


def build_gallery():
    g = D('gallery.json')
    out = ''
    for y in sorted({x['year'] for x in g}, reverse=True):
        figs = ''.join(f'<figure><img src="{x["img"]}" alt="{e(x["title"])}" loading="lazy"><figcaption>{e(x["title"])}<span>{e(x["date"])}</span></figcaption></figure>'
                       for x in g if x['year'] == y)
        out += f'<h2 class="sub-h">{y}</h2><div class="ggrid">{figs}</div>'
    body = page_head('Community · Gallery', 'Gallery') + f'<section class="section"><div class="wrap">{out}</div></section>'
    page('gallery.html', 'Gallery', 'COMMUNITY', body)


def build_contact():
    body = page_head('Contact', 'Contact') + '''
<section class="section" id="location"><div class="wrap recruit">
<div class="l">
<h2 class="sub-h" style="margin-top:0">Location</h2>
<iframe class="map" title="성균관대학교 제2종합연구동 지도" loading="lazy" src="https://maps.google.com/maps?hl=ko&amp;q=%EC%84%B1%EA%B7%A0%EA%B4%80%EB%8C%80%ED%95%99%EA%B5%90+%EC%A0%9C2%EC%A2%85%ED%95%A9%EC%97%B0%EA%B5%AC%EB%8F%99&amp;ll=37.293267,126.978485&amp;z=17&amp;output=embed"></iframe>
</div>
<div class="r">
<p style="margin:0 0 6px;font-weight:700;color:var(--ink)">성균관대학교 제2종합연구동 83240호</p>
<p style="margin:0 0 20px">경기도 수원시 장안구 서부로 2066<br>(천천동 300)</p>
<p style="margin:0 0 6px;font-weight:700;color:var(--ink)">Research Complex #2, Rm 83240</p>
<p style="margin:0 0 20px">Sungkyunkwan University (SKKU)<br>2066 Seobu-ro, Jangan-gu, Suwon-si,<br>Gyeonggi-do, Korea</p>
<p style="margin:0">Tel. 031-299-4180<br><a href="mailto:sss85@skku.edu">sss85@skku.edu</a></p>
</div>
</div></section>
<section class="section soft" id="recruit"><div class="wrap">
<h2 class="h2 ko" style="margin-bottom:16px">신입 대학원생 모집</h2>
<p style="max-width:760px;color:var(--ink-2)">성균관대 신성식 교수 연구실에서 자발적이고 독립적인 연구자가 될 신입 대학원생을 모집합니다. 본 연구실은 차세대 에너지 소재 및 소자 관련 연구를 수행하고 있습니다. 상기 연구에 관심이 있고, 꿈과 열정이 넘치며, 학위 취득 후 세계적인 연구자가 되고자 하는 학생들의 지원을 환영합니다.</p>
<p style="max-width:760px;color:var(--ink-2)">학부연구생, 석사, 석박통합, 박사과정을 모집하며 신소재, 화공, 기계, 나노, 에너지뿐 아니라 다양한 전공의 지원을 환영합니다. 상담과 문의는 언제든 환영합니다.</p>
<a class="btn" href="mailto:sss85@skku.edu">sss85@skku.edu 로 문의하기</a>
</div></section>'''
    page('contact.html', 'Contact', 'CONTACT', body)


def build_patents():
    pats = D('patents.json')
    if not pats:
        body = page_head('Publications · Patents', 'Patents') + \
            '<section class="section"><div class="wrap"><p class="lead">특허 목록을 정리하고 있습니다. 곧 업데이트됩니다.</p></div></section>'
        page('patents.html', 'Patents', 'PUBLICATIONS', body)
        return
    def entry(x):
        t = e(x['title'])
        t = f'<a href="{e(x["url"])}">{t}</a>' if x.get('url') else t
        en = f'<p class="au">{e(x["title_en"])}</p>' if x.get('title_en') else ''
        parts = []
        if x.get('status') == '등록' and x.get('reg_no'):
            parts.append(f'등록번호 {x["reg_no"]}')
        parts.append(f'출원번호 {x["app_no"]}')
        return (f'<li class="pub"><span class="n">{e(x.get("status", ""))}</span><div><p class="tt">{t}</p>'
                f'{en}<p class="vn">{e(" · ".join(parts))}</p></div></li>')

    kr = [x for x in pats if x.get('country', 'KR') == 'KR']
    pct = sorted([x for x in pats if x.get('country') == 'PCT'], key=lambda x: x['app_date'], reverse=True)
    out = ''
    for y in sorted({str(x['year']) for x in kr}, reverse=True):
        out += f'<div class="year"><h2 id="p{y}">{y}</h2><ol>{"".join(entry(x) for x in kr if str(x["year"]) == y)}</ol></div>'
    reg = sum(1 for x in kr if x.get('status') == '등록')
    sections = f'<h2 class="sub-h" id="domestic">국내 특허 (Korea)</h2>{out}'
    if pct:
        pout = ''
        for y in sorted({str(x['year']) for x in pct}, reverse=True):
            pout += f'<div class="year"><h2>{y}</h2><ol>{"".join(entry(x) for x in pct if str(x["year"]) == y)}</ol></div>'
        sections += f'<h2 class="sub-h" id="international">국제 특허 (PCT)</h2>{pout}'
    lead = f'국내 등록 {reg}건 · 국내 출원 {len(kr) - reg}건 · PCT 국제출원 {len(pct)}건'
    body = page_head('Publications · Patents', 'Patents', lead) + f'<section class="section"><div class="wrap">{sections}</div></section>'
    page('patents.html', 'Patents', 'PUBLICATIONS', body)


if __name__ == '__main__':
    for f in (build_home, build_professor, build_members, build_alumni, build_research, build_facilities,
              build_publications, build_patents, build_news, build_media, build_gallery, build_contact):
        f()
    print('built', len(list(ROOT.glob('*.html'))), 'pages')

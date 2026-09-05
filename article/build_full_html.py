from pathlib import Path
import json, re, html
import mistune
from bs4 import BeautifulSoup, NavigableString

root = Path(__file__).resolve().parents[1]
md_text = (root / 'article/full.md').read_text(encoding='utf-8')
tips = json.loads((root / 'data/tips.json').read_text(encoding='utf-8'))

renderer = mistune.HTMLRenderer(escape=False)
md = mistune.create_markdown(renderer=renderer, plugins=['table', 'url'])
article_html = md(md_text)
soup = BeautifulSoup(article_html, 'html.parser')

# Standalone page supplies hero/spoiler chrome.
first_h1 = soup.find('h1')
if first_h1:
    first_h1.decompose()
first_blockquote = soup.find('blockquote')
if first_blockquote and 'SPOILER WARNING' in first_blockquote.get_text(' ', strip=True):
    first_blockquote.decompose()

# Extract the author line from Markdown so it can truly be the final page element.
author_html = ''
for p in list(soup.find_all('p')):
    text = p.get_text(' ', strip=True)
    if text.startswith('Author') and '夕空ユウ' in text:
        author_html = str(p)
        p.decompose()
        break

# Heading IDs and menu contents.
used = set()
toc = []
def slug_heading(txt: str) -> str:
    t = txt.strip()
    m = re.match(r'^(\d{2})[\s　]+', t)
    if m:
        return f's{m.group(1)}'
    if t.upper() == 'SOURCE NOTES':
        return 'sources'
    s = re.sub(r'[^a-zA-Z0-9ぁ-んァ-ヶ一-龠]+', '-', t).strip('-').lower()
    return s or 'section'

for h in soup.find_all('h2'):
    sid = slug_heading(h.get_text(' ', strip=True))
    base = sid
    i = 2
    while sid in used:
        sid = f'{base}-{i}'
        i += 1
    used.add(sid)
    h['id'] = sid
    toc.append((sid, h.get_text(' ', strip=True)))

# Tips: exact display names plus a few prose aliases.
aliases = {v['name']: k for k, v in tips.items()}
aliases.update({
    'パワプロクンポケット': 'pawapoke',
    'トゥルー': 'true_end',
    '登録選手数': 'registered_player',
    'ジオット': 'gio',
    'ホンフー': 'hongfu',
    '6人組': 'six',
    'カタストロフ': 'catastrophe',
    '一撃計画': 'one_strike',
    'ポケレンジャー': 'pokerangers',
    'ハタ人間': 'hata',
    'しあわせ島編': 'shiawase_island',
    '秘密結社編': 'secret_society_ura',
    '海洋冒険編': 'marine_ura',
    '札侍編': 'fudasamurai',
})
pattern = re.compile('|'.join(map(re.escape, sorted(aliases, key=len, reverse=True))))
used_keys = set()
skip_parents = {'a', 'code', 'pre', 'script', 'style', 'button', 'h1', 'h2', 'h3', 'th'}

for node in list(soup.find_all(string=True)):
    if not isinstance(node, NavigableString) or not node.strip():
        continue
    if node.parent and node.parent.name in skip_parents:
        continue
    text = str(node)
    pos = 0
    pieces = []
    changed = False
    for m in pattern.finditer(text):
        key = aliases[m.group(0)]
        if key in used_keys:
            continue
        pieces.append(NavigableString(text[pos:m.start()]))
        b = soup.new_tag('button', attrs={
            'type': 'button',
            'class': 'tip-trigger',
            'data-tip': key,
            'aria-label': f"{tips[key]['name']}のTipsを開く",
        })
        b.string = m.group(0)
        pieces.append(b)
        pos = m.end()
        used_keys.add(key)
        changed = True
    if changed:
        pieces.append(NavigableString(text[pos:]))
        for p in reversed(pieces):
            node.insert_after(p)
        node.extract()

# Wrap wide tables for mobile.
for table in soup.find_all('table'):
    wrap = soup.new_tag('div', attrs={
        'class': 'table-wrap',
        'role': 'region',
        'aria-label': '横スクロールできる表',
        'tabindex': '0',
    })
    table.wrap(wrap)

article_inner = str(soup)

toc_items = []
for sid, title in toc:
    label = html.escape(title)
    toc_items.append(f'<li><a href="#{html.escape(sid)}"><span>{label[:2] if sid.startswith("s") else "—"}</span>{label}</a></li>')
toc_html = ''.join(toc_items)

category_labels = {
    'series': 'シリーズ', 'system': '遊び方', 'character': '人物', 'organization': '組織',
    'technology': '技術', 'power': '能力', 'concept': '概念', 'place': '場所',
    'ura': '裏サクセス', 'meta': 'メタ',
}
spoiler_labels = {'low': '軽度', 'medium': '中', 'high': '高', 'critical': '核心'}
index_items = []
for key, v in tips.items():
    search = f"{v['name']} {v['summary']} {category_labels.get(v['category'], v['category'])} {v['first']}"
    index_items.append(f'''<li class="index-item" data-search="{html.escape(search)}" data-category="{html.escape(v['category'])}">
<button type="button" class="index-open" data-tip-index="{html.escape(key)}">
<span class="index-name">{html.escape(v['name'])}</span>
<span class="index-meta">{html.escape(category_labels.get(v['category'], v['category']))} · 初出 {html.escape(v['first'])}</span>
</button></li>''')
index_html = '\n'.join(index_items)
tips_json = json.dumps(tips, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

css = r'''
:root{
  --paper:#f2efe7; --paper2:#fbfaf6; --ink:#171717; --muted:#706b63; --line:#bbb3a7;
  --accent:#b83229; --accent2:#21495a; --dark:#111; --max:1220px; --article:744px;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Kaku Gothic ProN","Yu Gothic",Meiryo,sans-serif;
  --serif:"Yu Mincho","Hiragino Mincho ProN",Georgia,serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:72px}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:17px;line-height:2;letter-spacing:.01em}
button,input{font:inherit}
a{color:inherit}
.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.skip-link{position:fixed;left:12px;top:-80px;z-index:1000;background:#fff;padding:8px 12px;border:1px solid var(--ink)}
.skip-link:focus{top:12px}

.sitebar{position:sticky;top:0;z-index:40;height:58px;background:rgba(242,239,231,.96);backdrop-filter:blur(10px);border-bottom:1px solid var(--ink)}
.sitebar-inner{max-width:var(--max);height:100%;margin:auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;gap:20px}
.brand{font-size:12px;font-weight:800;letter-spacing:.14em;white-space:nowrap}
.menu-button{border:0;background:transparent;color:var(--ink);display:flex;align-items:center;gap:10px;padding:7px 0;cursor:pointer;font-size:12px;font-weight:800;letter-spacing:.12em}
.menu-icon{width:24px;height:16px;position:relative;display:block}
.menu-icon::before,.menu-icon::after,.menu-icon span{content:"";position:absolute;right:0;height:1px;background:currentColor}
.menu-icon::before{top:0;width:24px}.menu-icon span{top:7px;width:17px}.menu-icon::after{bottom:0;width:24px}
.menu-button:hover .menu-icon span,.menu-button:focus-visible .menu-icon span{width:24px}
.menu-button:focus-visible{outline:2px solid var(--accent);outline-offset:6px}

.hero{border-bottom:1px solid var(--ink);background:var(--paper2)}
.hero-inner{max-width:var(--max);margin:auto;padding:72px 24px 62px;display:grid;grid-template-columns:minmax(0,1fr) 210px;gap:56px;align-items:end}
.eyebrow{margin:0 0 18px;color:var(--accent);font-size:11px;font-weight:900;letter-spacing:.16em}
.hero h1{margin:0;font-family:var(--serif);font-size:clamp(40px,5.5vw,74px);line-height:1.22;letter-spacing:-.045em;font-weight:700}
.hero-deck{max-width:760px;margin:25px 0 0;font-size:18px;line-height:1.8;color:#393632}
.hero-code{border-left:1px solid var(--line);padding-left:22px;color:var(--muted);font-size:11px;line-height:1.7;letter-spacing:.08em}
.hero-code strong{display:block;color:var(--ink);font-size:34px;line-height:1;margin-bottom:12px;letter-spacing:-.04em}
.spoiler-bar{background:var(--dark);color:#fff;border-bottom:1px solid var(--dark)}
.spoiler-inner{max-width:var(--max);margin:auto;padding:10px 24px;font-size:12px;letter-spacing:.03em}
.spoiler-inner strong{color:#ff8178;letter-spacing:.11em}

.layout{max-width:var(--max);margin:auto;padding:72px 24px 110px;display:grid;grid-template-columns:minmax(0,var(--article)) minmax(220px,280px);gap:82px;align-items:start}
.article{min-width:0}
.article>p{margin:0 0 1.45em}
.article>p:first-child{font-size:20px}
.article h2{font-family:var(--serif);font-size:36px;line-height:1.42;letter-spacing:-.025em;margin:5.2rem 0 1.7rem;padding-top:.35rem;border-top:3px solid var(--ink)}
.article h3{font-size:21px;line-height:1.55;margin:2.8rem 0 .85rem;padding-left:14px;border-left:4px solid var(--accent)}
.article strong{font-weight:800}
.article blockquote{margin:2.4rem 0;padding:4px 0 4px 22px;border-left:5px solid var(--accent);font-family:var(--serif);font-size:21px;line-height:1.8}
.article hr{border:0;border-top:1px solid var(--line);margin:4.2rem 0}
.article ul,.article ol{padding-left:1.35em;margin:1.2em 0 1.8em}
.article li{margin:.4em 0}
.article a{text-decoration-thickness:1px;text-underline-offset:3px}
.article a:hover{color:var(--accent)}
.table-wrap{max-width:100%;overflow-x:auto;margin:1.8rem 0 2.3rem;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}
.article table{width:100%;min-width:680px;border-collapse:collapse;font-size:13px;line-height:1.55;background:rgba(255,255,255,.27)}
.article th,.article td{padding:11px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
.article th{font-size:11px;letter-spacing:.06em;background:rgba(0,0,0,.035)}
.article tr:last-child td{border-bottom:0}
#sources{font-family:var(--sans);font-size:17px;letter-spacing:.08em;border-top:1px solid var(--ink);padding-top:20px}
#sources~p,#sources~ul{font-size:13px;line-height:1.75;color:#514d47}

.tip-trigger{display:inline;padding:0 1px;border:0;border-bottom:1px dashed var(--accent);background:transparent;color:inherit;cursor:pointer;text-align:inherit;line-height:inherit}
.tip-trigger::after{content:"?";display:inline-grid;place-items:center;width:13px;height:13px;margin-left:2px;border:1px solid var(--accent);border-radius:50%;color:var(--accent);font:700 9px/1 var(--sans);vertical-align:.28em}
.tip-trigger:hover,.tip-trigger:focus-visible{background:rgba(184,50,41,.08);outline:0}
.tip-trigger:focus-visible{box-shadow:0 0 0 2px var(--accent)}
.rail{position:sticky;top:88px}
.tip-card{border-top:3px solid var(--ink);border-bottom:1px solid var(--ink);padding:16px 0 18px}
.tip-kicker{margin:0 0 12px;color:var(--accent);font-size:10px;font-weight:900;letter-spacing:.16em}
.tip-card h2{margin:0 0 10px;font-family:var(--serif);font-size:24px;line-height:1.45}
.tip-summary{margin:0 0 14px;font-size:14px;line-height:1.85;color:#34312e}
.tip-meta{font-size:10px;color:var(--muted);letter-spacing:.05em;text-transform:uppercase}
.tip-hint{margin:18px 0 0;color:var(--muted);font-size:11px;line-height:1.65}

.article-actions{max-width:var(--article);margin:0 auto 0;display:flex;flex-wrap:wrap;gap:10px;padding:0 24px 46px}
.action-button{appearance:none;border:1px solid var(--ink);background:transparent;color:var(--ink);min-height:44px;padding:9px 15px;display:inline-flex;align-items:center;gap:8px;text-decoration:none;cursor:pointer;font-size:13px;font-weight:750}
.action-button:hover,.action-button:focus-visible{background:var(--ink);color:#fff;outline:none}
.action-button.liked{background:var(--accent);border-color:var(--accent);color:#fff}
.action-icon{font-size:16px;line-height:1}
.author{max-width:var(--article);margin:0 auto;padding:26px 24px 58px;border-top:1px solid var(--ink);font-size:13px;line-height:1.8;color:#45413c}
.author p{margin:0}.author strong{color:var(--ink)}

/* Right-side menu drawer: permanent article pattern for contents + dictionary. */
.menu-overlay{position:fixed;inset:0;z-index:80;background:rgba(0,0,0,.42);opacity:0;pointer-events:none;transition:opacity .18s ease}
.menu-overlay.open{opacity:1;pointer-events:auto}
.menu-drawer{position:absolute;top:0;right:0;width:min(470px,94vw);height:100%;background:var(--paper2);border-left:1px solid var(--ink);transform:translateX(100%);transition:transform .22s ease;display:flex;flex-direction:column}
.menu-overlay.open .menu-drawer{transform:translateX(0)}
.menu-head{height:58px;flex:0 0 auto;padding:0 18px 0 22px;border-bottom:1px solid var(--ink);display:flex;align-items:center;justify-content:space-between}
.menu-head strong{font-size:11px;letter-spacing:.14em}
.menu-close{width:34px;height:34px;border:1px solid var(--ink);background:transparent;cursor:pointer;font-size:22px;line-height:1}
.menu-close:hover,.menu-close:focus-visible{background:var(--ink);color:#fff;outline:none}
.menu-tabs{display:grid;grid-template-columns:1fr 1fr;border-bottom:1px solid var(--ink)}
.menu-tab{border:0;border-right:1px solid var(--ink);background:transparent;padding:13px 10px;cursor:pointer;font-size:11px;font-weight:850;letter-spacing:.1em}
.menu-tab:last-child{border-right:0}.menu-tab.active{background:var(--ink);color:#fff}
.menu-panel{display:none;overflow:auto;min-height:0;flex:1}.menu-panel.active{display:block}
.toc-list{list-style:none;margin:0;padding:0}
.toc-list li{border-bottom:1px solid var(--line)}
.toc-list a{display:grid;grid-template-columns:35px 1fr;gap:9px;padding:13px 22px;text-decoration:none;font-size:13px;line-height:1.55}
.toc-list a span{color:var(--accent);font-size:10px;font-weight:900;letter-spacing:.06em;padding-top:3px}
.toc-list a:hover,.toc-list a:focus-visible{background:rgba(0,0,0,.04);outline:none}
.index-tools{position:sticky;top:0;z-index:2;background:var(--paper2);padding:16px 18px;border-bottom:1px solid var(--ink)}
.index-search{width:100%;height:44px;border:1px solid var(--ink);background:#fff;padding:0 12px;border-radius:0;outline:none}
.index-search:focus{box-shadow:inset 0 -3px 0 var(--accent)}
.index-count{display:block;margin-top:7px;font-size:10px;color:var(--muted);letter-spacing:.08em}
.drawer-tip{margin:14px 18px 0;border:1px solid var(--ink);background:var(--paper);padding:14px}
.drawer-tip[hidden]{display:none}
.drawer-tip strong{display:block;font-family:var(--serif);font-size:20px;line-height:1.4;margin-bottom:7px}
.drawer-tip p{margin:0 0 8px;font-size:13px;line-height:1.75}
.drawer-tip small{color:var(--muted);font-size:10px}
.index-list{list-style:none;margin:0;padding:0}
.index-item{border-bottom:1px solid var(--line)}
.index-open{width:100%;border:0;background:transparent;padding:12px 18px;text-align:left;cursor:pointer;display:block}
.index-open:hover,.index-open:focus-visible{background:rgba(0,0,0,.04);outline:none}
.index-name{display:block;font-size:14px;font-weight:800;line-height:1.4}
.index-meta{display:block;margin-top:4px;font-size:9px;color:var(--muted);letter-spacing:.04em}

.tip-dialog{width:min(560px,calc(100vw - 28px));max-height:74vh;padding:0;border:1px solid var(--ink);border-radius:0;background:var(--paper2);color:var(--ink);box-shadow:0 24px 70px rgba(0,0,0,.25)}
.tip-dialog::backdrop{background:rgba(0,0,0,.48)}
.dialog-head{display:flex;align-items:center;justify-content:space-between;padding:12px 14px 12px 18px;border-bottom:1px solid var(--ink)}
.dialog-head p{margin:0;font-size:10px;color:var(--accent);font-weight:900;letter-spacing:.15em}
.dialog-head h2{margin:2px 0 0;font-family:var(--serif);font-size:23px}
.dialog-close{width:36px;height:36px;border:1px solid var(--ink);background:transparent;cursor:pointer;font-size:22px}
.dialog-close:hover,.dialog-close:focus-visible{background:var(--ink);color:#fff;outline:none}
.dialog-body{padding:18px}.dialog-body p{margin:0 0 12px;line-height:1.85}.dialog-meta{font-size:10px!important;color:var(--muted)}
.toast{position:fixed;left:50%;bottom:24px;z-index:120;transform:translate(-50%,20px);opacity:0;background:var(--ink);color:#fff;padding:8px 12px;font-size:12px;pointer-events:none;transition:.18s ease}.toast.show{opacity:1;transform:translate(-50%,0)}

@media(max-width:980px){
  .hero-inner{grid-template-columns:1fr}.hero-code{border-left:0;border-top:1px solid var(--line);padding:16px 0 0;display:flex;gap:16px;align-items:center}.hero-code strong{margin:0}
  .layout{grid-template-columns:minmax(0,1fr);max-width:800px;gap:0}.rail{display:none}.article{width:100%;max-width:var(--article);margin:auto}
  .article-actions,.author{max-width:792px}
}
@media(max-width:620px){
  body{font-size:16px;line-height:1.92}.sitebar-inner{padding:0 16px}.brand{font-size:10px}.menu-button{font-size:10px}
  .hero-inner{padding:44px 16px 40px;gap:30px}.hero h1{font-size:36px;line-height:1.27}.hero-deck{font-size:16px}.spoiler-inner{padding:9px 16px}
  .layout{padding:42px 16px 80px}.article h2{font-size:29px;margin-top:4.5rem}.article h3{font-size:19px}.article blockquote{font-size:18px;padding-left:16px}
  .article table{font-size:12px;min-width:650px}.article-actions{padding:0 16px 38px}.author{padding:22px 16px 48px}.action-button{flex:1 1 auto;justify-content:center}
  .menu-drawer{width:100vw}.menu-head{padding-left:16px}.toc-list a{padding-left:16px;padding-right:16px}.index-tools{padding:14px 16px}.drawer-tip{margin-left:16px;margin-right:16px}.index-open{padding-left:16px;padding-right:16px}
}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}
@media print{.sitebar,.spoiler-bar,.rail,.menu-overlay,.tip-dialog,.article-actions,.toast{display:none!important}.hero{border-bottom:0}.hero-inner{display:block;padding:20px 0}.layout{display:block;padding:0}.article{max-width:none}.tip-trigger{border:0;padding:0}.tip-trigger::after{content:""}body{background:#fff;font-size:11pt}.author{max-width:none;padding-left:0;padding-right:0}}
'''

js = r'''
(() => {
  const tips = JSON.parse(document.getElementById('tips-data').textContent);
  const cat = {series:'シリーズ',system:'遊び方',character:'人物',organization:'組織',technology:'技術',power:'能力',concept:'概念',place:'場所',ura:'裏サクセス',meta:'メタ'};
  const spoiler = {low:'軽度',medium:'中',high:'高',critical:'核心'};
  const byId = id => document.getElementById(id);

  const railName = byId('rail-tip-name');
  const railSummary = byId('rail-tip-summary');
  const railMeta = byId('rail-tip-meta');
  const dialog = byId('tip-dialog');
  const dName = byId('dialog-tip-name');
  const dSummary = byId('dialog-tip-summary');
  const dMeta = byId('dialog-tip-meta');
  const dClose = byId('dialog-close');
  let returnFocus = null;

  const tipMeta = t => `${cat[t.category] || t.category} · 初出 ${t.first} · SPOILER ${spoiler[t.spoiler] || t.spoiler}`;
  function renderRail(key){
    const t=tips[key]; if(!t) return;
    railName.textContent=t.name; railSummary.textContent=t.summary; railMeta.textContent=tipMeta(t);
  }
  function openTipDialog(key, source){
    const t=tips[key]; if(!t) return;
    returnFocus=source || null;
    dName.textContent=t.name; dSummary.textContent=t.summary; dMeta.textContent=tipMeta(t);
    if(typeof dialog.showModal==='function' && !dialog.open){ dialog.showModal(); dClose.focus(); }
  }
  document.addEventListener('click', e => {
    const btn=e.target.closest('.tip-trigger'); if(!btn) return;
    const isMobile=window.matchMedia('(max-width: 980px)').matches;
    renderRail(btn.dataset.tip);
    if(isMobile) openTipDialog(btn.dataset.tip, btn);
  });
  dClose.addEventListener('click',()=>dialog.close());
  dialog.addEventListener('close',()=>{ if(returnFocus) returnFocus.focus(); });

  // Drawer menu
  const overlay=byId('menu-overlay'), drawer=byId('menu-drawer'), menuOpen=byId('menu-open'), menuClose=byId('menu-close');
  let menuReturn=null;
  function openMenu(){ menuReturn=document.activeElement; overlay.classList.add('open'); overlay.setAttribute('aria-hidden','false'); menuOpen.setAttribute('aria-expanded','true'); document.body.style.overflow='hidden'; menuClose.focus(); }
  function closeMenu(){ overlay.classList.remove('open'); overlay.setAttribute('aria-hidden','true'); menuOpen.setAttribute('aria-expanded','false'); document.body.style.overflow=''; if(menuReturn) menuReturn.focus(); }
  menuOpen.addEventListener('click',openMenu); menuClose.addEventListener('click',closeMenu);
  overlay.addEventListener('click',e=>{ if(e.target===overlay) closeMenu(); });
  document.addEventListener('keydown',e=>{
    if(!overlay.classList.contains('open')) return;
    if(e.key==='Escape'){ closeMenu(); return; }
    if(e.key==='Tab'){
      const focusable=[...drawer.querySelectorAll('button:not([disabled]),a[href],input:not([disabled]),[tabindex]:not([tabindex="-1"])')].filter(el=>!el.hidden && el.offsetParent!==null);
      if(!focusable.length) return;
      const first=focusable[0], last=focusable[focusable.length-1];
      if(e.shiftKey && document.activeElement===first){ e.preventDefault(); last.focus(); }
      else if(!e.shiftKey && document.activeElement===last){ e.preventDefault(); first.focus(); }
    }
  });
  document.querySelectorAll('.toc-list a').forEach(a=>a.addEventListener('click',closeMenu));

  const tabs=[...document.querySelectorAll('.menu-tab')];
  const panels=[...document.querySelectorAll('.menu-panel')];
  tabs.forEach(tab=>tab.addEventListener('click',()=>{
    tabs.forEach(t=>{ const active=t===tab; t.classList.toggle('active',active); t.setAttribute('aria-selected',active?'true':'false'); });
    panels.forEach(p=>p.classList.toggle('active',p.id===tab.getAttribute('aria-controls')));
  }));

  // Dictionary search + in-drawer detail
  const search=byId('index-search'), count=byId('index-count'), items=[...document.querySelectorAll('.index-item')];
  const detail=byId('drawer-tip'), detailName=byId('drawer-tip-name'), detailText=byId('drawer-tip-text'), detailMeta=byId('drawer-tip-meta');
  function filter(){
    const q=search.value.trim().toLowerCase(); let n=0;
    items.forEach(li=>{ const hit=!q || li.dataset.search.toLowerCase().includes(q); li.hidden=!hit; if(hit)n++; });
    count.textContent=`${n} / ${items.length} TERMS`;
  }
  search.addEventListener('input',filter); filter();
  document.querySelectorAll('.index-open').forEach(btn=>btn.addEventListener('click',()=>{
    const t=tips[btn.dataset.tipIndex]; if(!t) return;
    detail.hidden=false; detailName.textContent=t.name; detailText.textContent=t.summary; detailMeta.textContent=tipMeta(t);
    detail.scrollIntoView({block:'nearest'});
  }));

  // Like button: deliberately no fake public count. This is only a local UI state until a backend is wired.
  const like=byId('like-button');
  const likeKey='yu-zora-pawapoke-like';
  try{ if(localStorage.getItem(likeKey)==='1'){ like.classList.add('liked'); like.setAttribute('aria-pressed','true'); like.querySelector('.action-label').textContent='好き済み'; } }catch(_e){}
  like.addEventListener('click',()=>{
    const next=!like.classList.contains('liked');
    like.classList.toggle('liked',next); like.setAttribute('aria-pressed',next?'true':'false'); like.querySelector('.action-label').textContent=next?'好き済み':'好き';
    try{ localStorage.setItem(likeKey,next?'1':'0'); }catch(_e){}
  });

  const share=byId('share-x');
  share.addEventListener('click',e=>{
    e.preventDefault();
    const u=`https://twitter.com/intent/tweet?text=${encodeURIComponent(document.title)}&url=${encodeURIComponent(location.href)}`;
    window.open(u,'_blank','noopener,noreferrer,width=720,height=520');
  });
  const toast=byId('toast');
  function showToast(msg){ toast.textContent=msg; toast.classList.add('show'); clearTimeout(showToast.t); showToast.t=setTimeout(()=>toast.classList.remove('show'),1800); }
  byId('copy-link').addEventListener('click',async()=>{
    try{ await navigator.clipboard.writeText(location.href); showToast('リンクをコピーしました'); }
    catch(_e){ showToast('リンクをコピーできませんでした'); }
  });
})();
'''

full = f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light">
<title>野球ゲームの彼女ルートに、世界史を隠すな。――パワポケの「二つの裏」 | YU-ZORA</title>
<meta name="description" content="『パワプロクンポケット』1〜14の彼女ルートや周回の奥に隠れた連続史と、もう一つのゲーム『裏サクセス』。パワプロ未経験者向けTips付きでたどる長編特集。">
<style>{css}</style>
</head>
<body>
<a class="skip-link" href="#main">本文へ移動</a>
<header class="sitebar"><div class="sitebar-inner"><span class="brand">YU-ZORA / LONGFORM FEATURE</span><button class="menu-button" id="menu-open" type="button" aria-haspopup="dialog" aria-controls="menu-drawer" aria-expanded="false">CONTENTS / INDEX <span class="menu-icon" aria-hidden="true"><span></span></span></button></div></header>
<section class="hero" aria-labelledby="page-title"><div class="hero-inner"><div>
<p class="eyebrow">BASEBALL GAME / HIDDEN WORLD HISTORY / URA SUCCESS</p>
<h1 id="page-title">野球ゲームの彼女ルートに、世界史を隠すな。<br>――パワポケの「二つの裏」</h1>
<p class="hero-deck">彼女ルートの奥にある1〜14の連続史と、メニューの裏側にある“もう一本のゲーム”。パワプロを知らない人でも迷子にならないTipsを添えて、二つの「裏」を同じ地図に置く。</p>
</div><div class="hero-code"><strong>01—14</strong><span>1999–2011<br>LONGFORM / SPOILER<br>{len(tips)} POCKET TIPS</span></div></div></section>
<div class="spoiler-bar"><div class="spoiler-inner"><strong>SPOILER WARNING</strong> — 『パワプロクンポケット』1〜14のシナリオ、彼女候補、真ルート、裏サクセスに触れます。</div></div>
<main id="main" class="layout">
<article class="article">{article_inner}</article>
<aside class="rail" aria-label="本文Tips"><div class="tip-card"><p class="tip-kicker">POCKET TIP / CLICK A DOTTED TERM</p><h2 id="rail-tip-name">赤い「?」の語を選ぶ</h2><p id="rail-tip-summary" class="tip-summary">パワプロもサクセスも知らない人向けの基本語から、人物・組織・技術まで。本文を離れずに補足します。</p><div id="rail-tip-meta" class="tip-meta" aria-live="polite">{len(tips)} TERMS LOADED</div><p class="tip-hint">用語をまとめて探したい場合は、右上の CONTENTS / INDEX から検索できます。</p></div></aside>
</main>
<section class="article-actions" aria-label="記事アクション">
<button class="action-button" id="like-button" type="button" aria-pressed="false"><span class="action-icon" aria-hidden="true">♥</span><span class="action-label">好き</span></button>
<a class="action-button" id="share-x" href="#"><span class="action-icon" aria-hidden="true">𝕏</span><span>Xで共有</span></a>
<button class="action-button" id="copy-link" type="button"><span class="action-icon" aria-hidden="true">↗</span><span>リンクをコピー</span></button>
</section>
<footer class="author">{author_html or '<p><strong>Author　夕空ユウ（@yuu_mintia）</strong><br>趣味で個人制作のブラウザゲームを公開している。パワポケ、とくに裏サクセスはゲーム制作の大きな原点の一つ。</p>'}</footer>

<div class="menu-overlay" id="menu-overlay" aria-hidden="true"><aside class="menu-drawer" id="menu-drawer" role="dialog" aria-modal="true" aria-label="記事メニュー">
<div class="menu-head"><strong>POCKET MENU</strong><button class="menu-close" id="menu-close" type="button" aria-label="メニューを閉じる">×</button></div>
<div class="menu-tabs" role="tablist"><button class="menu-tab active" id="tab-contents" type="button" role="tab" aria-selected="true" aria-controls="panel-contents">CONTENTS / 目次</button><button class="menu-tab" id="tab-index" type="button" role="tab" aria-selected="false" aria-controls="panel-index">INDEX / 用語</button></div>
<nav class="menu-panel active" id="panel-contents" role="tabpanel" aria-labelledby="tab-contents" aria-label="記事内目次"><ol class="toc-list">{toc_html}</ol></nav>
<section class="menu-panel" id="panel-index" role="tabpanel" aria-labelledby="tab-index" aria-label="用語索引"><div class="index-tools"><label><span class="sr-only">用語を検索</span><input class="index-search" id="index-search" type="search" placeholder="人物・用語・遊び方を検索" autocomplete="off"></label><output class="index-count" id="index-count" for="index-search"></output></div><div class="drawer-tip" id="drawer-tip" hidden><strong id="drawer-tip-name"></strong><p id="drawer-tip-text"></p><small id="drawer-tip-meta"></small></div><ul class="index-list">{index_html}</ul></section>
</aside></div>

<dialog class="tip-dialog" id="tip-dialog" aria-labelledby="dialog-tip-name"><div class="dialog-head"><div><p>POCKET TIP</p><h2 id="dialog-tip-name">Tips</h2></div><button id="dialog-close" class="dialog-close" type="button" aria-label="Tipsを閉じる">×</button></div><div class="dialog-body"><p id="dialog-tip-summary"></p><p id="dialog-tip-meta" class="dialog-meta"></p></div></dialog>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script type="application/json" id="tips-data">{tips_json}</script>
<script>{js}</script>
</body></html>'''

out = root / 'article/full.html'
out.write_text(full, encoding='utf-8')
print('wrote', out, 'bytes', len(full.encode('utf-8')), 'tips', len(tips), 'annotated', len(used_keys))

from pathlib import Path
import json,re,html
import mistune
from bs4 import BeautifulSoup, NavigableString, Tag

root=Path(__file__).resolve().parents[1]
md_text=(root/'article/full.md').read_text(encoding='utf-8')
tips=json.loads((root/'data/tips.json').read_text(encoding='utf-8'))

renderer=mistune.HTMLRenderer(escape=False)
md=mistune.create_markdown(renderer=renderer, plugins=['table','url'])
article_html=md(md_text)
soup=BeautifulSoup(article_html,'html.parser')

# The standalone page supplies its own hero title / spoiler bar. Remove the duplicated Markdown header block.
first_h1=soup.find('h1')
if first_h1:
    first_h1.decompose()
first_blockquote=soup.find('blockquote')
if first_blockquote and 'SPOILER WARNING' in first_blockquote.get_text(' ',strip=True):
    first_blockquote.decompose()

# Heading IDs and TOC
used=set(); toc=[]
def slug_heading(txt):
    t=txt.strip()
    m=re.match(r'^(\d{2})[\s　]+', t)
    if m: return f's{m.group(1)}'
    if t.upper()=='SOURCE NOTES': return 'sources'
    s=re.sub(r'[^a-zA-Z0-9ぁ-んァ-ヶ一-龠]+','-',t).strip('-').lower()
    return s or 'section'
for h in soup.find_all('h2'):
    sid=slug_heading(h.get_text(' ',strip=True)); base=sid; i=2
    while sid in used: sid=f'{base}-{i}'; i+=1
    used.add(sid); h['id']=sid; toc.append((sid,h.get_text(' ',strip=True)))

# Tips: exact display names + safe aliases used in prose.
aliases={v['name']:k for k,v in tips.items()}
aliases.update({
    'ジオット':'gio','ホンフー':'hongfu','6人組':'six','超能力':'esp','カタストロフ':'catastrophe',
    '一撃計画':'one_strike','ポケレンジャー':'pokerangers','ハタ人間':'hata','しあわせ島':'shiawase_island',
    '秘密結社編':'secret_society_ura','海洋冒険編':'marine_ura','札侍編':'fudasamurai',
})
# Longest aliases first, and only annotate a term once in the main article.
pattern=re.compile('|'.join(map(re.escape,sorted(aliases,key=len,reverse=True))))
used_keys=set()
skip_parents={'a','code','pre','script','style','button','h1','h2','h3'}
for node in list(soup.find_all(string=True)):
    if not isinstance(node,NavigableString) or not node.strip(): continue
    if node.parent and node.parent.name in skip_parents: continue
    text=str(node); pos=0; pieces=[]; changed=False
    for m in pattern.finditer(text):
        key=aliases[m.group(0)]
        if key in used_keys: continue
        pieces.append(NavigableString(text[pos:m.start()]))
        b=soup.new_tag('button', attrs={
            'type':'button','class':'tip-trigger','data-tip':key,
            'aria-label':f"{tips[key]['name']}のTipsを開く"
        })
        b.string=m.group(0)
        pieces.append(b); pos=m.end(); used_keys.add(key); changed=True
    if changed:
        pieces.append(NavigableString(text[pos:]))
        for p in reversed(pieces): node.insert_after(p)
        node.extract()

article_inner=str(soup)

toc_html=''.join(f'<li><a href="#{html.escape(sid)}">{html.escape(title)}</a></li>' for sid,title in toc if sid!='sources')

category_labels={'character':'人物','organization':'組織','technology':'技術','power':'能力','concept':'概念','place':'場所','ura':'裏サクセス','meta':'メタ'}
spoiler_labels={'low':'軽度','medium':'中','high':'高','critical':'核心'}
index_items=[]
for key,v in tips.items():
    index_items.append(f'''<li class="index-item" data-search="{html.escape(v['name'])} {html.escape(v['summary'])}" data-category="{html.escape(v['category'])}">
<button type="button" class="index-open" data-tip="{html.escape(key)}">
<span class="index-name">{html.escape(v['name'])}</span>
<span class="index-meta">{html.escape(category_labels.get(v['category'],v['category']))} · 初出 {html.escape(v['first'])} · SPOILER {html.escape(spoiler_labels.get(v['spoiler'],v['spoiler']))}</span>
</button></li>''')
index_html='\n'.join(index_items)
tips_json=json.dumps(tips,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')

css=r'''
:root{
  --paper:#f1ede3;--paper-2:#faf8f2;--ink:#171717;--muted:#68645e;--line:#b8b1a4;
  --accent:#b42f25;--accent-2:#173f54;--dark:#111;--max:1180px;--body:720px;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Kaku Gothic ProN","Yu Gothic",Meiryo,sans-serif;
  --serif:"Yu Mincho","Hiragino Mincho ProN","Noto Serif JP",serif;
}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:17px;line-height:1.92}
a{color:inherit;text-decoration-thickness:1px;text-underline-offset:.18em}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}.skip-link{position:absolute;left:8px;top:-80px;background:#fff;color:#000;padding:12px 16px;z-index:999}.skip-link:focus{top:8px}
.topline{border-bottom:1px solid var(--ink);background:var(--paper-2)}.topline-inner{max-width:var(--max);margin:auto;min-height:54px;padding:0 22px;display:flex;align-items:center;justify-content:space-between;gap:20px;font-size:12px;letter-spacing:.12em;text-transform:uppercase}.brand{font-weight:800}.top-meta{color:var(--muted)}
.hero{border-bottom:1px solid var(--ink)}.hero-inner{max-width:var(--max);margin:auto;padding:66px 22px 54px;display:grid;grid-template-columns:minmax(0,1fr) 210px;gap:50px;align-items:end}.eyebrow{font-size:12px;letter-spacing:.16em;font-weight:800;color:var(--accent);margin:0 0 24px}.hero h1{font-family:var(--serif);font-size:clamp(34px,5vw,68px);line-height:1.22;letter-spacing:-.03em;margin:0;max-width:900px}.hero-deck{margin:26px 0 0;font-size:18px;max-width:760px;color:#333}.hero-code{border-left:1px solid var(--ink);padding-left:18px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12px;line-height:1.65;color:var(--muted)}.hero-code strong{display:block;color:var(--ink);font-size:28px;line-height:1.1;margin-bottom:8px}.spoiler-bar{background:var(--dark);color:#fff}.spoiler-inner{max-width:var(--max);margin:auto;padding:14px 22px;font-size:13px;letter-spacing:.04em}
.mobile-toc{display:none;max-width:var(--max);margin:0 auto;border-bottom:1px solid var(--line);padding:16px 22px}.mobile-toc summary{font-weight:800;cursor:pointer}.mobile-toc ol{columns:2;padding-left:22px}.mobile-toc a{font-size:14px}
.layout{max-width:var(--max);margin:0 auto;padding:56px 22px 100px;display:grid;grid-template-columns:minmax(0,var(--body)) minmax(260px,330px);gap:80px;align-items:start}.article{min-width:0}.article p{margin:0 0 1.45em}.article h2{font-family:var(--serif);font-size:clamp(28px,3vw,40px);line-height:1.4;margin:5.2rem 0 1.7rem;padding-top:1.2rem;border-top:1px solid var(--ink);letter-spacing:-.02em}.article h2:first-of-type{margin-top:0}.article h3{font-size:20px;line-height:1.55;margin:3rem 0 1rem;color:var(--accent-2)}.article strong{font-weight:800}.article blockquote{margin:2.2rem 0;padding:1rem 0 1rem 22px;border-left:5px solid var(--accent);font-family:var(--serif);font-size:21px;line-height:1.8}.article blockquote p:last-child{margin-bottom:0}.article hr{border:0;border-top:1px solid var(--line);margin:4rem 0}.article ul{padding-left:1.3em}.article li{margin:.55em 0}.article table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.65;margin:1.8rem 0 2.6rem}.article th,.article td{padding:11px 10px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}.article th{border-top:2px solid var(--ink);font-size:12px;letter-spacing:.04em;background:rgba(255,255,255,.28)}.article td:first-child,.article th:first-child{white-space:nowrap;font-weight:800}.article a[href^="http"]{word-break:break-all}.article #sources{font-family:var(--sans);font-size:20px;letter-spacing:.08em}.article #sources~p,.article #sources~ul{font-size:13px;color:var(--muted)}
.tip-trigger{display:inline;padding:0 .06em;border:0;border-bottom:1px dotted var(--accent);background:transparent;color:inherit;font:inherit;font-weight:inherit;cursor:pointer;text-decoration:none}.tip-trigger::after{content:"↗";font-size:.62em;color:var(--accent);vertical-align:.55em;margin-left:.14em}.tip-trigger:hover,.tip-trigger:focus-visible{background:#fff2c8;outline:2px solid transparent;border-bottom-style:solid}.tip-trigger:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.rail{position:sticky;top:20px;align-self:start}.rail-block{border-top:3px solid var(--ink);border-bottom:1px solid var(--ink);padding:14px 0 18px;margin-bottom:28px}.rail-kicker{margin:0 0 16px;font:800 11px/1 var(--sans);letter-spacing:.18em;color:var(--accent)}.rail h2{font-family:var(--serif);font-size:23px;line-height:1.4;margin:0 0 12px}.rail p{font-size:13px;line-height:1.7;color:var(--muted);margin:0 0 10px}.rail .tip-summary{font-size:14px;color:var(--ink)}.rail-meta{display:flex;gap:8px;flex-wrap:wrap;font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}.rail nav{border-top:1px solid var(--line);padding-top:16px}.rail nav h2{font:800 11px/1 var(--sans);letter-spacing:.18em;margin:0 0 12px}.rail ol{margin:0;padding:0;list-style:none;max-height:48vh;overflow:auto}.rail li{border-top:1px solid var(--line)}.rail li:first-child{border-top:0}.rail a{display:block;padding:8px 0;font-size:12px;line-height:1.45;text-decoration:none}.rail a:hover,.rail a:focus-visible{color:var(--accent);text-decoration:underline}.rail-index-link{display:block;border-top:1px solid var(--ink);margin-top:16px;padding-top:12px;font-size:12px;font-weight:800;letter-spacing:.05em}
.pocket-index{background:var(--paper-2);border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}.pocket-inner{max-width:var(--max);margin:auto;padding:55px 22px 75px}.pocket-head{display:grid;grid-template-columns:1fr minmax(240px,360px);gap:40px;align-items:end;border-bottom:2px solid var(--ink);padding-bottom:22px}.pocket-head h2{font-family:var(--serif);font-size:clamp(30px,4vw,48px);margin:0;line-height:1.25}.pocket-head p{margin:0;color:var(--muted);font-size:14px}.index-controls{display:grid;grid-template-columns:1fr auto;gap:10px;margin:24px 0}.index-search{width:100%;min-height:46px;border:1px solid var(--ink);background:#fff;padding:10px 12px;font:inherit;border-radius:0}.index-count{display:flex;align-items:center;border:1px solid var(--ink);padding:0 12px;font:700 12px/1 var(--sans);letter-spacing:.08em}.index-list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr}.index-item{border-bottom:1px solid var(--line)}.index-item:nth-child(odd){border-right:1px solid var(--line)}.index-open{width:100%;min-height:70px;text-align:left;border:0;background:transparent;padding:12px 14px;cursor:pointer}.index-open:hover,.index-open:focus-visible{background:#f0e4d1;outline:2px solid var(--accent);outline-offset:-2px}.index-name{display:block;font-weight:800;font-size:15px}.index-meta{display:block;margin-top:4px;font-size:10px;color:var(--muted);letter-spacing:.04em}.index-item[hidden]{display:none}
.footer{max-width:var(--max);margin:auto;padding:30px 22px 50px;display:flex;justify-content:space-between;gap:20px;font-size:11px;color:var(--muted);letter-spacing:.05em}
.tip-dialog{width:min(92vw,560px);border:1px solid var(--ink);border-radius:0;padding:0;background:var(--paper-2);color:var(--ink);box-shadow:10px 10px 0 rgba(0,0,0,.22)}.tip-dialog::backdrop{background:rgba(0,0,0,.62)}.dialog-head{display:flex;justify-content:space-between;align-items:start;gap:16px;border-bottom:1px solid var(--ink);padding:16px 18px}.dialog-head p{margin:0 0 5px;font-size:10px;letter-spacing:.14em;color:var(--accent);font-weight:800}.dialog-head h2{font-family:var(--serif);margin:0;font-size:26px;line-height:1.3}.dialog-close{min-width:44px;min-height:44px;border:1px solid var(--ink);background:transparent;font-size:22px;cursor:pointer}.dialog-close:hover,.dialog-close:focus-visible{background:var(--ink);color:#fff;outline:2px solid var(--accent);outline-offset:2px}.dialog-body{padding:18px}.dialog-body p{margin:0 0 14px;line-height:1.8}.dialog-meta{font-size:12px;color:var(--muted)}
@media(max-width:980px){.hero-inner{grid-template-columns:1fr}.hero-code{border-left:0;border-top:1px solid var(--line);padding:16px 0 0;display:flex;gap:16px;align-items:center}.hero-code strong{margin:0}.layout{grid-template-columns:minmax(0,1fr);gap:0;max-width:800px}.rail{display:none}.mobile-toc{display:block}.article{width:100%;max-width:720px;margin:auto}.pocket-inner{max-width:800px}.pocket-head{grid-template-columns:1fr}.index-list{grid-template-columns:1fr}.index-item:nth-child(odd){border-right:0}}
@media(max-width:620px){body{font-size:16px;line-height:1.9}.topline-inner{padding:0 16px}.top-meta{display:none}.hero-inner{padding:42px 16px 38px}.hero h1{font-size:34px;line-height:1.28}.hero-deck{font-size:16px}.spoiler-inner,.mobile-toc{padding-left:16px;padding-right:16px}.mobile-toc ol{columns:1}.layout{padding:38px 16px 70px}.article h2{font-size:27px;margin-top:4.2rem}.article h3{font-size:19px}.article blockquote{font-size:18px;padding-left:16px}.article table{font-size:12px;min-width:640px}.article table{display:table}.article .table-wrap{width:100%;max-width:100%;min-width:0;overflow-x:auto;overscroll-behavior-inline:contain}.pocket-inner{padding:42px 16px 60px}.pocket-head h2{font-size:32px}.index-controls{grid-template-columns:1fr}.index-count{min-height:42px}.footer{padding-left:16px;padding-right:16px;display:block}.footer span{display:block;margin-top:5px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}
@media print{.topline,.spoiler-bar,.mobile-toc,.rail,.pocket-index,.tip-dialog,.footer{display:none!important}.hero{border-bottom:0}.hero-inner{display:block;padding:20px 0}.layout{display:block;padding:0}.article{max-width:none}.tip-trigger{border:0;padding:0}.tip-trigger::after{content:""}body{background:#fff;font-size:11pt}.article h2{break-after:avoid}.article table{font-size:9pt}}
'''

# Fix mobile table overflow by wrapping tables in article content.
article_soup=BeautifulSoup(article_inner,'html.parser')
for table in article_soup.find_all('table'):
    wrap=article_soup.new_tag('div',attrs={'class':'table-wrap','role':'region','aria-label':'横スクロールできる表','tabindex':'0'})
    table.wrap(wrap)
article_inner=str(article_soup)

js=r'''
(() => {
  const tips = JSON.parse(document.getElementById('tips-data').textContent);
  const cat = {character:'人物',organization:'組織',technology:'技術',power:'能力',concept:'概念',place:'場所',ura:'裏サクセス',meta:'メタ'};
  const spoiler = {low:'軽度',medium:'中',high:'高',critical:'核心'};
  const railName = document.getElementById('rail-tip-name');
  const railSummary = document.getElementById('rail-tip-summary');
  const railMeta = document.getElementById('rail-tip-meta');
  const dialog = document.getElementById('tip-dialog');
  const dName = document.getElementById('dialog-tip-name');
  const dSummary = document.getElementById('dialog-tip-summary');
  const dMeta = document.getElementById('dialog-tip-meta');
  const close = document.getElementById('dialog-close');
  let returnFocus = null;

  function renderTip(key, openDialog=false){
    const t=tips[key]; if(!t) return;
    const meta=`${cat[t.category] || t.category} · 初出 ${t.first} · SPOILER ${spoiler[t.spoiler] || t.spoiler}`;
    railName.textContent=t.name; railSummary.textContent=t.summary; railMeta.textContent=meta;
    dName.textContent=t.name; dSummary.textContent=t.summary; dMeta.textContent=meta;
    if(openDialog && typeof dialog.showModal==='function' && !dialog.open){ dialog.showModal(); close.focus(); }
  }
  document.addEventListener('click', e => {
    const btn=e.target.closest('[data-tip]'); if(!btn) return;
    const isMobile=window.matchMedia('(max-width: 980px)').matches;
    returnFocus=btn; renderTip(btn.dataset.tip,isMobile);
  });
  close.addEventListener('click',()=>dialog.close());
  dialog.addEventListener('close',()=>{ if(returnFocus) returnFocus.focus(); });
  dialog.addEventListener('click',e=>{ if(e.target===dialog){ const r=dialog.getBoundingClientRect(); const inside=e.clientX>=r.left&&e.clientX<=r.right&&e.clientY>=r.top&&e.clientY<=r.bottom; if(!inside) dialog.close(); }});

  const search=document.getElementById('index-search');
  const count=document.getElementById('index-count');
  const items=[...document.querySelectorAll('.index-item')];
  function filter(){
    const q=search.value.trim().toLowerCase(); let n=0;
    items.forEach(li=>{ const hit=!q || li.dataset.search.toLowerCase().includes(q); li.hidden=!hit; if(hit)n++; });
    count.textContent=`${n} / ${items.length}`;
  }
  search.addEventListener('input',filter); filter();

  const current = location.hash && document.querySelector(location.hash);
  if(current) setTimeout(()=>current.scrollIntoView(),0);
})();
'''

full=f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light">
<title>野球ゲームの彼女ルートに、世界史を隠すな。――パワポケの「二つの裏」 | YU-ZORA</title>
<meta name="description" content="『パワプロクンポケット』1〜14の彼女ルートや周回の奥に隠れた連続史と、もう一つのゲーム『裏サクセス』。パワポケの二つの『裏』を、初見向けTips付きでたどる長編特集。">
<style>{css}</style>
</head>
<body>
<a class="skip-link" href="#main">本文へ移動</a>
<header class="topline"><div class="topline-inner"><span class="brand">YU-ZORA / LONGFORM FEATURE</span><span class="top-meta">PAWAPOKE RESEARCH · 001</span></div></header>
<section class="hero" aria-labelledby="page-title"><div class="hero-inner"><div>
<p class="eyebrow">BASEBALL GAME / HIDDEN WORLD HISTORY / URA SUCCESS</p>
<h1 id="page-title">野球ゲームの彼女ルートに、世界史を隠すな。<br>――パワポケの「二つの裏」</h1>
<p class="hero-deck">彼女ルートの奥にある1〜14の連続史と、メニューの裏側にある“もう一本のゲーム”。二つの「裏」を同じ地図に置く。</p>
</div><div class="hero-code"><strong>01—14</strong><span>1999–2011<br>LONGFORM / SPOILER<br>65 POCKET TIPS</span></div></div></section>
<div class="spoiler-bar"><div class="spoiler-inner"><strong>SPOILER WARNING</strong> — 『パワプロクンポケット』1〜14のシナリオ、彼女候補、真ルート、裏サクセスに触れます。</div></div>
<details class="mobile-toc"><summary>CONTENTS / 目次</summary><ol>{toc_html}</ol></details>
<main id="main" class="layout">
<article class="article">{article_inner}</article>
<aside class="rail" aria-label="人物・用語Tips">
<div class="rail-block"><p class="rail-kicker">POCKET TIP / CLICK A TERM</p><h2 id="rail-tip-name">本文の赤い点線語を選択</h2><p id="rail-tip-summary" class="tip-summary">人物・組織・技術を、本文から離れずに補足します。初見の人だけ開けばOKです。</p><div id="rail-tip-meta" class="rail-meta" aria-live="polite">65 terms loaded</div></div>
<nav aria-label="記事内目次"><h2>CONTENTS</h2><ol>{toc_html}</ol><a class="rail-index-link" href="#pocket-index">POCKET INDEX — 65語一覧 ↓</a></nav>
</aside>
</main>
<section class="pocket-index" id="pocket-index" aria-labelledby="pocket-index-title"><div class="pocket-inner">
<div class="pocket-head"><h2 id="pocket-index-title">POCKET INDEX<br>人物・組織・用語 65</h2><p>本文で触れ切れなかった語も含む、調査用の小さな索引。クリックすると補足を表示します。ネタバレ度は「核心」が最も高い表記です。</p></div>
<div class="index-controls"><label><span class="sr-only">用語検索</span><input class="index-search" id="index-search" type="search" placeholder="人物・組織・用語を検索" autocomplete="off"></label><output class="index-count" id="index-count" for="index-search">65 / 65</output></div>
<ul class="index-list">{index_html}</ul>
</div></section>
<footer class="footer"><span>YU-ZORA / PAWAPOKE LONGFORM</span><span>Research notes are maintained separately in this repository.</span></footer>
<dialog class="tip-dialog" id="tip-dialog" aria-labelledby="dialog-tip-name"><div class="dialog-head"><div><p>POCKET TIP</p><h2 id="dialog-tip-name">Tips</h2></div><button id="dialog-close" class="dialog-close" type="button" aria-label="Tipsを閉じる">×</button></div><div class="dialog-body"><p id="dialog-tip-summary"></p><p id="dialog-tip-meta" class="dialog-meta"></p></div></dialog>
<script type="application/json" id="tips-data">{tips_json}</script>
<script>{js}</script>
</body></html>'''
(root/'article/full.html').write_text(full,encoding='utf-8')
print('wrote',root/'article/full.html','bytes',len(full.encode('utf-8')),'annotated tips',len(used_keys),sorted(used_keys))

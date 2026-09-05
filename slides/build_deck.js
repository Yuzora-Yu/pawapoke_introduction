const pptxgen = require('pptxgenjs');
const path = require('path');
const {
  imageSizingCrop,
  safeOuterShadow,
  warnIfSlideHasOverlaps,
  warnIfSlideElementsOutOfBounds,
} = require('/home/oai/skills/slides/pptxgenjs_helpers');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5
pptx.author = 'YU-ZORA / ChatGPT';
pptx.company = 'YU-ZORA';
pptx.subject = '身内向け・入門版 パワポケ布教スライド';
pptx.title = 'パワポケ布教スライド — 身内向け・入門版';
pptx.lang = 'ja-JP';
pptx.theme = {
  headFontFace: 'Noto Sans CJK JP',
  bodyFontFace: 'Noto Sans CJK JP',
  lang: 'ja-JP',
};
pptx.defineSlideMaster({
  title: 'PAWAPOKE',
  background: { color: 'EAF7FF' },
  objects: [],
  slideNumber: { x: 12.62, y: 7.08, w: 0.34, h: 0.2, color: '6A7892', fontFace: 'Noto Sans CJK JP', fontSize: 9, align: 'right' },
});

const ROOT = path.resolve(__dirname, '..');
const A = (name) => path.join(ROOT, 'assets', 'pawapoke_fukyo', name);
const OUT = path.join(__dirname, 'pawapoke_fukyo_intro.pptx');

const C = {
  navy: '0C1D48',
  navy2: '132B67',
  blue: '259BFF',
  cyan: '88D8FF',
  sky: 'EAF7FF',
  sky2: 'D9F0FF',
  white: 'FFFFFF',
  ink: '102247',
  muted: '5D6C87',
  yellow: 'FFE13A',
  yellow2: 'FFF49C',
  red: 'FF2B25',
  coral: 'FF6A55',
  purple: '6C3BCB',
  green: '38B77A',
  line: 'B8DDF4',
  soft: 'F7FBFF',
  black: '111111',
};

const FONT = 'Noto Sans CJK JP';
const SHADOW = safeOuterShadow('000000', 0.17, 45, 2, 1);

function addBg(slide, opts = {}) {
  const color = opts.color || C.sky;
  slide.background = { color };
  // subtle game-board dots
  const dots = [
    [0.25,0.25,0.18],[0.6,0.55,0.09],[12.4,0.55,0.12],[12.8,1.0,0.07],
    [0.35,6.55,0.1],[0.8,6.95,0.06],[12.3,6.45,0.08],[11.9,6.9,0.14],
  ];
  dots.forEach(([x,y,r], i) => slide.addShape(pptx.ShapeType.ellipse, {
    x,y,w:r,h:r, fill:{color:i%2?C.cyan:C.white, transparency:i%2?55:35}, line:{color:C.cyan, transparency:100}
  }));
}

function addHeader(slide, num, title, kicker) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x:0.42, y:0.28, w:12.5, h:0.78, rectRadius:0.06,
    fill:{color:C.navy}, line:{color:C.cyan, width:2}, shadow:SHADOW
  });
  slide.addShape(pptx.ShapeType.roundRect, {
    x:0.58, y:0.43, w:0.62, h:0.48,
    fill:{color:C.white}, line:{color:C.red, width:2}
  });
  slide.addText('P', { x:0.58,y:0.37,w:0.62,h:0.56, fontFace:FONT,fontSize:25,bold:true,color:C.red,align:'center',valign:'mid',margin:0 });
  slide.addText(String(num).padStart(2,'0'), { x:1.28,y:0.41,w:0.55,h:0.26,fontFace:FONT,fontSize:11,bold:true,color:C.yellow,margin:0 });
  slide.addText(title, { x:1.78,y:0.38,w:9.75,h:0.42,fontFace:FONT,fontSize:23,bold:true,color:C.white,margin:0,breakLine:false,fit:'shrink' });
  if (kicker) slide.addText(kicker, { x:1.8,y:0.77,w:9.7,h:0.18,fontFace:FONT,fontSize:8.8,color:'BBD9FF',margin:0,charSpacing:0.2 });
}

function addFooter(slide, label) {
  slide.addShape(pptx.ShapeType.line, { x:0.55,y:7.08,w:12.05,h:0, line:{color:C.line,width:1} });
  if (label) slide.addText(label, { x:0.58,y:7.13,w:5.5,h:0.18,fontFace:FONT,fontSize:8,color:C.muted,margin:0 });
}

function addCard(slide, x, y, w, h, opts = {}) {
  const fill = opts.fill || C.white;
  const line = opts.line || C.line;
  slide.addShape(pptx.ShapeType.roundRect, {
    x,y,w,h, rectRadius:0.07,
    fill:{color:fill, transparency:opts.transparency || 0},
    line:{color:line, width:opts.lineWidth || 1.4},
    shadow: opts.shadow === false ? undefined : SHADOW,
  });
}

function addPill(slide, text, x, y, w, opts={}) {
  slide.addShape(pptx.ShapeType.roundRect, { x,y,w,h:0.34, rectRadius:0.12, fill:{color:opts.fill||C.navy}, line:{color:opts.line||opts.fill||C.navy, width:1} });
  slide.addText(text, { x:x+0.03,y:y+0.04,w:w-0.06,h:0.24,fontFace:FONT,fontSize:opts.fontSize||10,bold:opts.bold!==false,color:opts.color||C.white,align:'center',margin:0,fit:'shrink' });
}

function addArrow(slide, x1, y1, x2, y2, color=C.red, width=2.3) {
  slide.addShape(pptx.ShapeType.line, { x:x1, y:y1, w:x2-x1, h:y2-y1, line:{color,width,beginArrowType:'none',endArrowType:'triangle'} });
}

function addLock(slide, x, y, scale=1, color=C.navy) {
  slide.addShape(pptx.ShapeType.arc, { x:x+0.07*scale,y:y,w:0.32*scale,h:0.34*scale, adjustPoint:0.35, rotate:0, fill:{color:C.sky,transparency:100}, line:{color,width:2} });
  slide.addShape(pptx.ShapeType.roundRect, { x,y:y+0.2*scale,w:0.46*scale,h:0.38*scale,rectRadius:0.05,fill:{color},line:{color} });
  slide.addShape(pptx.ShapeType.ellipse, { x:x+0.19*scale,y:y+0.31*scale,w:0.08*scale,h:0.08*scale,fill:{color:C.yellow},line:{color:C.yellow} });
}

function addSlideTag(slide, text, x, y, fill=C.yellow, color=C.navy) {
  slide.addShape(pptx.ShapeType.rect, { x,y,w:1.55,h:0.32,rotate:-2,fill:{color:fill},line:{color:fill} });
  slide.addText(text, { x:x+0.06,y:y+0.04,w:1.43,h:0.2,fontFace:FONT,fontSize:9,bold:true,color,align:'center',margin:0,fit:'shrink' });
}

// 1 — cover
{
  const s = pptx.addSlide('PAWAPOKE');
  s.addImage({ path:A('cover.png'), ...imageSizingCrop(A('cover.png'), 0, 0, 13.333, 7.5) });
  s.addShape(pptx.ShapeType.roundRect, { x:10.55,y:6.83,w:2.35,h:0.38,fill:{color:C.navy,transparency:4},line:{color:C.cyan,width:1.1} });
  s.addText('※ 1〜14のネタバレあり', { x:10.67,y:6.92,w:2.12,h:0.16,fontFace:FONT,fontSize:9.4,bold:true,color:C.white,align:'center',margin:0 });
}

// 2 — what is pawapoke
{
  const s = pptx.addSlide('PAWAPOKE'); addBg(s); addHeader(s,2,'そもそもパワポケって何？','まずは30秒で共通認識を作る');
  s.addText('1999', { x:0.72,y:1.46,w:1.05,h:0.55,fontFace:FONT,fontSize:31,bold:true,color:C.red,margin:0 });
  addArrow(s,1.8,1.72,4.55,1.72,C.navy,2.6);
  s.addText('2011', { x:4.75,y:1.46,w:1.05,h:0.55,fontFace:FONT,fontSize:31,bold:true,color:C.navy,margin:0 });
  addPill(s,'ナンバリング 1 → 14',1.77,2.02,3.28,{fill:C.navy});
  s.addImage({ path:A('character.png'), ...imageSizingCrop(A('character.png'), 9.55, 1.36, 3.35, 5.3) });
  s.addShape(pptx.ShapeType.roundRect,{x:9.7,y:5.85,w:2.75,h:0.58,fill:{color:C.navy,transparency:2},line:{color:C.white,width:1.1}});
  s.addText('主人公は変わる。\n世界だけは続く。',{x:9.83,y:5.96,w:2.49,h:0.35,fontFace:FONT,fontSize:13.5,bold:true,color:C.white,align:'center',margin:0,breakLine:false,fit:'shrink'});

  const cards = [
    {x:0.72,title:'パワプロ派生の携帯機シリーズ',body:'Game Boy → GBA → DSへ。\n「野球選手を作る」が共通の出口。',accent:C.blue},
    {x:3.72,title:'サクセス＝育成＋物語',body:'練習・試合・仲間・彼女・選択肢。\n失敗したら、もう一周。',accent:C.red},
    {x:6.72,title:'通称「野球バラエティ」',body:'恋愛 / SF / 企業抗争 / ホラー / RPG…\n毎年なにかが足されていく。',accent:C.purple},
  ];
  cards.forEach(c=>{addCard(s,c.x,2.72,2.62,2.65);s.addShape(pptx.ShapeType.rect,{x:c.x,y:2.72,w:2.62,h:0.12,fill:{color:c.accent},line:{color:c.accent}});s.addText(c.title,{x:c.x+0.18,y:3.02,w:2.26,h:0.62,fontFace:FONT,fontSize:15,bold:true,color:C.ink,margin:0.02,fit:'shrink'});s.addText(c.body,{x:c.x+0.18,y:3.85,w:2.26,h:1.08,fontFace:FONT,fontSize:11.3,color:C.muted,margin:0.02,breakLine:false,fit:'shrink'});});
  s.addText('「野球選手を作る」という最終目的だけ残して、途中に何を入れていいかの判定がどんどん壊れていった。',{x:0.72,y:5.7,w:8.45,h:0.58,fontFace:FONT,fontSize:16.2,bold:true,color:C.navy,margin:0.02,fit:'shrink'});
  addFooter(s,'身内向け・入門版');
}

// 3 — core weirdness
{
  const s = pptx.addSlide('PAWAPOKE'); addBg(s,{color:'E8F6FF'}); addHeader(s,3,'このシリーズ、まず何が変なのか','「鬱ゲー」だけでは説明不足');
  s.addImage({ path:A('character.png'), ...imageSizingCrop(A('character.png'), 8.45, 1.22, 4.65, 5.95) });
  s.addShape(pptx.ShapeType.roundRect,{x:0.74,y:1.42,w:7.55,h:2.25,fill:{color:C.white},line:{color:C.navy,width:2.2},shadow:SHADOW});
  s.addText('彼女候補を攻略していたら、\n巨大企業の政変と人体改造と\n時間犯罪の話になった。',{x:1.06,y:1.78,w:6.92,h:1.54,fontFace:FONT,fontSize:24.5,bold:true,color:C.navy,margin:0,breakLine:false,fit:'shrink'});
  s.addShape(pptx.ShapeType.chevron,{x:7.95,y:2.18,w:0.62,h:0.7,fill:{color:C.white},line:{color:C.navy,width:2.2},rotate:0});
  addSlideTag(s,'さっきまで高校野球',0.9,3.92,C.yellow,C.navy);
  const pills=[
    ['野球',C.navy],['恋愛',C.red],['企業抗争',C.purple],['サイボーグ',C.blue],['超能力',C.green],['時間移動',C.coral]
  ];
  let px=0.9; let py=4.48;
  pills.forEach(([t,col],i)=>{const w=[0.9,0.9,1.32,1.48,1.12,1.18][i];addPill(s,t,px,py,w,{fill:col});px+=w+0.18; if(px>7.6){px=0.9;py+=0.55;}});
  s.addShape(pptx.ShapeType.roundRect,{x:0.88,y:5.72,w:7.25,h:0.78,fill:{color:C.navy},line:{color:C.cyan,width:1.2}});
  s.addText('「彼女がひどい目に遭う野球ゲーム」だけでは、まだ半分。',{x:1.12,y:5.94,w:6.78,h:0.33,fontFace:FONT,fontSize:17.2,bold:true,color:C.white,align:'center',margin:0,fit:'shrink'});
  addFooter(s,'入口は「何が起きているの？」でOK');
}

// 4 — two undersides
{
  const s = pptx.addSlide('PAWAPOKE'); addBg(s); addHeader(s,4,'パワポケには「二つの裏」がある','この2枚看板だけ覚えれば、今日の目的は達成');
  addCard(s,0.72,1.42,5.78,4.98,{fill:'F8FCFF',line:C.blue,lineWidth:2});
  addCard(s,6.84,1.42,5.78,4.98,{fill:'FFF9F3',line:C.red,lineWidth:2});
  s.addImage({path:A('map.png'),...imageSizingCrop(A('map.png'),0.95,1.68,2.25,1.28)});
  s.addImage({path:A('vortex.png'),...imageSizingCrop(A('vortex.png'),9.92,1.68,2.22,1.28)});
  addPill(s,'① 物語の「裏」',3.44,1.72,2.35,{fill:C.blue});
  addPill(s,'② ゲームの「裏」',7.12,1.72,2.45,{fill:C.red});
  s.addText('表サクセスの奥に\n隠れた連続史',{x:1.05,y:3.17,w:5.1,h:0.92,fontFace:FONT,fontSize:24,bold:true,color:C.navy,align:'center',margin:0,fit:'shrink'});
  s.addText('彼女ルート・周回・追加イベント\n↓\n組織史 / 技術史 / 世界の危機',{x:1.15,y:4.22,w:4.9,h:1.18,fontFace:FONT,fontSize:14,color:C.muted,align:'center',margin:0.02,fit:'shrink'});
  s.addText('文字どおりの\n「裏サクセス」',{x:7.17,y:3.17,w:5.1,h:0.92,fontFace:FONT,fontSize:24,bold:true,color:C.navy,align:'center',margin:0,fit:'shrink'});
  s.addText('忍者 / 宇宙 / ハタ人間 / 秘密結社 / 大海原\n↓\nほぼ別ジャンルのゲーム',{x:7.27,y:4.22,w:4.9,h:1.18,fontFace:FONT,fontSize:14,color:C.muted,align:'center',margin:0.02,fit:'shrink'});
  s.addShape(pptx.ShapeType.roundRect,{x:3.72,y:5.75,w:5.9,h:0.78,fill:{color:C.navy},line:{color:C.yellow,width:1.6}});
  s.addText('どっちも、野球ゲームの中にある。',{x:4.02,y:5.98,w:5.3,h:0.28,fontFace:FONT,fontSize:17.8,bold:true,color:C.yellow,align:'center',margin:0});
  addFooter(s,'片方は「隠された世界史」、片方は「ほとんど別ゲーム」');
}

// 5 — 8 hide 11 lock
{
  const s = pptx.addSlide('PAWAPOKE'); addBg(s,{color:'EFF9FF'}); addHeader(s,5,'「8」から隠す。「11」から施錠する。','後期パワポケの情報設計が、ここで一段変わる');
  s.addShape(pptx.ShapeType.line,{x:1.05,y:3.38,w:11.15,h:0,line:{color:C.navy,width:5,transparency:15}});
  const pts=[
    {n:'8',x:1.1,c:C.blue,t:'深いルートに\n過去作接続を置く',lock:false},
    {n:'10',x:3.15,c:C.blue,t:'しあわせ島→親切高校\n後期史の発射台',lock:false},
    {n:'11',x:5.22,c:C.red,t:'追加イベント・\n登録選手数などが鍵',lock:true},
    {n:'12',x:7.28,c:C.red,t:'「事件の背景を\n知りたい」が解禁',lock:true},
    {n:'13',x:9.33,c:C.red,t:'周回・他ルート履歴で\n情報が増える',lock:true},
    {n:'14',x:11.38,c:C.red,t:'真ルート / トゥルーに\n事前条件',lock:true},
  ];
  pts.forEach(p=>{
    s.addShape(pptx.ShapeType.ellipse,{x:p.x,y:3.03,w:0.72,h:0.72,fill:{color:p.c},line:{color:C.white,width:2},shadow:SHADOW});
    s.addText(p.n,{x:p.x,y:3.12,w:0.72,h:0.32,fontFace:FONT,fontSize:18,bold:true,color:C.white,align:'center',margin:0});
    addCard(s,p.x-0.45,1.53,1.62,1.18,{fill:C.white,line:p.c,lineWidth:1.5});
    s.addText(p.t,{x:p.x-0.32,y:1.78,w:1.36,h:0.68,fontFace:FONT,fontSize:10.8,bold:true,color:C.ink,align:'center',margin:0.01,fit:'shrink'});
    if(p.lock) addLock(s,p.x+0.12,4.05,0.92,C.red);
    else addPill(s,'HIDE',p.x-0.02,4.13,0.92,{fill:C.blue,fontSize:9});
  });
  s.addShape(pptx.ShapeType.roundRect,{x:1.03,y:5.35,w:11.2,h:0.94,fill:{color:C.navy},line:{color:C.cyan,width:1.4},shadow:SHADOW});
  s.addText('設定が深い、だけではない。　設定を読むこと自体が攻略になっている。',{x:1.35,y:5.66,w:10.55,h:0.32,fontFace:FONT,fontSize:18.2,bold:true,color:C.white,align:'center',margin:0,fit:'shrink'});
  addFooter(s,'中心コピー：『8』から奥へ隠した。『11』から施錠した。');
}

// 6 — long-distance passes
{
  const s = pptx.addSlide('PAWAPOKE'); addBg(s); addHeader(s,6,'パワポケ名物：数作飛んで返ってくる','「昔のイベント」が「歴史」に変わる瞬間');
  s.addImage({path:A('map.png'),...imageSizingCrop(A('map.png'),10.65,1.28,2.05,1.14)});
  const rows=[
    {y:1.52,a:'3',at:'寺岡薫',b:'12',bt:'デウエス',note:'9作品越しの長距離パス',col:C.red},
    {y:2.73,a:'6',at:'しあわせ島',b:'10',bt:'親切高校',note:'裏の人体実験が表へ戻る',col:C.blue},
    {y:3.94,a:'7',at:'ヒーロー側',b:'9',bt:'反対側の視点',note:'同じ対立構造を反転して描く',col:C.purple},
    {y:5.15,a:'14 表',at:'トゥルー',b:'14 裏',bt:'「ジオット」',note:'表の履歴が裏イベントの鍵',col:C.green},
  ];
  rows.forEach((r,i)=>{
    addCard(s,0.78,r.y,11.55,0.94,{fill:i%2?'F8FCFF':'FFFFFF',line:r.col,lineWidth:1.4});
    addPill(s,r.a,1.04,r.y+0.29,0.72,{fill:r.col});
    s.addText(r.at,{x:1.95,y:r.y+0.22,w:2.25,h:0.38,fontFace:FONT,fontSize:15.2,bold:true,color:C.ink,margin:0,fit:'shrink'});
    addArrow(s,4.35,r.y+0.48,6.25,r.y+0.48,r.col,2.8);
    addPill(s,r.b,6.48,r.y+0.29,0.82,{fill:r.col});
    s.addText(r.bt,{x:7.48,y:r.y+0.22,w:2.18,h:0.38,fontFace:FONT,fontSize:15.2,bold:true,color:C.ink,margin:0,fit:'shrink'});
    addPill(s,r.note,9.6,r.y+0.29,2.43,{fill:C.navy,fontSize:9.7});
  });
  s.addText('こういう線を一本見つけると、急に「過去作」ではなく「世界史」になる。',{x:1.02,y:6.28,w:10.85,h:0.44,fontFace:FONT,fontSize:16.4,bold:true,color:C.navy,align:'center',margin:0,fit:'shrink'});
  addFooter(s,'※ 7→9は構造的接続を強く言える一方、「9主人公＝レッド」は断定しない');
}

// 7 — heroines as windows
{
  const s = pptx.addSlide('PAWAPOKE'); addBg(s,{color:'FFF9F5'}); addHeader(s,7,'彼女候補は「世界史を見る窓」になる','後期では、恋愛ルートが本筋の収納場所になることがある');
  const cards=[
    {x:0.78,y:1.48,n:'神条紫杏',sub:'10 → 11',body:'高校の彼女候補から、\n巨大組織の合併・再編史へ。',c:C.red},
    {x:3.85,y:1.48,n:'パカーディ・ハイネン',sub:'12',body:'有名な結末だけでなく、\n復讐・カエサリオン・ジオットへ。',c:C.purple},
    {x:0.78,y:3.62,n:'木村冴花',sub:'13',body:'彼女ルート＋周回履歴で、\n黒幕側の事情が増えていく。',c:C.blue},
    {x:3.85,y:3.62,n:'天月紗矢香',sub:'14',body:'事前クリアとトゥルーの先で、\nカタストロフへ到達。',c:C.green},
  ];
  cards.forEach(c=>{addCard(s,c.x,c.y,2.72,1.72,{fill:C.white,line:c.c,lineWidth:2});addPill(s,c.sub,c.x+1.92,c.y+0.14,0.58,{fill:c.c,fontSize:9});s.addText(c.n,{x:c.x+0.18,y:c.y+0.2,w:1.7,h:0.42,fontFace:FONT,fontSize:15.2,bold:true,color:C.ink,margin:0,fit:'shrink'});s.addText(c.body,{x:c.x+0.18,y:c.y+0.78,w:2.36,h:0.7,fontFace:FONT,fontSize:11.2,color:C.muted,margin:0.01,fit:'shrink'});});
  addCard(s,7.05,1.62,5.18,3.94,{fill:C.navy,line:C.cyan,lineWidth:1.6});
  s.addText('「彼女ルート」\n＝ 恋愛サブイベント？',{x:7.42,y:1.98,w:4.42,h:0.9,fontFace:FONT,fontSize:24,bold:true,color:C.white,align:'center',margin:0,fit:'shrink'});
  s.addText('↓',{x:9.25,y:2.88,w:0.8,h:0.4,fontFace:FONT,fontSize:28,bold:true,color:C.yellow,align:'center',margin:0});
  s.addText('ときどき逆。',{x:7.7,y:3.32,w:3.85,h:0.45,fontFace:FONT,fontSize:23,bold:true,color:C.yellow,align:'center',margin:0});
  s.addText('本筋を表から見えなくするための\n「収納場所」になっている。',{x:7.52,y:4.05,w:4.24,h:0.9,fontFace:FONT,fontSize:17.2,bold:true,color:C.white,align:'center',margin:0.02,fit:'shrink'});
  s.addShape(pptx.ShapeType.roundRect,{x:7.62,y:5.74,w:4.12,h:0.62,fill:{color:C.yellow},line:{color:C.navy,width:1.3},rotate:-1.5});
  s.addText('好きなキャラを追う → 世界の続きが気になる',{x:7.82,y:5.94,w:3.72,h:0.25,fontFace:FONT,fontSize:12,bold:true,color:C.navy,align:'center',margin:0,fit:'shrink'});
  addFooter(s,'個人的には紫杏・野崎維織が特に好き（※維織はこのスライドの構造説明枠とは別）');
}

// 8 — ura success table
{
  const s = pptx.addSlide('PAWAPOKE'); addBg(s,{color:'EEF8FF'}); addHeader(s,8,'もう一つの裏：裏サクセスは、ほぼ別ゲーム','「野球選手を作るおまけ」の説明が途中から苦しくなる');
  s.addImage({path:A('field.png'),...imageSizingCrop(A('field.png'),0,5.4,13.333,2.1)});
  s.addShape(pptx.ShapeType.rect,{x:0,y:5.4,w:13.333,h:2.1,fill:{color:C.navy,transparency:60},line:{color:C.navy,transparency:100}});
  const items=[
    ['2','戦争編','戦時下で生存'],['5','忍者戦国編','国取りSLG'],['7','大正冒険奇譚','クエスト冒険'],['9','宇宙編','冒険・交易RPG'],
    ['11','ハタ人間','サバイバルRPG'],['12','秘密結社','探索・戦闘RPG'],['13','海洋冒険','航海・海戦'],['14','札侍','カードバトル']
  ];
  items.forEach((it,i)=>{
    const col=i%4,row=Math.floor(i/4); const x=0.75+col*3.06,y=1.5+row*1.82;
    addCard(s,x,y,2.62,1.42,{fill:C.white,line:i>=4?C.red:C.blue,lineWidth:1.5});
    addPill(s,it[0],x+0.16,y+0.15,0.55,{fill:i>=4?C.red:C.blue,fontSize:10});
    s.addText(it[1],{x:x+0.83,y:y+0.16,w:1.55,h:0.32,fontFace:FONT,fontSize:13.6,bold:true,color:C.ink,margin:0,fit:'shrink'});
    s.addText(it[2],{x:x+0.18,y:y+0.76,w:2.25,h:0.34,fontFace:FONT,fontSize:10.7,color:C.muted,align:'center',margin:0,fit:'shrink'});
  });
  s.addShape(pptx.ShapeType.roundRect,{x:2.1,y:5.72,w:9.15,h:0.78,fill:{color:C.navy,transparency:4},line:{color:C.yellow,width:1.3}});
  s.addText('「……野球は？」　→　最後に選手ができるので、野球です。たぶん。',{x:2.45,y:5.95,w:8.45,h:0.29,fontFace:FONT,fontSize:17,bold:true,color:C.white,align:'center',margin:0,fit:'shrink'});
  addFooter(s,'野球が帰る場所としてあったから、裏は忍者にも宇宙にも海にも行けた。');
}

// 9 — evolution 5 7 11 12 13
{
  const s = pptx.addSlide('PAWAPOKE'); addBg(s); addHeader(s,9,'特に好きな5本で見る「進化」','5 → 7 → 11 → 12 → 13');
  const steps=[
    {x:0.75,y:4.65,w:2.05,h:1.35,n:'5',t:'忍者戦国編',b:'国取り\nシミュレーション',c:C.blue},
    {x:2.95,y:4.0,w:2.05,h:1.55,n:'7',t:'大正冒険奇譚',b:'依頼を拾う\nクエスト型冒険',c:C.blue},
    {x:5.15,y:3.25,w:2.05,h:1.75,n:'11',t:'怪奇！ハタ人間',b:'探索・装備・仲間編成\nサバイバルRPG',c:C.red},
    {x:7.35,y:2.42,w:2.05,h:1.92,n:'12',t:'秘密結社編',b:'11の戦闘 ＋ 7の\nクエスト構造',c:C.red},
    {x:9.55,y:1.52,w:2.65,h:2.15,n:'13',t:'海洋冒険編',b:'航海・交易・海戦へ拡張\n裏サクセスの集大成',c:C.red},
  ];
  steps.forEach((st,i)=>{
    addCard(s,st.x,st.y,st.w,st.h,{fill:C.white,line:st.c,lineWidth:i>=2?2:1.5});
    addPill(s,st.n,st.x+0.14,st.y+0.13,0.55,{fill:st.c});
    s.addText(st.t,{x:st.x+0.78,y:st.y+0.15,w:st.w-0.9,h:0.34,fontFace:FONT,fontSize:12.8,bold:true,color:C.ink,margin:0,fit:'shrink'});
    s.addText(st.b,{x:st.x+0.16,y:st.y+0.67,w:st.w-0.32,h:st.h-0.83,fontFace:FONT,fontSize:11.2,color:C.muted,align:'center',valign:'mid',margin:0.01,fit:'shrink'});
    if(i<steps.length-1) addArrow(s,st.x+st.w,st.y+st.h/2,steps[i+1].x-0.12,steps[i+1].y+steps[i+1].h/2,C.navy,2.2);
  });
  addPill(s,'キャラ面で特に好き',5.05,5.35,2.1,{fill:C.navy,fontSize:9.5});
  addPill(s,'シナリオ・システム面で特に好き',7.35,5.17,2.5,{fill:C.navy,fontSize:8.8});
  s.addShape(pptx.ShapeType.roundRect,{x:10.04,y:4.58,w:2.32,h:0.88,fill:{color:C.yellow},line:{color:C.navy,width:1.4},shadow:SHADOW,rotate:-2});
  s.addText('「あ、これパワポケだった。」\nと我に返るやつ。',{x:10.21,y:4.78,w:1.98,h:0.46,fontFace:FONT,fontSize:11.7,bold:true,color:C.navy,align:'center',margin:0,fit:'shrink'});
  addFooter(s,'裏サクセスだけでも、一本のゲームデザイン進化史として見られる。');
}

// 10 — recommend 13
{
  const s = pptx.addSlide('PAWAPOKE'); addBg(s,{color:'FFF8E8'}); addHeader(s,10,'一本だけ勧めるなら、私は「13」を選ぶ','シリーズ物を13から勧めるのか？ → その通り。でも強い。');
  s.addImage({path:A('map.png'),...imageSizingCrop(A('map.png'),0.78,1.55,4.2,2.5)});
  s.addShape(pptx.ShapeType.roundRect,{x:0.78,y:1.55,w:4.2,h:2.5,fill:{color:C.white,transparency:100},line:{color:C.white,width:6},shadow:SHADOW,rotate:-1.2});
  s.addText('13',{x:0.98,y:3.7,w:2.0,h:1.0,fontFace:FONT,fontSize:60,bold:true,color:C.red,margin:0});
  s.addText('最高傑作と呼べる一本',{x:2.18,y:4.08,w:2.85,h:0.5,fontFace:FONT,fontSize:18,bold:true,color:C.navy,margin:0,fit:'shrink'});
  const rs=[
    {y:1.55,label:'表',title:'逆襲球児編',body:'王道の高校野球。\n一度落ちた主人公が、仲間と上がり直す。',c:C.blue},
    {y:3.02,label:'裏',title:'海洋冒険編',body:'航海・交易・海戦。\n11〜12で積み上げたRPG要素の集大成。',c:C.red},
    {y:4.49,label:'深部',title:'周回で世界史が増える',body:'彼女ルート・アルバム・過去の履歴で\n黒幕側の情報が深くなる。',c:C.purple},
  ];
  rs.forEach(r=>{addCard(s,5.35,r.y,6.65,1.16,{fill:C.white,line:r.c,lineWidth:1.5});addPill(s,r.label,5.58,r.y+0.38,0.78,{fill:r.c,fontSize:10});s.addText(r.title,{x:6.58,y:r.y+0.17,w:2.28,h:0.35,fontFace:FONT,fontSize:15.6,bold:true,color:C.ink,margin:0,fit:'shrink'});s.addText(r.body,{x:8.88,y:r.y+0.16,w:2.8,h:0.67,fontFace:FONT,fontSize:10.5,color:C.muted,margin:0.01,fit:'shrink'});});
  s.addShape(pptx.ShapeType.roundRect,{x:1.0,y:5.22,w:3.78,h:1.02,fill:{color:C.navy},line:{color:C.yellow,width:1.5},shadow:SHADOW});
  s.addText('初めてアルバムを\nフルコンプリートした作品。',{x:1.28,y:5.48,w:3.22,h:0.47,fontFace:FONT,fontSize:15.2,bold:true,color:C.white,align:'center',margin:0,fit:'shrink'});
  addFooter(s,'一般的な根拠：表・裏とも完成度が高く、開発側も裏を集大成的と振り返っている。');
}

// 11 — entry routes
{
  const s = pptx.addSlide('PAWAPOKE'); addBg(s); addHeader(s,11,'初見なら、どこから入る？','全部理解してから遊ぶ必要はない');
  const cols=[
    {x:0.78,c:C.red,tag:'まず1本',title:'13から',body:'表は王道高校野球。\n裏は大航海RPG。\n「パワポケって何？」を一作で浴びる。'},
    {x:4.43,c:C.blue,tag:'歴史を追う',title:'1 → 14',body:'古い作品から順に。\n主人公は変わるのに、世界が歳を取る感覚が一番分かる。'},
    {x:8.08,c:C.purple,tag:'RPG好き',title:'11裏 → 12裏 → 13裏',body:'探索・装備・仲間編成から、\nクエスト融合、航海・海戦へ。\n裏サクセスの進化だけ追う。'},
  ];
  cols.forEach((c,i)=>{
    addCard(s,c.x,1.63,3.17,3.65,{fill:C.white,line:c.c,lineWidth:2});
    addPill(s,c.tag,c.x+0.26,1.9,1.15,{fill:c.c,fontSize:9.7});
    s.addText(c.title,{x:c.x+0.25,y:2.48,w:2.66,h:0.72,fontFace:FONT,fontSize:25,bold:true,color:C.navy,align:'center',margin:0,fit:'shrink'});
    s.addText(c.body,{x:c.x+0.32,y:3.48,w:2.52,h:1.18,fontFace:FONT,fontSize:12.1,color:C.muted,align:'center',margin:0.01,fit:'shrink'});
    s.addText(['★','→','⚔'][i],{x:c.x+1.12,y:4.72,w:0.92,h:0.38,fontFace:FONT,fontSize:18,bold:true,color:c.c,align:'center',margin:0});
  });
  s.addShape(pptx.ShapeType.roundRect,{x:1.5,y:5.72,w:10.32,h:0.82,fill:{color:C.navy},line:{color:C.cyan,width:1.4},shadow:SHADOW});
  s.addText('正解ルートはない。「なんだこれ？」が出たら、もう入口には立っている。',{x:1.88,y:5.99,w:9.56,h:0.29,fontFace:FONT,fontSize:17.6,bold:true,color:C.white,align:'center',margin:0,fit:'shrink'});
  addFooter(s,'手元にある作品から始めても大丈夫。分からない固有名詞は、あとから戻ればいい。');
}

// 12 — close
{
  const s = pptx.addSlide('PAWAPOKE');
  s.addImage({path:A('character.png'),...imageSizingCrop(A('character.png'),0,0,13.333,7.5)});
  s.addShape(pptx.ShapeType.rect,{x:0,y:0,w:13.333,h:7.5,fill:{color:C.navy,transparency:30},line:{color:C.navy,transparency:100}});
  s.addShape(pptx.ShapeType.roundRect,{x:0.72,y:0.7,w:7.32,h:4.18,fill:{color:C.white,transparency:6},line:{color:C.white,width:2},shadow:SHADOW});
  s.addText('その認識、\n半分は正しい。\n半分がとんでもなく足りない。',{x:1.14,y:1.17,w:6.5,h:2.25,fontFace:FONT,fontSize:31,bold:true,color:C.navy,margin:0,fit:'shrink'});
  s.addText('「彼女がひどい目に遭う野球ゲーム」は入口にすぎない。\n奥には、世界史と、もう一本のゲームが埋まっている。',{x:1.16,y:3.7,w:6.45,h:0.88,fontFace:FONT,fontSize:15.2,bold:true,color:C.ink,margin:0.01,fit:'shrink'});
  s.addShape(pptx.ShapeType.roundRect,{x:0.9,y:5.46,w:6.82,h:0.94,fill:{color:C.navy,transparency:3},line:{color:C.yellow,width:1.6}});
  s.addText('彼女のバッドエンド集だけ見て帰らないで。',{x:1.2,y:5.76,w:6.22,h:0.31,fontFace:FONT,fontSize:17.3,bold:true,color:C.yellow,align:'center',margin:0,fit:'shrink'});
  addPill(s,'FINISH',11.12,6.58,1.2,{fill:C.red,fontSize:10.5});
  s.addText('身内向け・入門版',{x:9.23,y:6.7,w:1.62,h:0.22,fontFace:FONT,fontSize:9,bold:true,color:C.white,align:'right',margin:0});
}

// Basic layout checks.
for (const [idx, slide] of pptx._slides.entries()) {
  try {
    warnIfSlideElementsOutOfBounds(slide, pptx);
    // Overlap warnings are informative; intentional image overlays may still be reported.
    warnIfSlideHasOverlaps(slide, pptx);
  } catch (e) {
    console.warn(`layout check slide ${idx+1}:`, e.message);
  }
}

pptx.writeFile({ fileName: OUT });
console.log(`Wrote ${OUT}`);

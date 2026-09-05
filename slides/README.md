# slides — 身内向け・入門版PowerPoint

成果物：

- `pawapoke_fukyo_intro.pptx` — 16:9、12枚、編集可能なPowerPoint
- `build_deck.js` — PptxGenJSによる生成元
- `montage.png` — 全体確認用プレビュー

## 目的

パワポケ未経験〜うろ覚えの身内へ、記事の中心命題を10分前後で布教する入門版。
設定資料集ではなく、まず「何が変なシリーズなのか」「なぜ彼女ルートに世界史が出るのか」「裏サクセスがどれだけ別ゲームなのか」が伝わることを優先する。

## 現在の12枚

1. 表紙
2. そもそもパワポケって何？
3. このシリーズ、まず何が変なのか
4. パワポケには「二つの裏」がある
5. 「8」から隠す。「11」から施錠する。
6. 数作飛んで返ってくる長距離伏線
7. 彼女候補は「世界史を見る窓」になる
8. 裏サクセスは、ほぼ別ゲーム
9. 5→7→11→12→13で見る裏サクセスの進化
10. 一本だけ勧めるなら「13」
11. 初見なら、どこから入る？
12. 締め

## ビジュアル

ユーザー提供のキービジュアルを `assets/pawapoke_fukyo/cover.png` に置き、同画像から必要部分を切り出した派生素材を同フォルダに置いている。
ネット上のゲーム画面・立ち絵は追加していない。

## 再生成

リポジトリ直下で：

```bash
node slides/build_deck.js
```

出力：`slides/pawapoke_fukyo_intro.pptx`

レイアウトQA：

```bash
python /home/oai/skills/slides/container_tools/slides_test.py slides/pawapoke_fukyo_intro.pptx
```

## 内容面の正本

事実・表記・断言強度はスライド内で独自に増やさず、以下に従う。

- `article/full.md`
- `AI_HANDOFF.md`
- `research/sources/factcheck.md`
- `AGENTS.md`

特に「8から隠す／11から施錠」「9主人公＝レッドを断定しない」「一撃計画と14のカタストロフを同一視しない」「正史彼女を一人に固定しない」は崩さない。

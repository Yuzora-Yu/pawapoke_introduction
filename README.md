# pawapoke_introduction

『パワプロクンポケット』シリーズの布教記事と、そのための調査資料庫。

## 採用タイトル
> **野球ゲームの彼女ルートに、世界史を隠すな。――パワポケの「二つの裏」**

## 中心命題
パワポケには二つの「裏」がある。

1. **表サクセスの深部に隠された連続史**
2. **文字どおりの裏サクセス**

さらに後半作品では、連続史が彼女ルートだけでなく、周回・追加イベント・真ルートの**ゲーム条件そのもの**に隠される。

> **パワポケの裏社会史は、シナリオ上隠れているだけではない。システム上も鍵がかけられている。**

## Git運用
- リポジトリには常に最新版だけを置く。
- `old/`、`v2/`、日付付きresearch packを作らない。
- 訂正は上書きし、過去はGit履歴へ任せる。

## 入口
- **次回AIの引継ぎ：`AI_HANDOFF.md`**
- 現在の判断：`PROJECT.md`
- AI作業ルール：`AGENTS.md`
- 調査全体の地図：`RESEARCH_MAP.md`
- 完全版本文：`article/full.md`
- Tips付き完全版HTML：`article/full.html`
- note版：`article/note.md`
- 身内向け・入門版PowerPoint：`slides/pawapoke_fukyo_intro.pptx`
- スライド生成元：`slides/build_deck.js`
- ファクトチェック：`research/sources/factcheck.md`

## HTML更新

```bash
python article/build_full_html.py
```

`article/full.md` と `data/tips.json` を反映して `article/full.html` を上書き生成する。

## 身内向けPowerPoint更新

```bash
node slides/build_deck.js
```

`article/full.md` と現在の調査判断を要約した、16:9・12枚の入門用スライド。
表紙および主要ビジュアルは `assets/pawapoke_fukyo/cover.png` を起点に構成する。

## 最重要ルール
- **パカーディ・ハイネン**。
- 「6人の未来人」と書かない。基本は **未来から来たミスターKが組織した「6人組」**。
- 「正史彼女」を一人に固定しない。
- 旧ジャジメント / ツナミ / 再改称後ジャジメントを時系列上区別。
- 一撃計画とジオットのカタストロフを同一視しない。
- パワポケ考察Wikiは重要参考先として使うが、非公式資料として確度を分ける。

## 筆者側の軸
筆者にとって『13』は初めてアルバムをフルコンプリートした思い出の作品で、表・裏とも非常に好きな一本。
またパワポケ、とくに裏サクセスは自身のゲーム制作の大きな原点の一つ。

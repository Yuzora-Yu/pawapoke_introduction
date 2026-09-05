# article

公開文章の作業領域。

調査事実は `research/`、表示用語辞書は `data/tips.json` に置き、このディレクトリには読者へ見せる文章・構成・HTML生成物を置く。

## 現在の正本

- `full.md` — **自サイト完全版の本文正本**
- `note.md` — note向け入口版
- `full.html` — Tips付き完全版HTML。`full.md` と `data/tips.json` から生成

## HTML生成

```bash
python article/build_full_html.py
```

開発用依存はルート `requirements-dev.txt`。

`full.html` は単一ファイルで、CSS / JS / Tips JSONを内包する。

現在：

- `data/tips.json`：110語
- 本文中：69語をクリックTips化（本文変更で増減可）
- PC：右側 sticky Tips
- スマホ：Tips dialog
- 右上：`CONTENTS / INDEX` drawer
  - 記事内目次
  - 全110語の検索可能な索引
- 下部：好き / X共有 / リンクコピー
- 最終末尾：短いAuthor表記のみ
- 画像素材なし
- YU-ZORA統合前の独立ページとして閲覧可能

## 補助資料

- `outline.md` — 採用構成
- `fragments.md` — 使える文章パーツ
- `ui-notes.md` — UI設計
- `author-note.md` — 筆者紹介の最小化ルール / 『13』の個人的体験
- `related/` — 派生記事計画

## 運用

`draft-v1.md`、`preview-v2.html`、日付付きコピーのような旧稿は作らない。

本文修正は `full.md` を上書きし、HTMLを再生成する。改稿履歴はGitで管理する。

# Web Design Rules — mandatory

本ファイルは、ユーザー提供の **Web Design Director** スキルをこのリポジトリで運用するための要点。
HTML、CSS、JavaScript、記事ページ、Tips UI、公開サイトの新規作成・改修時は必ず従う。

## Central concept

実装ごとに中心コンセプトを1文で決める。
現記事の第一候補：

> **「インディーゲーム雑誌の長文特集」と「ファンによる調査資料庫」が同じ紙面に共存する。**

見た目を先にカード部品へ分解せず、この一文から文字、罫線、索引、注釈、Tips、余白、色を決める。

## Workflow

1. 既存HTML/CSS/JS、リポジトリ、素材、参考URLを確認。
2. 目的、主要読者、主要行動、情報階層を確認。
3. central conceptを固定。
4. 少数のdesign tokensを定義。
5. semantic HTMLを作る。
6. content needsからresponsive CSSを設計。
7. navigation/state理解に必要なinteractionだけを追加。
8. accessibility / performance / deployabilityを確認。
9. link / anchor / relative path / local-vs-hostedを検証。
10. 完成ファイルを納品。

## Visual direction

Prefer:
- 限定されたpalette
- display/bodyの役割が明確なtype system
- title / index / body / metadataの強いhierarchy
- 意味のある非対称
- 罫線、番号、索引、注釈、スタンプ等の反復motif
- 実プロジェクト素材
- 内容に固有のcomponent

Avoid default AI patterns:
- 紫青gradient
- glassmorphism
- 同型rounded cardの大量配置
- pill label乱用
- decorative blobs
- vague marketing hero
- 意味のないicon / shadow / glow
- 不要なanimation
- 全section中央揃え

## Long-form Japanese typography

- 本文は概ね35〜45字/行。
- line-heightは概ね1.7〜2.0。
- displayとbodyの書体役割を分ける。
- レトロ表現のためだけに日本語本文すべてをmonospaceにしない。

## Accessibility

- semantic landmarksを使う。
- skip linkを用意する。
- visible keyboard focus。
- touch targetは概ね44px以上。
- image altを適切に設定。
- 色だけでstateを伝えない。
- `prefers-reduced-motion`を尊重。
- native HTMLで足りるところに不要なARIAを足さない。

人物Tips/モーダルはkeyboardでも開閉可能にし、focus管理とEscape closeを実装する。

## Responsive QA

最低限おおよそ以下で確認：
- 320px
- 768px
- wide desktop

確認事項：
- horizontal overflowなし
- navigationがtouch/keyboardで使える
- 長い日本語見出しが破綻しない
- sticky要素がanchor destinationを隠さない
- Tipsが本文を潰さない

## Deployment QA

- `file://` とHTTP serverの差を認識する。
- relative asset pathとanchorを検証する。
- GitHub Pages / Cloudflare Pages等のターゲット環境で成立する構成にする。
- ユーザーのプロジェクトについて未確認の文言を発明しない。


## Long-form navigation pattern

長文記事の共通骨格として以下を優先する。

- 右上固定の `CONTENTS / INDEX` から drawer を開く。
- CONTENTS＝記事内目次。
- INDEX＝検索可能な人物・用語・基本語辞書。
- PCのその場Tipsは右rail。モバイルはdialog。
- 記事末に巨大な辞書一覧を置かない。
- 記事下部に共有 / 好き等のアクションをまとめる。
- Authorは最終末尾に小さく置き、本文を自己宣伝で終わらせない。

この情報設計はパワポケ記事固有ではなく、YU-ZORAの今後の長文記事にも流用する。

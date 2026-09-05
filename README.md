# pawapoke_introduction

『パワプロクンポケット』シリーズの布教記事を、調査・構成・執筆まで一貫して管理するリポジトリ。

## 採用タイトル

> **野球ゲームの彼女ルートに、世界史を隠すな。――パワポケの「二つの裏」**

## 記事の中心命題

パワポケには二つの「裏」がある。

1. **表サクセスの深部に隠された連続史**
   - プロペラ団
   - オオガミ
   - 旧ジャジメント
   - ツナミ
   - 再改称後のジャジメント
   - 「6人組」
   - 一撃計画
   - ジオット
   - カタストロフ

2. **文字どおりの裏サクセス**
   - 特に『5』『7』『11』『12』『13』を、ゲームデザインの進化史として読む。

入口には彼女候補の強烈なエピソードを使うが、
「彼女がひどい目に遭う鬱ゲー」の紹介だけでは終わらせない。

---

## Git運用

このリポジトリでは **常に最新版だけを置く**。

原則として以下を作らない。

- `research_pack_YYYYMMDD/`
- `old/`
- `backup/`
- `v1/`, `v2/`

過去の状態はGit履歴に任せ、設定や事実を訂正したら現在のファイルを上書きする。
誤情報を「旧版参考」として横に残さない。

---

## 構成

```text
.
├─ README.md
├─ PROJECT.md
├─ AGENTS.md
├─ article/
│  ├─ README.md
│  ├─ outline.md
│  └─ fragments.md
├─ research/
│  ├─ README.md
│  ├─ canon/
│  │  ├─ hidden-continuity-design.md
│  │  ├─ overview.md
│  │  ├─ organizations.md
│  │  ├─ six-person-group.md
│  │  ├─ evidence-11-14.md
│  │  └─ catastrophe.md
│  ├─ heroine/
│  │  └─ hooks.md
│  ├─ release/
│  │  └─ chronology.md
│  ├─ ura-success/
│  │  └─ evolution-5-7-11-12-13.md
│  └─ sources/
│     ├─ policy.md
│     ├─ index.md
│     ├─ official-guides.md
│     ├─ factcheck.md
│     └─ uncertainties.md
└─ assets/
   ├─ README.md
   └─ diagrams/
      └─ README.md
```

## 読む順番

### 人間
1. `PROJECT.md`
2. `research/canon/hidden-continuity-design.md`
3. `research/canon/overview.md`
4. `article/outline.md`

### ChatGPT / 調査エージェント
1. `AGENTS.md`
2. `PROJECT.md`
3. `research/sources/policy.md`
4. `research/sources/factcheck.md`
5. 必要なテーマ別research

## 最重要の表記・編集ルール

- **パカーディ・ハイネン**で統一。
- 「6人の未来人」「未来から来た6人組」と書かない。
- 「正史彼女」を安易に決めない。
- 旧ジャジメントと再改称後のジャジメントを時系列上区別する。
- 一撃計画と、ジオットが実行へ向かうカタストロフを同一視しない。
- 後半作品では、連続史が彼女ルートだけでなく**周回・追加イベント・真ルートの条件そのものにも隠されている**点を記事の核にする。

# wildcard_tagnodes

ComfyUI 向けのワイルドカードタグ生成ノード集です。服装や外見（髪・体型）、アクセサリー、背景、ポーズ・表情、カメラ×ライティング、アートスタイルなど多様なタグをランダムに生成します。

## 利用可能なノード
- 服装タグ生成 (ClothingTagNode)
- 外見タグ生成 (AppearanceTagNode) — 髪と体型をまとめて生成
- アクセサリータグ生成 (AccessoryTagNode)
- 背景タグ生成 (BackgroundTagNode)
- ポーズ・表情タグ生成 (PoseEmotionTagNode)
- カメラ×ライティング統合タグ生成 (CameraLightingTagNode)
- アートスタイルタグ生成 (ArtStyleTagNode)

各ノードは `seed` を受け取り、確率設定や最大文字数、出力の小文字化など共通のオプションを備えています。統合ノードにより、髪と体型、ポーズと表情、カメラとライティングといった関連要素を一度に生成できるようになりました。

## インストール
このリポジトリを `ComfyUI/custom_nodes` に配置するだけで利用可能です。

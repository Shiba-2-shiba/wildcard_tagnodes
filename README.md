# wildcard_tagnodes

ComfyUI 向けのワイルドカードタグ生成ノード集です。服装やポーズに加え、髪型や体型、アクセサリー、ライティング、カメラアングル、アートスタイルなど多様なタグをランダムに生成します。

## 利用可能なノード
- 服装タグ生成 (ClothingTagNode)
- ポーズタグ生成 (PoseTagNode)
- 表情タグ生成 (ExpressionTagNode)
- 背景タグ生成 (BackgroundTagNode)
- ポーズ・表情タグ生成 (PoseEmotionTagNode)
- 髪型タグ生成 (HairTagNode)
- 体型タグ生成 (BodyTypeTagNode)
- アクセサリータグ生成 (AccessoryTagNode)
- ライティングタグ生成 (LightingTagNode)
- カメラアングルタグ生成 (CameraAngleTagNode)
- アートスタイルタグ生成 (ArtStyleTagNode)

各ノードは `seed` を受け取り、確率設定や最大文字数、出力の小文字化など共通のオプションを備えています。

## インストール
このリポジトリを `ComfyUI/custom_nodes` に配置するだけで利用可能です。

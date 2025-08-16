# __init__.py
# 各ノードクラスをComfyUIに登録します。

# 既存ノード
from .clothing_tag import ClothingTagNode
from .pose_tag import PoseTagNode
from .expression_tag import ExpressionTagNode
from .background_tag import BackgroundTagNode
from .pose_emotion_tag import PoseEmotionTagNode

# ComfyUIにノードを登録するための辞書
NODE_CLASS_MAPPINGS = {
    "ClothingTagNode": ClothingTagNode,
    "PoseTagNode": PoseTagNode,
    "ExpressionTagNode": ExpressionTagNode,
    "BackgroundTagNode": BackgroundTagNode,
    "PoseEmotionTagNode": PoseEmotionTagNode,
}

# ComfyUIのメニューに表示されるノード名
NODE_DISPLAY_NAME_MAPPINGS = {
    "ClothingTagNode": "服装タグ生成 (Clothing Tag)",
    "PoseTagNode": "ポーズタグ生成 (Pose Tag)",
    "ExpressionTagNode": "表情タグ生成 (Expression Tag)",
    "BackgroundTagNode": "背景タグ生成 (Background Tag)",
    "PoseEmotionTagNode": "ポーズ・表情タグ生成 (Pose+Emotion Tag)",
}
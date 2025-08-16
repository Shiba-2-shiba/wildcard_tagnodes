# __init__.py
# 各ノードクラスをComfyUIに登録します。

# 既存ノード
from .clothing_tag import ClothingTagNode
from .pose_tag import PoseTagNode
from .expression_tag import ExpressionTagNode
from .background_tag import BackgroundTagNode
from .pose_emotion_tag import PoseEmotionTagNode
from .hair_style_tag import HairTagNode
from .body_type_tag import BodyTypeTagNode
from .accessory_tag import AccessoryTagNode
from .lighting_tag import LightingTagNode
from .camera_angle_tag import CameraAngleTagNode
from .art_style_tag import ArtStyleTagNode

# ComfyUIにノードを登録するための辞書
NODE_CLASS_MAPPINGS = {
    "ClothingTagNode": ClothingTagNode,
    "PoseTagNode": PoseTagNode,
    "ExpressionTagNode": ExpressionTagNode,
    "BackgroundTagNode": BackgroundTagNode,
    "PoseEmotionTagNode": PoseEmotionTagNode,
    "HairTagNode": HairTagNode,
    "BodyTypeTagNode": BodyTypeTagNode,
    "AccessoryTagNode": AccessoryTagNode,
    "LightingTagNode": LightingTagNode,
    "CameraAngleTagNode": CameraAngleTagNode,
    "ArtStyleTagNode": ArtStyleTagNode,
}

# ComfyUIのメニューに表示されるノード名
NODE_DISPLAY_NAME_MAPPINGS = {
    "ClothingTagNode": "服装タグ生成 (Clothing Tag)",
    "PoseTagNode": "ポーズタグ生成 (Pose Tag)",
    "ExpressionTagNode": "表情タグ生成 (Expression Tag)",
    "BackgroundTagNode": "背景タグ生成 (Background Tag)",
    "PoseEmotionTagNode": "ポーズ・表情タグ生成 (Pose+Emotion Tag)",
    "HairTagNode": "髪型タグ生成 (Hair Tag)",
    "BodyTypeTagNode": "体型タグ生成 (Body Type Tag)",
    "AccessoryTagNode": "アクセサリータグ生成 (Accessory Tag)",
    "LightingTagNode": "ライティングタグ生成 (Lighting Tag)",
    "CameraAngleTagNode": "カメラアングルタグ生成 (Camera Angle Tag)",
    "ArtStyleTagNode": "アートスタイルタグ生成 (Art Style Tag)",
}
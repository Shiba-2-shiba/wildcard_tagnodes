# prompt_assemblerのインポートを追加
from .prompt_assembler import MarkdownPromptAssemblerNode
from .clothing_tag import ClothingTagNode
from .background_tag import BackgroundTagNode
from .pose_emotion_tag import PoseEmotionTagNode
from .accessory_tag import AccessoryTagNode
from .art_style_tag import ArtStyleTagNode
from .appearance_tag import AppearanceTagNode 
from .camera_lighting_tag import CameraLightingTagNode  

# ---- 登録マップ ----
NODE_CLASS_MAPPINGS = {
    # MarkdownPromptAssemblerNode を追加
    "MarkdownPromptAssemblerNode": MarkdownPromptAssemblerNode,
    "ClothingTagNode": ClothingTagNode,
    "BackgroundTagNode": BackgroundTagNode,
    "PoseEmotionTagNode": PoseEmotionTagNode,   
    "AccessoryTagNode": AccessoryTagNode,
    "ArtStyleTagNode": ArtStyleTagNode,
    "AppearanceTagNode": AppearanceTagNode,    
    "CameraLightingTagNode": CameraLightingTagNode,  
}

# ---- 表示名マップ（メニュー名）----
NODE_DISPLAY_NAME_MAPPINGS = {
    # MarkdownPromptAssemblerNode の表示名を追加
    "MarkdownPromptAssemblerNode": "Markdownプロンプト組立 (Prompt Assembler)",
    "ClothingTagNode": "服装タグ生成 (Clothing Tag)",
    "BackgroundTagNode": "背景タグ生成 (Background Tag)",
    "PoseEmotionTagNode": "ポーズ・表情タグ生成 (Pose+Emotion Tag)",
    "AccessoryTagNode": "アクセサリータグ生成 (Accessory Tag)",
    "ArtStyleTagNode": "アートスタイルタグ生成 (Art Style Tag)",
    "AppearanceTagNode": "外見タグ生成 (Appearance Tag)",
    "CameraLightingTagNode": "カメラ×ライティング統合タグ生成 (Camera+Lighting Tag)",
}

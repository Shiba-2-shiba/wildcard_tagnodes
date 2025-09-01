# ファイル名: prompt_assembler.py

import re

# 必要な語彙をインポートして、構図やライティングに関連するタグを特定できるようにします
try:
    from .vocab.pose_emotion_vocab import VIEW_ANGLES, VIEW_FRAMING
    from .vocab.background_vocab import BG_LIGHT, BG_FX
except ImportError:
    print("Warning: Vocab files not found for PromptAssemblerNode. Tag splitting will be basic.")
    VIEW_ANGLES, VIEW_FRAMING, BG_LIGHT, BG_FX = [], [], [], []

# 高速な検索のためにセットに変換
COMPOSITION_TAGS = set(VIEW_ANGLES + VIEW_FRAMING)
LIGHTING_TAGS = set(BG_LIGHT + BG_FX)

class MarkdownPromptAssemblerNode:
    """
    複数のタグ生成ノードからの出力を受け取り、
    指定されたMarkdown形式のプロンプトに組み立てるノード。
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "overall_concept": ("STRING", {
                    "multiline": True,
                    "default": "# 全体のコンセプトと品質 (Overall Concept & Quality)\nmasterpiece, best quality, ultra-detailed, photorealistic, 1girl, solo"
                }),
                "appearance_tags": ("STRING", {"multiline": False, "default": ""}),
                "clothing_tags": ("STRING", {"multiline": False, "default": ""}),
                "pose_emotion_tags": ("STRING", {"multiline": False, "default": ""}),
                "background_tags": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "assemble_prompt"
    CATEGORY = "Text/Formatting"

    # ★★★★★ ここからが修正箇所です ★★★★★
    # assemble_prompt 関数をクラス内に正しくインデントします
    
    def assemble_prompt(self, overall_concept, appearance_tags, clothing_tags, pose_emotion_tags, background_tags):
        
        # --- pose_emotion_tagsを「表情とポーズ」と「構図」に分割 ---
        pose_parts = []
        composition_parts = []
        # カンマやスペースで区切られたタグをリストに変換
        pe_tags = [tag.strip() for tag in re.split(r'[, ]+', pose_emotion_tags) if tag.strip()]
        for tag in pe_tags:
            if tag in COMPOSITION_TAGS:
                composition_parts.append(tag)
            else:
                pose_parts.append(tag)
        
        # --- background_tagsを「背景と設定」と「ライティング」に分割 ---
        setting_parts = []
        lighting_parts = []
        bg_tags = [tag.strip() for tag in re.split(r'[, ]+', background_tags) if tag.strip()]
        for tag in bg_tags:
            if tag in LIGHTING_TAGS:
                lighting_parts.append(tag)
            else:
                setting_parts.append(tag)

        # --- 各セクションの文字列を構築 ---
        sections = {
            "concept": overall_concept.strip(),
            "appearance": f"## 被写体 (Subject / Character)\n{appearance_tags.strip()}",
            "clothing": f"## 服装 (Attire / Outfit)\n{clothing_tags.strip()}",
            "pose": f"## 表情とポーズ (Expression & Pose)\n{', '.join(pose_parts)}",
            "background": f"## 背景と設定 (Background & Setting)\n{', '.join(setting_parts)}",
            "composition_lighting": f"## 構図とライティング (Composition & Lighting)\n{', '.join(composition_parts + lighting_parts)}"
        }

        # --- 全てのセクションを結合 ---
        final_parts = []
        # 定義された順序でセクションを追加
        for key in ["concept", "appearance", "clothing", "pose", "background", "composition_lighting"]:
            section_content = sections[key]
            # 見出し行の後の内容が空でないセクションのみを追加
            lines = section_content.splitlines()
            if len(lines) > 1 and lines[1].strip():
                final_parts.append(section_content)
        
        final_prompt = "\n\n".join(final_parts)

        return (final_prompt,)

# ComfyUIにノードを登録するための定型文
NODE_CLASS_MAPPINGS = {
    "MarkdownPromptAssemblerNode": MarkdownPromptAssemblerNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "MarkdownPromptAssemblerNode": "Markdown Prompt Assembler"
}
# background_prompt_assembler.py
# Advanced Background Tagノードからの出力を受け取り、
# 背景描写に特化したMarkdown形式のプロンプトを生成するノード。
# T5Gemmaなどのモデルが解釈しやすいように出力を調整。

import re

try:
    # background_vocab.pyから全ての語彙リストをインポートし、タグの分類に使用
    from .vocab.background_vocab import (
        BG_ENV_INDOOR, BG_ENV_OUTDOOR,
        BG_DETAILS_INDOOR, BG_DETAILS_OUTDOOR,
        BG_ARCH_INDOOR, BG_ARCH_OUTDOOR,
        BG_PROPS_INDOOR, BG_PROPS_OUTDOOR,
        BG_LIGHT, BG_TEXTURE, BG_WEATHER, BG_TIME, BG_FX
    )
    VOCAB_IMPORTED = True
except ImportError:
    print("Warning: background_vocab.py not found. BackgroundPromptAssemblerNode will not categorize tags.")
    VOCAB_IMPORTED = False

# パフォーマンス向上のため、インポートした語彙をカテゴリ別のセットに変換
if VOCAB_IMPORTED:
    VOCAB_SETS = {
        "Environment": set(BG_ENV_INDOOR + BG_ENV_OUTDOOR),
        "Details": set(BG_DETAILS_INDOOR + BG_DETAILS_OUTDOOR),
        "Architecture": set(BG_ARCH_INDOOR + BG_ARCH_OUTDOOR),
        "Props": set(BG_PROPS_INDOOR + BG_PROPS_OUTDOOR),
        "Lighting": set(BG_LIGHT),
        "Texture": set(BG_TEXTURE),
        "Weather & Season": set(BG_WEATHER),
        "Time of Day": set(BG_TIME),
        "Effects (FX)": set(BG_FX),
    }

class BackgroundPromptAssemblerNode:
    """
    背景タグを受け取り、カテゴリ分類してMarkdown形式で出力するノード。
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "background_tags": ("STRING", {"multiline": False, "default": ""}),
            },
            "optional": {
                # ★★★ T5Gemma向けにデフォルトヘッダーをシンプルに変更 ★★★
                "main_header": ("STRING", {"multiline": False, "default": "## Background & Scene"}),
                "show_category_headers": ("BOOL", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "assemble_background_prompt"
    CATEGORY = "Text/Formatting"

    def assemble_background_prompt(self, background_tags, main_header="## Background & Scene", show_category_headers=True):
        # 語彙ファイルが見つからない場合は、単純にタグを結合して返す
        if not VOCAB_IMPORTED:
            prompt = f"{main_header}\n{background_tags}"
            return (prompt,)
            
        # 1. 入力されたタグ文字列をリストに分割
        tags = [tag.strip() for tag in background_tags.split(',') if tag.strip()]

        # 2. タグをカテゴリごとに分類
        categorized_tags = {key: [] for key in VOCAB_SETS.keys()}
        misc_tags = []

        for tag in tags:
            found_category = False
            for category, vocab_set in VOCAB_SETS.items():
                if tag in vocab_set:
                    categorized_tags[category].append(tag)
                    found_category = True
                    break
            if not found_category:
                misc_tags.append(tag)
        
        if misc_tags:
            categorized_tags["Environment"].extend(misc_tags)

        # ★★★★★ ここからが出力形式の修正箇所です ★★★★★
        # 3. T5Gemma向けのMarkdown形式で出力文字列を構築
        output_parts = []
        if main_header:
            output_parts.append(main_header.strip())

        # 表示順を定義（絵文字は削除）
        display_order = [
            "Environment", "Architecture", "Props", "Details", 
            "Lighting", "Effects (FX)", "Weather & Season", 
            "Time of Day", "Texture"
        ]

        content_parts = []
        if show_category_headers:
            # カテゴリヘッダー付きの詳細表示
            for category in display_order:
                tags_in_category = categorized_tags.get(category)
                if tags_in_category:
                    # 各カテゴリをH3見出しとタグのリストで構成
                    section = f"### {category}\n{', '.join(tags_in_category)}"
                    content_parts.append(section)
            
            if content_parts:
                # 各セクションを2つの改行で区切る
                output_parts.append("\n\n".join(content_parts))

        else:
            # カテゴリヘッダーなしのシンプル表示
            all_categorized_tags = []
            for category in display_order:
                 tags_in_category = categorized_tags.get(category)
                 if tags_in_category:
                    all_categorized_tags.extend(tags_in_category)
            if all_categorized_tags:
                output_parts.append(', '.join(all_categorized_tags))

        # main_headerと内容を1つの改行で結合
        final_prompt = "\n".join(output_parts)
        
        return (final_prompt,)

# ComfyUIへのノード登録
NODE_CLASS_MAPPINGS = {
    "BackgroundPromptAssemblerNode": BackgroundPromptAssemblerNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "BackgroundPromptAssemblerNode": "Background Prompt Assembler"
}


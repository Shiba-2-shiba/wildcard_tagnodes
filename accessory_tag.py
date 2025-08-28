# accessory_tag.py (改善版)
# アクセサリータグ生成ノード

import random
from .util import rng_from_seed, join_clean, limit_len, normalize
# 改善版vocabファイルから全てをインポート
from .vocab.accessory_vocab import *

class AccessoryTagNode:
    # 利用可能なテーマパックのリストを取得
    THEME_PACK_KEYS = ["none"] + list(THEME_PACKS.keys())

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31 - 1}),
            },
            "optional": {
                "最大文字数": ("INT", {"default": 150, "min": 0, "max": 4096}),
                "小文字化": ("BOOL", {"default": True}),
                # テーマパック選択用のUIを追加
                "theme_pack": (cls.THEME_PACK_KEYS, {"default": "none"}),
                # 確率設定をカテゴリ毎に整理
                "確率_頭": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_顔": ("FLOAT", {"default": 0.25, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_耳": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_首": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_手腕": ("FLOAT", {"default": 0.4, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_他": ("FLOAT", {"default": 0.35, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_手持": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def _apply_exclusive_groups(self, rng, tags, exclusive_groups):
        """
        排他的タググループを適用し、矛盾するタグを削除するヘルパー関数。
        """
        final_tags = []
        used_groups = set()
        
        # タグをシャッフルして、どのタグが優先されるかをランダムにする
        random.Random(rng.random()).shuffle(tags)

        for tag in tags:
            is_exclusive = False
            for group_name, group_tags in exclusive_groups.items():
                if tag in group_tags:
                    if group_name not in used_groups:
                        final_tags.append(tag)
                        used_groups.add(group_name)
                    is_exclusive = True
                    break
            if not is_exclusive:
                final_tags.append(tag)
        return final_tags

    def generate(self, seed, 最大文字数=150, 小文字化=True, theme_pack="none", **kwargs):
        rng = rng_from_seed(seed)
        
        # 3. リファクタリング: カテゴリ、語彙、確率を辞書で一元管理
        # これにより、カテゴリの追加や削除が容易になる
        categories = {
            "頭": (HEADWEAR, kwargs.get("確率_頭", 0.3)),
            "顔": (EYEWEAR, kwargs.get("確率_顔", 0.25)),
            "耳": (EARRINGS, kwargs.get("確率_耳", 0.2)),
            "首": (NECKLACES, kwargs.get("確率_首", 0.3)),
            "手腕": (HAND_ACCESSORIES, kwargs.get("確率_手腕", 0.4)),
            "他": (OTHER_ACCESSORIES, kwargs.get("確率_他", 0.35)),
            "手持": (HANDHELD, kwargs.get("確率_手持", 0.2)),
        }

        # --- 生成ロジックの高度化 ---
        
        # ステップ 0: テーマパックの処理
        selected_tags = []
        if theme_pack != "none":
            theme_tags = THEME_PACKS.get(theme_pack, [])
            # テーマのタグをいくつかランダムに選ぶ（例: 1〜3個）
            num_to_pick = rng.randint(1, min(len(theme_tags), 3))
            selected_tags.extend(rng.sample(theme_tags, num_to_pick))

        # ステップ 1: 確率に基づいたタグの抽選 (第1段階)
        for category_name, (vocab, probability) in categories.items():
            if rng.random() < probability:
                # 既に選ばれているタグは候補から除外
                available_vocab = [t for t in vocab if t not in selected_tags]
                if available_vocab:
                    selected_tags.append(rng.choice(available_vocab))
        
        # ステップ 1.5: 排他的タグの処理
        selected_tags = self._apply_exclusive_groups(rng, selected_tags, EXCLUSIVE_TAG_GROUPS)

        # ステップ 2: 文字数が少ない場合にタグを追加 (第2段階)
        # 現在の文字数が最大文字数の半分未満の場合、タグを追加する
        current_length = len(join_clean(selected_tags))
        if current_length < 最大文字数 / 2:
            # まだタグが選ばれていないカテゴリのリストを作成
            unused_categories = [
                cat_vocab for _, (cat_vocab, _) in categories.items() 
                if not any(tag in selected_tags for tag in cat_vocab)
            ]
            rng.shuffle(unused_categories)

            # プロンプトが長くなりすぎるまで、未使用カテゴリからタグを追加
            for vocab in unused_categories:
                if len(join_clean(selected_tags)) >= 最大文字数:
                    break
                available_vocab = [t for t in vocab if t not in selected_tags]
                if available_vocab:
                    new_tag = rng.choice(available_vocab)
                    # 追加する前に排他チェックを行う
                    temp_tags = selected_tags + [new_tag]
                    if len(self._apply_exclusive_groups(rng, temp_tags, EXCLUSIVE_TAG_GROUPS)) == len(temp_tags):
                        selected_tags.append(new_tag)

        # ステップ 3: 最終的なプロンプトの構築
        # もし何も選ばれなかった場合のフォールバック処理
        if not selected_tags:
            all_items = [item for vocab in categories.values() for item in vocab[0]]
            if all_items:
                selected_tags.append(rng.choice(all_items))
        
        tag = join_clean(selected_tags)
        tag = normalize(tag, 小文字化)
        tag = limit_len(tag, 最大文字数)
        
        return (tag,)

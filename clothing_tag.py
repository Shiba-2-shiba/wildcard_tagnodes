# clothing_tag.py (v6 - 露出度選択・文字数調整強化版)
# - UIから露出度を選択可能に
# - 文字数上限まで積極的にタグを追加するロジックに強化

import random
from typing import List, Optional, Dict, Set
from .util import (
    rng_from_seed, maybe, pick, join_clean, limit_len, normalize, merge_unique
)
# [修正なし] 語彙定義をインポート
from .vocab.clothing_vocab import (
    COLORS, MATERIALS, PATTERNS, STYLES, EMBELLISH,
    TOPS, BOTTOMS, OUTERWEAR, DRESSES_SETS, LINGERIE,
    ACCENTS_EROTIC, REVEAL_MILD, REVEAL_BOLD, REVEAL_EXPLICIT,
    STATES,
    THEMES, EXCLUSIVE_GROUPS
)

# ========================
# UI日本語化のための定義
# ========================
MODE_MAP_JP = {"一般": "non_erotic", "セクシー": "erotic"}
# [修正] 露出度の選択肢を更新
EXPOSURE_MAP_JP = {"なし": "none", "マイルド": "mild", "大胆": "bold", "過激": "explicit"}
THEME_CHOICES = ["none"] + sorted(list(THEMES.keys()))

# ========================
# 準備ヘルパ
# ========================
def _apply_themes(base: dict, theme_keys: List[str]) -> dict:
    b = base.copy()
    for k in theme_keys:
        t = THEMES.get(k, {})
        for vocab_key in b.keys():
            b[vocab_key] = merge_unique(b[vocab_key], t.get(vocab_key, []))
    return b

def _get_exclusive_tags(first_tag: str) -> Set[str]:
    exclusive_set = set()
    for group_name, groups in EXCLUSIVE_GROUPS.items():
        for category, tags in groups.items():
            if first_tag in tags:
                for other_category, other_tags in groups.items():
                    if category != other_category:
                        exclusive_set.update(other_tags)
    return exclusive_set

def _prepare_lists(theme_keys: List[str]) -> Dict[str, List[str]]:
    base = {
        "colors": COLORS, "materials": MATERIALS, "patterns": PATTERNS,
        "styles": STYLES, "embellish": EMBELLISH, "tops": TOPS, "bottoms": BOTTOMS,
        "outerwear": OUTERWEAR, "dresses_sets": DRESSES_SETS, "lingerie": LINGERIE,
        "accents_erotic": ACCENTS_EROTIC, "reveal_mild": REVEAL_MILD,
        "reveal_bold": REVEAL_BOLD, "reveal_explicit": REVEAL_EXPLICIT,
        "states": STATES
    }
    if theme_keys:
        base = _apply_themes(base, theme_keys)
    return base

def _get_exposure_profile(level: str, erotic: bool, L: Dict[str, List[str]]) -> (List[str], float):
    """露出度設定に応じたタグのプールと確率を返す"""
    level = (level or "none").lower()
    pool, prob = [], 0.0
    if erotic:
        if level == "mild":     pool, prob = L["reveal_mild"], 0.5
        elif level == "bold":   pool, prob = L["reveal_mild"] + L["reveal_bold"], 0.75
        elif level == "explicit": pool, prob = L["reveal_bold"] + L["reveal_explicit"], 0.9
    else: # non-erotic
        if level == "mild":     pool, prob = L["reveal_mild"], 0.3
        elif level == "bold":   pool, prob = L["reveal_mild"] + L["reveal_bold"], 0.5
    return pool, prob

# ========================
# 生成ロジック
# ========================
def _compose(rng: random.Random, L: Dict[str, List[str]], erotic: bool, exposure_level: str, max_len: int) -> str:
    # --- ステージ1: 基本的な服装の組み合わせを決定 ---
    base_tags = []
    selected_categories = set()
    if erotic:
        if maybe(rng, 0.6): base_tags.append(pick(rng, L["lingerie"])); selected_categories.add("lingerie")
        else: base_tags.extend([pick(rng, L["tops"]), pick(rng, L["bottoms"])]); selected_categories.update(["tops", "bottoms"])
    else:
        if maybe(rng, 0.4): base_tags.append(pick(rng, L["dresses_sets"])); selected_categories.add("dresses_sets")
        else: base_tags.extend([pick(rng, L["tops"]), pick(rng, L["bottoms"])]); selected_categories.update(["tops", "bottoms"])
    if "dresses_sets" in selected_categories or ("tops" in selected_categories and "bottoms" in selected_categories):
        if maybe(rng, 0.35): base_tags.append(pick(rng, L["outerwear"])); selected_categories.add("outerwear")

    # --- ステージ2: 装飾的なタグを確率に基づいて追加 ---
    all_tags = list(base_tags)
    exclusive_tags = set().union(*[_get_exclusive_tags(tag) for tag in all_tags])

    def add_tag_if_not_exclusive(category: str, probability: float):
        if maybe(rng, probability):
            available_tags = [t for t in L[category] if t not in exclusive_tags]
            if available_tags:
                tag = pick(rng, available_tags)
                all_tags.append(tag)
                exclusive_tags.update(_get_exclusive_tags(tag))
                selected_categories.add(category)

    add_tag_if_not_exclusive("colors", 0.8)
    add_tag_if_not_exclusive("materials", 0.7)
    add_tag_if_not_exclusive("patterns", 0.4)
    add_tag_if_not_exclusive("styles", 0.6)
    add_tag_if_not_exclusive("embellish", 0.5)
    if erotic: add_tag_if_not_exclusive("accents_erotic", 0.6)
    
    # --- ステージ3: 露出表現の追加 ---
    exposure_pool, exposure_prob = _get_exposure_profile(exposure_level, erotic, L)
    if exposure_pool and maybe(rng, exposure_prob):
        tag = pick(rng, exposure_pool)
        if tag not in exclusive_tags:
            all_tags.append(tag)

    # --- ステージ4: 服装の状態を低確率で追加 ---
    if maybe(rng, 0.2):
        available_states = [s for s in L["states"] if s not in exclusive_tags]
        if available_states: all_tags.append(pick(rng, available_states))

    # --- [強化] ステージ5: 文字数調整 ---
    supplementary_categories = ["styles", "embellish", "materials", "patterns", "colors"]
    if erotic: supplementary_categories.append("accents_erotic")
    
    # 文字数が最大値に近づくまでタグを追加し続ける
    while len(join_clean(all_tags)) < max_len and supplementary_categories:
        category_to_add = rng.choice(supplementary_categories)
        available_tags = [t for t in L[category_to_add] if t not in exclusive_tags and t not in all_tags]
        
        if available_tags:
            tag = pick(rng, available_tags)
            # 追加しても文字数を超えない場合のみ追加
            if len(join_clean(all_tags + [tag])) <= max_len:
                all_tags.append(tag)
                exclusive_tags.update(_get_exclusive_tags(tag))
            else:
                # このタグを追加すると長すぎるので、このカテゴリは一旦試行済みとする
                supplementary_categories.remove(category_to_add)
        else:
            # このカテゴリには追加できるタグがないのでリストから削除
            supplementary_categories.remove(category_to_add)

    return join_clean(all_tags)

# ========================
# ComfyUI Node Class
# ========================
class ClothingTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31-1}),
                "モード": (list(MODE_MAP_JP.keys()),),
                "露出度": (list(EXPOSURE_MAP_JP.keys()), {"default": "マイルド"}), # [修正]
                "最大文字数": ("INT", {"default": 150, "min": 30, "max": 4096}),
            },
            "optional": {
                "テーマ1": (THEME_CHOICES,), "テーマ2": (THEME_CHOICES,), "テーマ3": (THEME_CHOICES,),
                "小文字化": ("BOOL", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def generate(self, seed, モード, 露出度, 最大文字数, テーマ1="none", テーマ2="none", テーマ3="none", 小文字化=True, **kwargs):
        rng = rng_from_seed(seed)
        mode_en = MODE_MAP_JP.get(モード, "non_erotic")
        exposure_en = EXPOSURE_MAP_JP.get(露出度, "none") # [修正]
        
        theme_keys = [k for k in [テーマ1, テーマ2, テーマ3] if k and k != "none"]
        L = _prepare_lists(theme_keys)
        
        tag = _compose(rng, L, erotic=(mode_en=="erotic"), exposure_level=exposure_en, max_len=最大文字数)
        
        tag = normalize(tag, 小文字化)
        # 最終的な文字数制限は念のため残す
        tag = limit_len(tag, 最大文字数)
        
        return (tag,)

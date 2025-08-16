# pose_tag.py (改修版)

from typing import List, Dict
from .util import (
    rng_from_seed, maybe, pick, join_clean, limit_len, normalize, merge_unique
)
from .vocab.pose_vocab import (
    POSE_VIEW,
    POSE_BODY_DAILY, POSE_MOTION_DAILY, POSE_PROPS_DAILY,
    POSE_BODY_ACTION, POSE_MOTION_ACTION, POSE_PROPS_ACTION
)

# ========================
# UI日本語化とモード定義
# ========================
MODE_MAP_JP = {"日常": "daily", "アクション": "action"}
COMPLEXITY_MAP_JP = {"シンプル": "simple", "標準": "normal", "複雑": "complex"}

# ========================
# 準備ヘルパ
# ========================
def _prepare_lists(mode: str) -> Dict[str, List[str]]:
    """選択されたモードに応じて語彙リストを準備する"""
    if mode == "action":
        return {
            "body": merge_unique(POSE_BODY_DAILY, POSE_BODY_ACTION),
            "view": POSE_VIEW,
            "motion": merge_unique(POSE_MOTION_DAILY, POSE_MOTION_ACTION),
            "props": merge_unique(POSE_PROPS_DAILY, POSE_PROPS_ACTION),
        }
    # デフォルトは "daily"
    return {
        "body": POSE_BODY_DAILY,
        "view": POSE_VIEW,
        "motion": POSE_MOTION_DAILY,
        "props": POSE_PROPS_DAILY,
    }

def _complexity_profile(level: str) -> Dict[str, float]:
    """構図の複雑さに応じて各要素の生成確率に乗数を設定する"""
    level = (level or "normal").lower()
    # デフォルト (標準) の確率乗数
    mul = dict(view=0.8, motion=0.6, props=0.5)
    if level == "simple":
        # シンプル: 基本のポーズのみになりやすく、他の要素を抑制
        mul.update(view=0.5, motion=0.2, props=0.1)
    elif level == "complex":
        # 複雑: 視点、動き、小道具の要素がすべて出やすくなる
        mul.update(view=0.95, motion=0.8, props=0.75)
    return mul

def _compose(rng, p: Dict[str, float], L: Dict[str, List[str]], complexity_level: str) -> str:
    """各パーツを確率に基づいて組み合わせてタグを生成する"""
    mul = _complexity_profile(complexity_level)

    # 必須要素
    body = pick(rng, L["body"]) or "standing straight"

    # 確率で追加される要素
    view = pick(rng, L["view"]) if maybe(rng, p["p_view"] * mul["view"]) else None
    motion = pick(rng, L["motion"]) if maybe(rng, p["p_motion"] * mul["motion"]) else None
    props = pick(rng, L["props"]) if maybe(rng, p["p_props"] * mul["props"]) else None

    # 結合処理
    tag = join_clean([body, view, motion, props], sep=", ")
    return tag

# ========================
# メインノードクラス
# ========================
class PoseTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31 - 1}),
            },
            "optional": {
                "モード": (list(MODE_MAP_JP.keys()),),
                "構図の複雑さ": (list(COMPLEXITY_MAP_JP.keys()), {"default": "標準"}),
                "最大文字数": ("INT", {"default": 100, "min": 0, "max": 4096}),
                "小文字化": ("BOOL", {"default": True}),
                "確率: 視点": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 動き": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 小道具": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def generate(self, seed, モード="日常", 構図の複雑さ="標準", 最大文字数=100, 小文字化=True,
                 確率_視点=1.0, 確率_動き=1.0, 確率_小道具=1.0, **kwargs):

        rng = rng_from_seed(seed)
        mode_en = MODE_MAP_JP.get(モード, "daily")
        complexity_en = COMPLEXITY_MAP_JP.get(構図の複雑さ, "normal")

        L = _prepare_lists(mode_en)

        params = {"p_view": 確率_視点, "p_motion": 確率_動き, "p_props": 確率_小道具}

        tag = _compose(rng, params, L, complexity_en)

        tag = normalize(tag, 小文字化)
        tag = limit_len(tag, 最大文字数)
        return (tag,)
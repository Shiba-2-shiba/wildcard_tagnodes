# expression_tag.py — 拡張版 v2.1（不具合修正）

from typing import List, Dict
from .util import (
    rng_from_seed, maybe, pick, join_clean, limit_len, normalize, merge_unique
)
# [修正] 新しい語彙ファイルをインポート
from .vocab.expression_vocab import (
    MOUTH_DAILY, EYES_DAILY, MOOD_DAILY,
    MOUTH_ALLURE, EYES_ALLURE, MOOD_ALLURE,
    BROW_COMMON
)

# ========================
# UI日本語化とモード定義
# ========================
MODE_MAP_JP = {"日常": "daily", "魅惑": "allure"}
INTENSITY_MAP_JP = {"控えめ": "subtle", "普通": "normal", "豊か": "expressive"}

# ========================
# 準備ヘルパ
# ========================
def _prepare_lists(mode: str) -> Dict[str, List[str]]:
    """選択されたモードに応じて語彙リストを準備する"""
    if mode == "allure":
        return {
            "mouth": merge_unique(MOUTH_DAILY, MOUTH_ALLURE),
            "eyes": merge_unique(EYES_DAILY, EYES_ALLURE),
            "mood": merge_unique(MOOD_DAILY, MOOD_ALLURE),
            "brow": BROW_COMMON,
        }
    # デフォルトは "daily"
    return {
        "mouth": MOUTH_DAILY,
        "eyes": EYES_DAILY,
        "mood": MOOD_DAILY,
        "brow": BROW_COMMON,
    }

def _intensity_profile(level: str) -> Dict[str, float]:
    """感情の強さに応じて各要素の生成確率に乗数を設定する"""
    level = (level or "normal").lower()
    # デフォルトの確率乗数
    mul = dict(mouth=1.0, eyes=1.0, brow=0.6, mood=0.7)
    if level == "subtle":
        # 控えめ: ムードや眉の表現を抑える
        mul.update(brow=0.3, mood=0.4)
    elif level == "expressive":
        # 豊か: 全ての要素が出やすくなる
        mul.update(brow=0.8, mood=0.95)
    return mul

# [修正] エラーが発生した関数を修正
def _compose(rng, p: Dict[str, float], L: Dict[str, List[str]], intensity_level: str) -> str:
    """各パーツを確率に基づいて組み合わせてタグを生成する"""
    mul = _intensity_profile(intensity_level)
    
    # 必須要素
    mouth = pick(rng, L["mouth"]) or "soft smile"
    eyes = pick(rng, L["eyes"]) or "gentle gaze"
    
    # 確率で追加される要素
    brow = pick(rng, L["brow"]) if maybe(rng, p["p_brow"] * mul["brow"]) else None
    mood = pick(rng, L["mood"]) if maybe(rng, p["p_mood"] * mul["mood"]) else None
    
    # 結合処理を修正
    # まず、基本的な表情パーツを結合する
    tag = join_clean([mouth, eyes, brow], sep=", ")
    
    # moodが存在すれば、さらに結合する
    if mood:
        tag = join_clean([tag, mood], sep=", ")
        
    return tag

# ========================
# メインノードクラス
# ========================
class ExpressionTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31-1}),
            },
            "optional": {
                "モード": (list(MODE_MAP_JP.keys()),),
                "感情の強さ": (list(INTENSITY_MAP_JP.keys()), {"default": "普通"}),
                "最大文字数": ("INT", {"default": 80, "min": 0, "max": 4096}),
                "小文字化": ("BOOL", {"default": True}),
                "確率: 眉": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: ムード": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def generate(self, seed, モード="日常", 感情の強さ="普通", 最大文字数=80, 小文字化=True,
                 確率_眉=1.0, 確率_ムード=1.0, **kwargs):
        
        rng = rng_from_seed(seed)
        mode_en = MODE_MAP_JP.get(モード, "daily")
        intensity_en = INTENSITY_MAP_JP.get(感情の強さ, "normal")
        
        L = _prepare_lists(mode_en)
        
        params = {"p_brow": 確率_眉, "p_mood": 確率_ムード}

        tag = _compose(rng, params, L, intensity_en)
        
        tag = normalize(tag, 小文字化)
        tag = limit_len(tag, 最大文字数)
        return (tag,)
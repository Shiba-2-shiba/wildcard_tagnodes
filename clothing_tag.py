# clothing_tag.py — 拡張版 v3.5（語彙フォルダ対応）
# - 語彙のインポート元を vocab/clothing_vocab.py に変更

from typing import List, Optional, Dict
from .util import (
    rng_from_seed, maybe, pick, join_clean, limit_len, normalize, merge_unique
)
# [修正] vocabパッケージ内のclothing_vocabからインポートするように変更
from .vocab.clothing_vocab import (
    COLORS, MATERIALS, PATTERNS, STYLES, CLOSURES, EMBELLISH,
    BASES_EROTIC, ACCENTS_EROTIC, BASES_NONEROTIC, ACCENTS_NONEROTIC,
    REVEAL_MILD, REVEAL_BOLD, REVEAL_EXPLICIT, THEMES
)

# ========================
# UI日本語化のための定義
# ========================
MODE_MAP_JP = {"一般": "non_erotic", "セクシー": "erotic"}
EXPOSURE_MAP_JP = {"控えめ": "modest", "普通": "mild", "大胆": "bold", "過激": "explicit"}
THEME_CHOICES = ["none"] + sorted(list(THEMES.keys()))

# ========================
# 準備ヘルパ
# ========================
def _apply_themes(base: dict, theme_keys: List[str]) -> dict:
    b = base.copy()
    for k in theme_keys:
        t = THEMES.get(k, {})
        b["bases_erotic"] = merge_unique(b["bases_erotic"], t.get("bases_erotic", []))
        b["bases_non"]    = merge_unique(b["bases_non"],    t.get("bases_non",    []))
        b["acc_erotic"]   = merge_unique(b["acc_erotic"],   t.get("accents_erotic", []))
        b["acc_non"]      = merge_unique(b["acc_non"],      t.get("accents_non",    []))
        b["materials"]    = merge_unique(b["materials"],    t.get("materials", []))
        b["patterns"]     = merge_unique(b["patterns"],     t.get("patterns",  []))
        b["styles"]       = merge_unique(b["styles"],       t.get("styles",    []))
    return b

def _exposure_profile(level: str, erotic: bool):
    level = (level or "modest").lower()
    mul = dict(color=1.0, material=1.0, pattern=1.0, style=1.0, accent=1.0, reveal=0.0)
    pool = []
    if level == "modest": mul.update(style=0.9, accent=0.7, reveal=0.0)
    elif level == "mild": mul.update(style=1.0, accent=1.0, reveal=0.35 if erotic else 0.15); pool = REVEAL_MILD
    elif level == "bold": mul.update(style=1.1, accent=1.15, reveal=0.6 if erotic else 0.3); pool = REVEAL_MILD + REVEAL_BOLD
    else: mul.update(style=1.15, accent=1.3, reveal=0.85 if erotic else 0.45); pool = REVEAL_MILD + REVEAL_BOLD + REVEAL_EXPLICIT
    return mul, pool

def _prepare_lists(theme_keys: List[str]):
    base = dict(colors=COLORS, materials=MATERIALS, patterns=PATTERNS, styles=STYLES, closures=CLOSURES, embellish=EMBELLISH, bases_erotic=BASES_EROTIC, bases_non=BASES_NONEROTIC, acc_erotic=ACCENTS_EROTIC, acc_non=ACCENTS_NONEROTIC,)
    if theme_keys: base = _apply_themes(base, theme_keys)
    return base

def _compose(rng, p, L, erotic: bool, exposure_level: str) -> str:
    mul, reveal_pool = _exposure_profile(exposure_level, erotic)
    def scaled(prob): return max(0.0, min(1.0, prob * mul.get("accent", 1.0)))
    color  = pick(rng, L["colors"])     if maybe(rng, p["p_color"] * mul.get("color",1.0)) else None
    mater  = pick(rng, L["materials"])  if maybe(rng, p["p_material"] * mul.get("material",1.0)) else None
    patt   = pick(rng, L["patterns"])   if maybe(rng, p["p_pattern"] * mul.get("pattern",1.0)) else None
    base   = pick(rng, L["bases_erotic"] if erotic else L["bases_non"]) or ("lingerie set" if erotic else "outfit set")
    if erotic and any(k in (base or "").lower() for k in ["blindfold","pasties","rope","handcuffs"]) and mater is None: mater = pick(rng, ["silk","satin","leather"])
    head = join_clean([color, mater, patt, base], sep=" ")
    tail: List[str] = []
    if maybe(rng, p["p_style"] * mul.get("style",1.0)): tail.append(pick(rng, L["styles"]))
    if maybe(rng, p["p_closure"]): tail.append(pick(rng, CLOSURES))
    if maybe(rng, p["p_embellish"]): tail.append(pick(rng, L["embellish"]))
    if erotic:
        if maybe(rng, scaled(p["p_accent_core"])): tail.append(pick(rng, L["acc_erotic"]))
        if reveal_pool and maybe(rng, mul.get("reveal",0.0)): tail.append(pick(rng, reveal_pool))
    else:
        if maybe(rng, scaled(p["p_accent_core"])): tail.append(pick(rng, L["acc_non"]))
        if reveal_pool and maybe(rng, mul.get("reveal",0.0) * 0.6): tail.append(pick(rng, REVEAL_MILD if exposure_level in ("mild","bold") else REVEAL_MILD))
    tail = [t for t in tail if t]
    return join_clean([head, ", ".join(tail)], sep=", ") if tail else head

# ========================
# 単出力版
# ========================
class ClothingTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31-1}),
            },
            "optional": {
                "モード": (list(MODE_MAP_JP.keys()),),
                "テーマ1": (THEME_CHOICES,),
                "テーマ2": (THEME_CHOICES,),
                "テーマ3": (THEME_CHOICES,),
                "テーマ4": (THEME_CHOICES,),
                "テーマ5": (THEME_CHOICES,),
                "露出度": (list(EXPOSURE_MAP_JP.keys()), {"default": "普通"}),
                "最大文字数": ("INT", {"default": 120, "min": 0, "max": 4096}),
                "小文字化": ("BOOL", {"default": True}),
                "確率: 色": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 素材": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 柄": ("FLOAT", {"default": 0.35, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: スタイル": ("FLOAT", {"default": 0.55, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 留め具": ("FLOAT", {"default": 0.35, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 装飾": ("FLOAT", {"default": 0.55, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: アクセント": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 露出表現": ("FLOAT", {"default": 0.45, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def generate(self, seed, モード="一般",
                 テーマ1="none", テーマ2="none", テーマ3="none", テーマ4="none", テーマ5="none",
                 露出度="普通", 最大文字数=120, 小文字化=True,
                 確率_色=0.7, 確率_素材=0.8, 確率_柄=0.35,
                 確率_スタイル=0.55, 確率_留め具=0.35, 確率_装飾=0.55, 確率_アクセント=0.5, 確率_露出表現=0.45,
                 **kwargs):
        rng = rng_from_seed(seed)
        mode_en = MODE_MAP_JP.get(モード, "non_erotic")
        exposure_en = EXPOSURE_MAP_JP.get(露出度, "mild")

        keys = []
        for k in [テーマ1, テーマ2, テーマ3, テーマ4, テーマ5]:
            if k and k != "none" and k in THEMES and k not in keys:
                keys.append(k)
        
        L = _prepare_lists(keys)
        
        params = {
            "p_color": 確率_色, "p_material": 確率_素材, "p_pattern": 確率_柄,
            "p_style": 確率_スタイル, "p_closure": 確率_留め具, "p_embellish": 確率_装飾,
            "p_accent_core": 確率_アクセント, "p_reveal": 確率_露出表現
        }

        tag = _compose(rng, params, L, erotic=(mode_en=="erotic"), exposure_level=exposure_en)
        tag = normalize(tag, 小文字化)
        tag = limit_len(tag, 最大文字数)
        return (tag,)

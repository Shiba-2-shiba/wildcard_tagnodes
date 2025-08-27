# appearance_tag.py
# 体型 + 胸サイズ + 髪タグ（長さ/質感/スタイル/前髪・分け目/色/色ミックス）統合ノード
# - clothing_tag の設計を踏襲し確率/UI/テーマ拡張に対応
# - kawaii テーマに petite 系（childlike 等）を集約
# - 胸サイズは段階 + ソフト/NSFW オプションを独立確率で制御

from typing import List
from .util import (
    rng_from_seed, maybe, pick, join_clean, limit_len, normalize, merge_unique
)
from .vocab.appearance_vocab import (
    BODY_BASE, BODY_DETAILS,
    BUST_SIZES, BUST_OPTIONS_SOFT, BUST_OPTIONS_NSFW,
    HAIR_LENGTHS, HAIR_TEXTURES, HAIR_ARRANGEMENTS, HAIR_BANGS_PART,
    HAIR_COLORS, HAIR_COLOR_MIX,
    THEMES,
)

# ===== UIラベル =====
MODE_MAP_JP = {"一般": "normal", "セクシー": "sexy"}
THEME_CHOICES = ["none"] + sorted(list(THEMES.keys()))

# ===== テーマ適用 =====
def _apply_themes(base: dict, theme_keys: List[str]) -> dict:
    b = base.copy()
    for k in theme_keys:
        t = THEMES.get(k, {})
        if t:
            b["body_bias"] = merge_unique(b.get("body_bias", []), t.get("body_bias", []))
            b["hair_bias"] = merge_unique(b.get("hair_bias", []), t.get("hair_bias", []))
    return b

def _prepare_lists(theme_keys: List[str]) -> dict:
    base = dict(
        body_base=BODY_BASE,
        body_details=BODY_DETAILS,
        bust_sizes=BUST_SIZES,
        bust_soft=BUST_OPTIONS_SOFT,
        bust_nsfw=BUST_OPTIONS_NSFW,
        hair_lengths=HAIR_LENGTHS,
        hair_textures=HAIR_TEXTURES,
        hair_arr=HAIR_ARRANGEMENTS,
        hair_bangs=HAIR_BANGS_PART,
        hair_colors=HAIR_COLORS,
        hair_mix=HAIR_COLOR_MIX,
        body_bias=[],
        hair_bias=[],
    )
    if theme_keys:
        base = _apply_themes(base, theme_keys)
    return base

# ===== 合成ロジック =====
def _compose_body(rng, p, L, sexy: bool) -> str:
    # テーマ体型バイアスを優先的に採用（確率）
    base_bias = pick(rng, L.get("body_bias", [])) if L.get("body_bias") and maybe(rng, p["p_body_bias"]) else None
    base      = base_bias or pick(rng, L["body_base"]) or "balanced physique"

    detail    = pick(rng, L["body_details"]) if maybe(rng, p["p_body_detail"]) else None
    bust      = pick(rng, L["bust_sizes"])   if maybe(rng, p["p_bust"]) else None

    bust_soft = pick(rng, L["bust_soft"]) if bust and maybe(rng, p["p_bust_soft"]) else None
    bust_nsfw = pick(rng, L["bust_nsfw"]) if sexy and bust and maybe(rng, p["p_bust_nsfw"]) else None

    parts = [base, detail, bust, bust_soft, bust_nsfw]
    return join_clean([x for x in parts if x])

def _compose_hair(rng, p, L) -> str:
    # 色ミックス or 単色（排他）
    color = None
    if maybe(rng, p["p_hair_color_mix"]):
        color = pick(rng, L["hair_mix"])
    if not color and maybe(rng, p["p_hair_color"]):
        color = pick(rng, L["hair_colors"])

    length  = pick(rng, L["hair_lengths"])  if maybe(rng, p["p_hair_length"])  else None
    texture = pick(rng, L["hair_textures"]) if maybe(rng, p["p_hair_texture"]) else None
    arr     = pick(rng, L["hair_arr"])      if maybe(rng, p["p_hair_arr"])     else None
    bangs   = pick(rng, L["hair_bangs"])    if maybe(rng, p["p_hair_bangs"])   else None

    # テーマ髪バイアス（例: kawaii -> twin tails / curtain bangs など）
    bias = pick(rng, L["hair_bias"]) if L.get("hair_bias") and maybe(rng, p["p_hair_bias"]) else None

    head = join_clean([length, texture, arr, bias], sep=" ")
    if head:
        head = head + " hair"

    return join_clean([color, head, bangs], sep=", ")

# ===== ノード本体 =====
class AppearanceTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31 - 1}),
            },
            "optional": {
                # テーマ/モード
                "モード": (list(MODE_MAP_JP.keys()), {"default": "一般"}),
                "テーマ1": (THEME_CHOICES, {"default": "none"}),
                "テーマ2": (THEME_CHOICES, {"default": "none"}),
                "テーマ3": (THEME_CHOICES, {"default": "none"}),

                # 出力整形
                "最大文字数": ("INT", {"default": 120, "min": 0, "max": 4096}),
                "小文字化": ("BOOL", {"default": True}),

                # 体型/胸 確率
                "確率: テーマ体型バイアス": ("FLOAT", {"default": 0.35, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 体型詳細": ("FLOAT", {"default": 0.55, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 胸サイズ": ("FLOAT", {"default": 0.80, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 胸オプション(ソフト)": ("FLOAT", {"default": 0.40, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 胸オプション(NSFW)": ("FLOAT", {"default": 0.15, "min": 0.0, "max": 1.0, "step": 0.01}),

                # 髪 確率
                "確率: 髪の長さ": ("FLOAT", {"default": 0.90, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 髪質/仕上げ": ("FLOAT", {"default": 0.75, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 髪スタイル": ("FLOAT", {"default": 0.60, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 前髪/分け目": ("FLOAT", {"default": 0.55, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 髪色(単色)": ("FLOAT", {"default": 0.65, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 髪色(ミックス)": ("FLOAT", {"default": 0.25, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: テーマ髪バイアス": ("FLOAT", {"default": 0.35, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def generate(
        self, seed,
        モード="一般", テーマ1="none", テーマ2="none", テーマ3="none",
        最大文字数=120, 小文字化=True,
        確率_テーマ体型バイアス=0.35, 確率_体型詳細=0.55,
        確率_胸サイズ=0.80, 確率_胸オプション_ソフト=0.40, 確率_胸オプション_NSFW=0.15,
        確率_髪の長さ=0.90, 確率_髪質_仕上げ=0.75, 確率_髪スタイル=0.60, 確率_前髪_分け目=0.55,
        確率_髪色_単色=0.65, 確率_髪色_ミックス=0.25, 確率_テーマ髪バイアス=0.35,
        **kwargs
    ):
        rng = rng_from_seed(seed)
        sexy = (MODE_MAP_JP.get(モード, "normal") == "sexy")

        # テーマキー整理
        keys = []
        for k in [テーマ1, テーマ2, テーマ3]:
            if k and k != "none" and k in THEMES and k not in keys:
                keys.append(k)

        L = _prepare_lists(keys)

        p = dict(
            # 体型/胸
            p_body_bias=確率_テーマ体型バイアス,
            p_body_detail=確率_体型詳細,
            p_bust=確率_胸サイズ,
            p_bust_soft=確率_胸オプション_ソフト,
            p_bust_nsfw=確率_胸オプション_NSFW,
            # 髪
            p_hair_length=確率_髪の長さ,
            p_hair_texture=確率_髪質_仕上げ,
            p_hair_arr=確率_髪スタイル,
            p_hair_bangs=確率_前髪_分け目,
            p_hair_color=確率_髪色_単色,
            p_hair_color_mix=確率_髪色_ミックス,
            p_hair_bias=確率_テーマ髪バイアス,
        )

        body = _compose_body(rng, p, L, sexy)
        hair = _compose_hair(rng, p, L)

        tag = join_clean([body, hair], sep=", ")
        tag = normalize(tag, 小文字化)
        tag = limit_len(tag, 最大文字数)
        return (tag,)


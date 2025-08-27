# background_tag.py
# clothing_tag.py の設計思想に合わせて改修
# - 語彙を vocab/background_vocab.py に分離
# - UIを日本語化し、ドロップダウンリストを実装
# - テーマ選択をCSV形式から複数のドロップダウンに変更
# - 不要な外部ファイル読み込み機能を削除
# - [エラー修正] INPUT_TYPESのキーをPythonの引数名と完全に一致させた

from .util import (
    rng_from_seed, maybe, pick, join_clean, limit_len, normalize, merge_unique
)
from .vocab.background_vocab import (
    BG_ENV_INDOOR, BG_ENV_OUTDOOR, BG_LIGHT, BG_DETAILS, BG_TEXTURE,
    BG_WEATHER, BG_TIME, BG_FX, BG_ARCH, BG_PROPS,
    THEME_PACKS, THEME_CHOICES
)

# ========================
# UI日本語化のための定義
# ========================
ENV_MODE_MAP_JP = {
    "おまかせ": "any",
    "屋内のみ": "indoor_only",
    "屋外のみ": "outdoor_only",
    "屋内と屋外の両方": "split_indoor_outdoor"
}

# ========================
# 準備ヘルパ
# ========================

def _apply_themes(base: dict, theme_keys: list) -> dict:
    """選択されたテーマをベースの語彙リストにマージする"""
    env_in, env_out = base["env_in"], base["env_out"]
    light, details, texture, arch = base["light"], base["details"], base["texture"], base["arch"]
    
    for key in theme_keys:
        t = THEME_PACKS.get(key, {})
        env_in  = merge_unique(env_in,  t.get("env_indoor", []))
        env_out = merge_unique(env_out, t.get("env_outdoor", []))
        light   = merge_unique(light,   t.get("light", []))
        details = merge_unique(details, t.get("details", []))
        texture = merge_unique(texture, t.get("texture", []))
        arch    = merge_unique(arch,    t.get("arch", []))
        
    return dict(env_in=env_in, env_out=env_out, light=light, details=details, texture=texture, arch=arch)


def _prepare_lists(theme_keys: list) -> dict:
    """
    ベースとなる語彙リストを準備し、選択されたテーマを適用する。
    """
    base = dict(
        env_in=BG_ENV_INDOOR,
        env_out=BG_ENV_OUTDOOR,
        light=BG_LIGHT,
        details=BG_DETAILS,
        texture=BG_TEXTURE,
        weather=BG_WEATHER,
        time=BG_TIME,
        fx=BG_FX,
        arch=BG_ARCH,
        props=BG_PROPS,
    )

    if theme_keys:
        themed_base = _apply_themes(base, theme_keys)
        base.update(themed_base)

    return base


# ========================
# ノード本体
# ========================
class BackgroundTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31-1}),
            },
            "optional": {
                "テーマ1": (THEME_CHOICES,),
                "テーマ2": (THEME_CHOICES,),
                "テーマ3": (THEME_CHOICES,),
                "抽選モード": (list(ENV_MODE_MAP_JP.keys()),),
                "最大文字数": ("INT", {"default": 140, "min": 0, "max": 4096}),
                "小文字化": ("BOOL", {"default": True}),
                # [エラー修正] UIの項目名（キー）を、generate関数の引数名と完全に一致させる
                "確率_照明": ("FLOAT", {"default": 0.85, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_詳細": ("FLOAT", {"default": 0.75, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_質感": ("FLOAT", {"default": 0.65, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_天候_季節": ("FLOAT", {"default": 0.5,  "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_時間帯": ("FLOAT", {"default": 0.7,  "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_効果_演出": ("FLOAT", {"default": 0.6,  "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_建築_構造": ("FLOAT", {"default": 0.5,  "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_小道具": ("FLOAT", {"default": 0.45, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def _pick_env(self, rng, L, mode: str):
        """抽選モードに基づいて環境タグを選択する"""
        ind = pick(rng, L["env_in"]) if L["env_in"] else None
        out = pick(rng, L["env_out"]) if L["env_out"] else None
        
        if mode == "indoor_only":
            return [ind or "simple indoor set"]
        if mode == "outdoor_only":
            return [out or "simple outdoor scene"]
        if mode == "split_indoor_outdoor":
            parts = []
            parts.append(ind or "simple indoor set")
            parts.append(out or "simple outdoor scene")
            return parts
        
        if ind and out:
            chosen_env = ind if pick(rng, ["indoor", "outdoor"]) == "indoor" else out
        else:
            chosen_env = ind or out or "simple backdrop"
        return [chosen_env]

    # [エラー修正] 引数名をINPUT_TYPESのキーと完全に一致させる
    def generate(
        self,
        seed,
        テーマ1="none", テーマ2="none", テーマ3="none",
        抽選モード="おまかせ",
        最大文字数=140, 小文字化=True,
        確率_照明=0.85, 確率_詳細=0.75, 確率_質感=0.65, 確率_天候_季節=0.5, 
        確率_時間帯=0.7, 確率_効果_演出=0.6, 確率_建築_構造=0.5, 確率_小道具=0.45,
    ):
        rng = rng_from_seed(seed)

        env_mode_en = ENV_MODE_MAP_JP.get(抽選モード, "any")

        theme_keys = []
        for k in [テーマ1, テーマ2, テーマ3]:
            if k and k != "none" and k not in theme_keys:
                theme_keys.append(k)
        
        L = _prepare_lists(theme_keys)

        env_parts = self._pick_env(rng, L, env_mode_en)
        parts = list(env_parts)

        if maybe(rng, 確率_照明): parts.append(pick(rng, L["light"]))
        if maybe(rng, 確率_詳細): parts.append(pick(rng, L["details"]))
        if maybe(rng, 確率_質感): parts.append(pick(rng, L["texture"]))
        if maybe(rng, 確率_天候_季節): parts.append(pick(rng, L["weather"]))
        if maybe(rng, 確率_時間帯): parts.append(pick(rng, L["time"]))
        if maybe(rng, 確率_効果_演出): parts.append(pick(rng, L["fx"]))
        if maybe(rng, 確率_建築_構造): parts.append(pick(rng, L["arch"]))
        if maybe(rng, 確率_小道具): parts.append(pick(rng, L["props"]))

        tag = join_clean([p for p in parts if p])
        tag = normalize(tag, 小文字化)
        tag = limit_len(tag, 最大文字数)
        
        return (tag,)


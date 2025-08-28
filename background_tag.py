# background_tag.py
# 語彙の拡充と、排他的なタグのグループ化ロジックを追加

from .util import (
    rng_from_seed, maybe, pick, join_clean, limit_len, normalize, merge_unique
)
from .vocab.background_vocab import (
    BG_ENV_INDOOR, BG_ENV_OUTDOOR, BG_LIGHT, BG_DETAILS, BG_TEXTURE,
    BG_WEATHER, BG_TIME, BG_FX, BG_ARCH, BG_PROPS,
    THEME_PACKS, THEME_CHOICES, EXCLUSIVE_TAG_GROUPS
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
    # 既存のロジックは変更なし
    env_in, env_out = base["env_in"], base["env_out"]
    light, details, texture, arch, props = base["light"], base["details"], base["texture"], base["arch"], base["props"]
    
    for key in theme_keys:
        t = THEME_PACKS.get(key, {})
        env_in  = merge_unique(env_in,  t.get("env_indoor", []))
        env_out = merge_unique(env_out, t.get("env_outdoor", []))
        light   = merge_unique(light,   t.get("light", []))
        details = merge_unique(details, t.get("details", []))
        texture = merge_unique(texture, t.get("texture", []))
        arch    = merge_unique(arch,    t.get("arch", []))
        props   = merge_unique(props,   t.get("props", []))
        
    return dict(env_in=env_in, env_out=env_out, light=light, details=details, texture=texture, arch=arch, props=props)


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
            if ind: parts.append(ind)
            if out: parts.append(out)
            return parts or ["simple backdrop"]
        
        if ind and out:
            chosen_env = ind if pick(rng, ["indoor", "outdoor"]) == "indoor" else out
        else:
            chosen_env = ind or out or "simple backdrop"
        return [chosen_env]
    
    def _get_exclusive_tags(self, rng, selected_tags: list) -> list:
        """
        選ばれたタグと排他的なグループに属するタグを返す
        """
        exclusive_tags = set()
        for tag in selected_tags:
            for group in EXCLUSIVE_TAG_GROUPS.values():
                for sub_group in group:
                    if tag in sub_group:
                        # 選択されたタグと同じサブグループから他のタグを追加
                        # これにより、同じグループ内の他の要素が選ばれるのを防ぐ
                        for excl_tag in sub_group:
                            if excl_tag != tag:
                                exclusive_tags.add(excl_tag)
        return list(exclusive_tags)

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

        # 確率に基づいて各カテゴリからタグを抽選
        if maybe(rng, 確率_照明): parts.append(pick(rng, L["light"]))
        if maybe(rng, 確率_詳細): parts.append(pick(rng, L["details"]))
        if maybe(rng, 確率_質感): parts.append(pick(rng, L["texture"]))
        if maybe(rng, 確率_天候_季節): parts.append(pick(rng, L["weather"]))
        if maybe(rng, 確率_時間帯): parts.append(pick(rng, L["time"]))
        if maybe(rng, 確率_効果_演出): parts.append(pick(rng, L["fx"]))
        if maybe(rng, 確率_建築_構造): parts.append(pick(rng, L["arch"]))
        if maybe(rng, 確率_小道具): parts.append(pick(rng, L["props"]))

        # ここから排他的なタグを削除する新しいロジック
        valid_parts = []
        exclusive_tags_to_remove = set()
        
        # 抽選されたタグを順に処理
        for p in parts:
            if not p:
                continue

            # 既に排他的なタグとしてマークされていればスキップ
            if p in exclusive_tags_to_remove:
                continue
            
            # タグが排他的なグループに属しているかチェック
            for group_name, exclusive_group in EXCLUSIVE_TAG_GROUPS.items():
                for sub_group in exclusive_group:
                    if p in sub_group:
                        # 属していれば、そのサブグループ内の他のタグを削除リストに追加
                        for tag_to_remove in sub_group:
                            if tag_to_remove != p:
                                exclusive_tags_to_remove.add(tag_to_remove)
            
            valid_parts.append(p)
        
        final_parts = [p for p in valid_parts if p not in exclusive_tags_to_remove]
        
        tag = join_clean(final_parts)
        tag = normalize(tag, 小文字化)
        tag = limit_len(tag, 最大文字数)
        
        return (tag,)

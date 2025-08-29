# background_tag.py
# 語彙の拡充、排他的なタグのグループ化、そして文字数を最大まで活用するロジックを追加

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
        
        # 抽選するカテゴリとその確率のリストを定義
        weighted_categories = [
            ("light", 確率_照明, L["light"]),
            ("details", 確率_詳細, L["details"]),
            ("texture", 確率_質感, L["texture"]),
            ("weather", 確率_天候_季節, L["weather"]),
            ("time", 確率_時間帯, L["time"]),
            ("fx", 確率_効果_演出, L["fx"]),
            ("arch", 確率_建築_構造, L["arch"]),
            ("props", 確率_小道具, L["props"]),
        ]
        
        # ランダムな順序でカテゴリをシャッフル
        rng.shuffle(weighted_categories)

        parts = list(env_parts)
        exclusive_tags_to_remove = set()
        
        # 初期タグの排他的なタグを削除リストに追加
        for p in parts:
            if p:
                exclusive_tags_to_remove.update(self._get_exclusive_tags(rng, [p]))

        # 1. 確率に基づいたタグの抽選
        tags_to_add = []
        for category_name, probability, vocab_list in weighted_categories:
            if not vocab_list:
                continue
            
            if maybe(rng, probability):
                selected_tag = pick(rng, vocab_list)
                if selected_tag and selected_tag not in exclusive_tags_to_remove:
                    tags_to_add.append(selected_tag)
                    # 排他的なタグを削除リストに追加
                    exclusive_tags_to_remove.update(self._get_exclusive_tags(rng, [selected_tag]))

        # 抽選されたタグを追加
        parts.extend(tags_to_add)

        # 2. 最大文字数に達するまでタグを追加
        all_categories = [
            L["light"], L["details"], L["texture"], L["weather"],
            L["time"], L["fx"], L["arch"], L["props"]
        ]
        
        flat_list = [item for sublist in all_categories for item in sublist]
        rng.shuffle(flat_list) # タグ全体をシャッフル

        for selected_tag in flat_list:
            if selected_tag and selected_tag not in parts and selected_tag not in exclusive_tags_to_remove:
                # タグを追加する前に文字数制限をチェック
                current_length = len(join_clean(parts))
                # +2はカンマとスペース
                if current_length + len(selected_tag) + 2 <= 最大文字数:
                    parts.append(selected_tag)
                    # 新しいタグの排他的なタグを削除リストに追加
                    exclusive_tags_to_remove.update(self._get_exclusive_tags(rng, [selected_tag]))
                else:
                    # 文字数制限を超えたら終了
                    break

        # 最終的なプロンプトの構築
        final_parts = [p for p in parts if p and p not in exclusive_tags_to_remove]
        
        tag = join_clean(final_parts)
        tag = normalize(tag, 小文字化)
        
        return (tag,)

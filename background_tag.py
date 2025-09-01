# background_tag.py
# 仕様書に基づき、環境フィルターとテーマ連動の抽選ロジックを実装

from .abg_util import rng_from_seed, maybe, pick, join_clean, normalize, merge_unique # <<< 変更点: util -> abg_util
from .vocab.background_vocab import (
    # --- 新しい構造に合わせてimport ---
    BG_ENV_INDOOR, BG_ENV_OUTDOOR, BG_DETAILS_INDOOR, BG_DETAILS_OUTDOOR,
    BG_ARCH_INDOOR, BG_ARCH_OUTDOOR, BG_PROPS_INDOOR, BG_PROPS_OUTDOOR,
    BG_LIGHT, BG_TEXTURE, BG_WEATHER, BG_TIME, BG_FX,
    THEME_PACKS, THEME_CHOICES, EXCLUSIVE_TAG_GROUPS
)

class BackgroundTagNode:
    # ... (クラスの残りの部分は変更ありません) ...
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
                "環境フィルター": (["指定しない", "屋内のみ", "屋外のみ"],),
                "小文字化": ("BOOL", {"default": True}),
                "確率_照明": ("FLOAT", {"default": 0.85, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_詳細": ("FLOAT", {"default": 0.75, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_質感": ("FLOAT", {"default": 0.65, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_天候_季節": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_時間帯": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_効果_演出": ("FLOAT", {"default": 0.6, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_建築_構造": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_小道具": ("FLOAT", {"default": 0.45, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def _get_exclusive_tags(self, rng, selected_tags: list) -> list:
        # この関数は変更なし
        exclusive_tags = set()
        for tag in selected_tags:
            for group in EXCLUSIVE_TAG_GROUPS.values():
                for sub_group in group:
                    if tag in sub_group:
                        exclusive_tags.update(t for t in sub_group if t != tag)
        return list(exclusive_tags)

    def _prepare_lists(self, theme_keys: list, filter_mode: str) -> dict:
        """
        環境フィルターに基づき、使用する語彙リストを動的に構築する
        """
        CATEGORIES = ["env", "light", "details", "texture", "weather", "time", "fx", "arch", "props"]
        L = {cat: [] for cat in CATEGORIES}

        # ベースとなる語彙を辞書として定義
        base_vocab = {
            "env_indoor": BG_ENV_INDOOR, "env_outdoor": BG_ENV_OUTDOOR,
            "details_indoor": BG_DETAILS_INDOOR, "details_outdoor": BG_DETAILS_OUTDOOR,
            "arch_indoor": BG_ARCH_INDOOR, "arch_outdoor": BG_ARCH_OUTDOOR,
            "props_indoor": BG_PROPS_INDOOR, "props_outdoor": BG_PROPS_OUTDOOR,
            "light": BG_LIGHT, "texture": BG_TEXTURE, "weather": BG_WEATHER,
            "time": BG_TIME, "fx": BG_FX
        }

        # ベース語彙と選択されたテーマの語彙をリスト化
        vocab_sources = [base_vocab] + [THEME_PACKS.get(key, {}) for key in theme_keys]
        
        # 各ソース（ベース語彙、テーマ）から語彙をマージ
        for source in vocab_sources:
            for cat in CATEGORIES:
                is_indoor_ok = filter_mode != "屋外のみ"
                is_outdoor_ok = filter_mode != "屋内のみ"

                # 共通カテゴリ（例: light, texture）
                if source.get(cat):
                    L[cat] = merge_unique(L[cat], source.get(cat, []))
                # 屋内用カテゴリ
                if is_indoor_ok and source.get(f"{cat}_indoor"):
                    L[cat] = merge_unique(L[cat], source.get(f"{cat}_indoor", []))
                # 屋外用カテゴリ
                if is_outdoor_ok and source.get(f"{cat}_outdoor"):
                    L[cat] = merge_unique(L[cat], source.get(f"{cat}_outdoor", []))
        return L

    def generate(
        self, seed, テーマ1="none", テーマ2="none", テーマ3="none",
        環境フィルター="指定しない", 小文字化=True,
        確率_照明=0.85, 確率_詳細=0.75, 確率_質感=0.65, 確率_天候_季節=0.5, 
        確率_時間帯=0.7, 確率_効果_演出=0.6, 確率_建築_構造=0.5, 確率_小道具=0.45,
    ):
        rng = rng_from_seed(seed)

        # --- テーマ選択ロジック（「おまかせ」対応） ---
        selected_options = [k for k in [テーマ1, テーマ2, テーマ3] if k and k != "none"]
        final_theme_keys = [t for t in selected_options if t != "おまかせ"]
        omakase_count = selected_options.count("おまかせ")
        
        if omakase_count > 0:
            available_for_random = [t for t in THEME_PACKS.keys() if t not in final_theme_keys]
            rng.shuffle(available_for_random)
            for _ in range(omakase_count):
                if not available_for_random: break
                final_theme_keys.append(available_for_random.pop())
        # 重複を除去しつつ順序を維持
        theme_keys = list(dict.fromkeys(final_theme_keys))
        
        # フィルターを適用して語彙リストを準備
        L = self._prepare_lists(theme_keys, 環境フィルター)

        # --- 新しい抽選ロジック ---
        # デフォルトの抽選回数
        DEFAULT_DRAW_COUNTS = {"env": 1, "light": 1, "details": 2, "texture": 1, "weather": 1, "time": 1, "fx": 1, "arch": 1, "props": 1}
        # テーマ選択時に抽選回数を増やすカテゴリ
        THEME_BOOST_COUNTS = {"env": 1, "light": 1, "details": 2, "texture": 1, "arch": 2, "props": 2}
        
        draw_counts = DEFAULT_DRAW_COUNTS.copy()
        if theme_keys:
            # テーマが1つでも選択されていればブースト
            for category, boost in THEME_BOOST_COUNTS.items():
                draw_counts[category] = draw_counts.get(category, 0) + boost

        # 各カテゴリの確率と語彙リストをマッピング
        weighted_categories = {
            "env": (1.0, L["env"]), "light": (確率_照明, L["light"]), "details": (確率_詳細, L["details"]),
            "texture": (確率_質感, L["texture"]), "weather": (確率_天候_季節, L["weather"]), "time": (確率_時間帯, L["time"]),
            "fx": (確率_効果_演出, L["fx"]), "arch": (確率_建築_構造, L["arch"]), "props": (確率_小道具, L["props"]),
        }

        parts = []
        exclusive_tags_to_remove = set()
        
        # 抽選対象となるカテゴリをプール化
        candidate_pool = [cat for cat, count in draw_counts.items() for _ in range(count)]
        rng.shuffle(candidate_pool)

        for category_name in candidate_pool:
            probability, vocab_list = weighted_categories.get(category_name, (0, []))
            if not vocab_list or not maybe(rng, probability):
                continue
            
            # まだ選ばれておらず、排他リストにもないタグのみを抽選対象とする
            available_tags = [t for t in vocab_list if t not in parts and t not in exclusive_tags_to_remove]
            if not available_tags:
                continue
            
            selected_tag = pick(rng, available_tags)
            if selected_tag:
                parts.append(selected_tag)
                exclusive_tags_to_remove.update(self._get_exclusive_tags(rng, [selected_tag]))

        # 環境タグが万一選ばれなかった場合のフォールバック
        if not any(tag in L["env"] for tag in parts if tag) and L["env"]:
            fallback = pick(rng, L["env"])
            if fallback:
                parts.insert(0, fallback)

        # 最終的なプロンプトを構築
        final_parts = [p for p in parts if p and p not in exclusive_tags_to_remove]
        tag = join_clean(final_parts)
        tag = normalize(tag, 小文字化)
        
        return (tag,)


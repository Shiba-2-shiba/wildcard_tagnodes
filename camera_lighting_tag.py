# camera_lighting_tag.py
# カメラアングル + ライティング統合タグ生成ノード
# - 主役モード: 「女性(=portrait)」「風景(=landscape)」
# - 露骨な機材語の混入をBAN_REPLACEで置換して安全化
# 依存:
#   from .util import rng_from_seed, maybe, pick, join_clean, limit_len, normalize
#   from .vocab.camera_lighting_vocab import (...)  # 下記参照

from .util import rng_from_seed, maybe, pick, join_clean, limit_len, normalize
from .vocab.camera_lighting_vocab import (
    COMMON_ANGLES, PORTRAIT_SHOTS, LANDSCAPE_SHOTS,
    LIGHT_STYLES_SAFE, LIGHT_DIRECTIONS_SAFE, LIGHT_TIMES, LIGHT_COLORS,
    PORTRAIT_EROTIC_TONE,  # 汎用（フォールバック用）
    PORTRAIT_EROTIC_TONE_TIER1, PORTRAIT_EROTIC_TONE_TIER2, PORTRAIT_EROTIC_TONE_TIER3,
    LANDSCAPE_GRANDEUR_TONE,
    BAN_REPLACE
)

MODE_MAP_JP = {"女性": "portrait", "風景": "landscape"}
官能LEVEL_CHOICES = ["控えめ (Tier1)", "強め (Tier2)", "濃厚 (Tier3)"]

class CameraLightingTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31 - 1}),
            },
            "optional": {
                "主役": (list(MODE_MAP_JP.keys()), {"default": "女性"}),
                "最大文字数": ("INT", {"default": 120, "min": 0, "max": 4096}),
                "小文字化": ("BOOL", {"default": True}),

                # 確率スライダ（clothing_tagの操作感を踏襲）
                "確率: 角度": ("FLOAT", {"default": 0.75, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: ショット": ("FLOAT", {"default": 0.95, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: ライト方向": ("FLOAT", {"default": 0.65, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 時間帯": ("FLOAT", {"default": 0.55, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 色味": ("FLOAT", {"default": 0.45, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 雰囲気補強": ("FLOAT", {"default": 0.75, "min": 0.0, "max": 1.0, "step": 0.01}),

                # 女性モード専用（官能段階と採用確率）
                "官能レベル(女性)": (官能LEVEL_CHOICES, {"default": "強め (Tier2)"}),
                "確率: 官能タグ(女性)": ("FLOAT", {"default": 0.85, "min": 0.0, "max": 1.0, "step": 0.01}),

                # 風景モード専用（雄大さブースト）
                "雄大さ強調(風景)": ("FLOAT", {"default": 0.85, "min": 0.0, "max": 1.0, "step": 0.05}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    # ---- 内部: 禁止語の置換（安全化）----
    def _sanitize(self, text: str) -> str:
        if not text:
            return text
        t = text
        low = t.lower()
        for bad, rep in BAN_REPLACE.items():
            if bad in low:
                # 大文字小文字の差異を気にせず、素直に3パターン置換
                t = t.replace(bad, rep).replace(bad.title(), rep).replace(bad.upper(), rep)
                low = t.lower()
        return t

    # ---- 内部: モード別ショット選択 ----
    def _pick_shot_by_mode(self, rng, mode: str, p_shot: float):
        if mode == "portrait":
            return pick(rng, PORTRAIT_SHOTS) if maybe(rng, p_shot) else None
        else:
            return pick(rng, LANDSCAPE_SHOTS) if maybe(rng, p_shot) else None

    # ---- 内部: 官能トーン選択（段階制）----
    def _pick_erotic_tone(self, rng, level: str):
        if "Tier3" in level:
            pool = PORTRAIT_EROTIC_TONE_TIER3 + PORTRAIT_EROTIC_TONE_TIER2
        elif "Tier2" in level:
            pool = PORTRAIT_EROTIC_TONE_TIER2 + PORTRAIT_EROTIC_TONE_TIER1
        else:
            pool = PORTRAIT_EROTIC_TONE_TIER1
        # バリエーション確保のため汎用も混ぜる
        pool = pool + PORTRAIT_EROTIC_TONE
        return pick(rng, pool)

    # ---- 内部: モード別の「雰囲気補強」選択 ----
    def _tone_by_mode(self, rng, mode: str, p_tone: float,
                      erotic_level: str, p_erotic: float,
                      grandeur_boost: float):
        if mode == "portrait":
            # 官能トーンは独立確率で採用
            if maybe(rng, min(1.0, p_erotic)):
                return self._pick_erotic_tone(rng, erotic_level)
            # 官能を使わない場合は汎用トーンを低確率で
            return pick(rng, PORTRAIT_EROTIC_TONE) if maybe(rng, p_tone * 0.5) else None
        else:
            prob = min(1.0, p_tone * (0.6 + 0.4 * max(0.0, min(1.0, grandeur_boost))))
            return pick(rng, LANDSCAPE_GRANDEUR_TONE) if maybe(rng, prob) else None

    # ---- 生成本体 ----
    def generate(self, seed,
                 主役="女性", 最大文字数=120, 小文字化=True,
                 確率_角度=0.75, 確率_ショット=0.95, 確率_ライト方向=0.65,
                 確率_時間帯=0.55, 確率_色味=0.45, 確率_雰囲気補強=0.75,
                 官能レベル_女性="強め (Tier2)", 確率_官能タグ_女性=0.85,
                 雄大さ強調_風景=0.85, **kwargs):

        rng = rng_from_seed(seed)
        mode = MODE_MAP_JP.get(主役, "portrait")

        # コア要素
        angle = pick(rng, COMMON_ANGLES) if maybe(rng, 確率_角度) else None
        shot  = self._pick_shot_by_mode(rng, mode, 確率_ショット)
        style = pick(rng, LIGHT_STYLES_SAFE)  # スタイルは常時1要素で簡潔に
        direction = pick(rng, LIGHT_DIRECTIONS_SAFE) if maybe(rng, 確率_ライト方向) else None
        time = pick(rng, LIGHT_TIMES) if maybe(rng, 確率_時間帯) else None
        color = pick(rng, LIGHT_COLORS) if maybe(rng, 確率_色味) else None

        # モード別トーン
        tone = self._tone_by_mode(
            rng, mode, 確率_雰囲気補強,
            erotic_level=官能レベル_女性, p_erotic=確率_官能タグ_女性,
            grandeur_boost=雄大さ強調_風景
        )

        # 出力（時間/色, スタイル, 方向, 角度/ショット, トーン）
        parts = [time, color, style, direction, angle, shot, tone]
        tag = join_clean(parts)

        tag = self._sanitize(tag)           # 禁止語の最終チェック
        tag = normalize(tag, 小文字化)
        tag = limit_len(tag, 最大文字数)
        return (tag,)



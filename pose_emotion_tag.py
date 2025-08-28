# pose_emotion_tag.py (改訂版)
# 新しい語彙体系 (improved_pose_emotion_vocab.py) に完全対応。
# - 排他タググループ機能の実装
# - 感情テーマパックのブースト機能
# - UIのシンプル化とロジックの刷新

from typing import Dict, List, Set, Tuple
import re
from .util import rng_from_seed, maybe, pick, join_clean, limit_len, normalize, merge_unique

# [更新] 新しい語彙ファイルをインポート
from .vocab.pose_emotion_vocab import (
    # 基本語彙
    VIEW_ANGLES, VIEW_FRAMING,
    POSE_STANDING, POSE_SITTING, POSE_LYING, POSE_DYNAMIC,
    HAND_POSITIONS, HAND_GESTURES, SPINE_AND_SHOULDERS, LEG_POSITIONS,
    MOUTH_BASE, EYES_BASE, BROWS_BASE, EFFECTS,
    # 感情モードとテーマ
    EXPRESSION_MODES, EMOTION_THEME_PACKS,
    # 排他グループ
    EXCLUSIVE_TAG_GROUPS,
    # NSFW関連
    EXTRA_NSFW_POSE, EXTRA_NSFW_EXPR, EXPLICIT_BLOCKLIST,
)

# ===== 日本語UIマップ =====
# [更新] 新しい感情モードを追加
EXPR_MODE_JP = {
    "日常": "daily", "魅惑": "allure", "喜び": "joy",
    "悲しみ": "sadness", "怒り": "anger", "官能": "erotic",
}
# [更新] テーマパックのキーを動的に取得
THEME_PACK_JP = {name.replace("_", " "): name for name in EMOTION_THEME_PACKS.keys()}
THEME_PACK_JP["なし"] = "none" # デフォルト値

COMPLEXITY_JP = {"単純": "simple", "標準": "normal", "複雑": "complex"}
NSFW_JP = {"オフ": "off", "アダルト寄り(非露骨)": "suggestive", "アダルト(露骨フィルタ)": "explicit"}

# ===== 確率プロファイル関数 =====
# [更新] UIのシンプル化に伴い、プロファイルを簡素化
def _complexity_profile(level: str) -> Dict[str, float]:
    # 各カテゴリの基本出現確率
    base = dict(view=0.8, full_body=1.0, upper_body=0.8, lower_body=0.6, expression=1.0, effects=0.5)
    if level == "simple":
        base.update(view=0.5, upper_body=0.5, lower_body=0.3, effects=0.2)
    elif level == "complex":
        base.update(view=0.95, upper_body=0.95, lower_body=0.8, effects=0.7)
    return base

# ===== 語彙プール準備関数 =====
# [新規] NSFWレベルに応じて語彙プールを拡張する
def _get_vocab_pools(nsfw_level: str) -> Dict[str, List[str]]:
    pools = {
        "view": _merge_unique(VIEW_ANGLES, VIEW_FRAMING),
        "pose_standing": POSE_STANDING[:],
        "pose_sitting": POSE_SITTING[:],
        "pose_lying": POSE_LYING[:],
        "pose_dynamic": POSE_DYNAMIC[:],
        "upper_body": _merge_unique(HAND_POSITIONS, HAND_GESTURES, SPINE_AND_SHOULDERS),
        "lower_body": LEG_POSITIONS[:],
        "mouth": MOUTH_BASE[:],
        "eyes": EYES_BASE[:],
        "brows": BROWS_BASE[:],
        "effects": EFFECTS[:],
    }
    # 感情モードごとの語彙を追加
    for mode, data in EXPRESSION_MODES.items():
        pools[f"mood_{mode}"] = data["mood"]

    if nsfw_level in ["suggestive", "explicit"]:
        # サジェスティブな語彙を追加 (suggestive, explicit共通)
        pools["upper_body"].extend(EXTRA_NSFW_POSE) # 手や体幹のポーズに統合
        pools["lower_body"].extend(EXTRA_NSFW_POSE) # 脚のポーズに統合
        for mode in ["allure", "erotic"]:
            pools[f"mood_{mode}"].extend(EXTRA_NSFW_EXPR)
        pools["effects"].extend(EXTRA_NSFW_EXPR)

    if nsfw_level == "explicit":
        # 露骨な語彙を追加 (explicitのみ)
        # 注意: これらは最終的に _sanitize でフィルタリングされる可能性がある
        pools["pose_dynamic"].extend(EXPLICIT_SEX_POSES)
        pools["mood_erotic"].extend(EXPLICIT_SEX_LEXICON)

    return pools

# ===== サニタイズ関数 =====
_BLOCK_PATTERNS = None
def _compile_block_patterns():
    global _BLOCK_PATTERNS
    if _BLOCK_PATTERNS is None:
        if not EXPLICIT_BLOCKLIST:
            _BLOCK_PATTERNS = False
            return _BLOCK_PATTERNS
        terms = sorted(EXPLICIT_BLOCKLIST, key=lambda s: (-len(s), s))
        pat = r"|".join(re.escape(t) for t in terms if t)
        _BLOCK_PATTERNS = re.compile(pat, re.IGNORECASE) if pat else False
    return _BLOCK_PATTERNS

def _sanitize(seq: List[str]) -> List[str]:
    pat = _compile_block_patterns()
    if not pat:
        return [s.strip() for s in seq if s and s.strip()]
    return [s.strip() for s in seq if s and s.strip() and not pat.search(s)]

# ===== タグ生成コア関数 =====
# [ロジック刷新] 排他グループとテーマパックを処理する新しいコア関数
def _compose(rng, probs: Dict[str, float], pools: Dict[str, List[str]],
             expr_mode: str, theme: str, gaze_target: str) -> str:

    chosen_tags: List[str] = []
    used_exclusive_groups: Set[str] = set()
    
    # 逆引き辞書を作成して、どのタグがどのグループに属するかを高速に引けるようにする
    tag_to_group_map: Dict[str, str] = {
        tag: group_name
        for group_name, tags in EXCLUSIVE_TAG_GROUPS.items()
        for tag in tags
    }

    def _handle_exclusive_selection(pool: List[str]) -> str | None:
        """排他グループを考慮してタグを一つ選択する"""
        # プール内のタグが属する可能性のあるグループを特定
        possible_groups = {tag_to_group_map.get(tag) for tag in pool if tag_to_group_map.get(tag)}
        
        # 既に使われたグループに属するタグは選択肢から除外
        available_pool = [
            tag for tag in pool
            if tag_to_group_map.get(tag) not in used_exclusive_groups
        ]
        
        if not available_pool:
            return None

        # タグを選択
        tag = pick(rng, available_pool)
        if tag:
            # タグが属するグループを特定し、使用済みとしてマーク
            group = tag_to_group_map.get(tag)
            if group:
                used_exclusive_groups.add(group)
        return tag

    # 1. テーマパックによるブースト
    if theme != "none" and theme in EMOTION_THEME_PACKS:
        pack = EMOTION_THEME_PACKS[theme]
        chosen_tags.extend(pack.get("pose_boost", []))
        chosen_tags.extend(pack.get("expr_boost", []))
        chosen_tags.extend(pack.get("camera_boost", []))
        # ブーストで追加されたタグの排他グループを使用済みにする
        for tag in chosen_tags:
            group = tag_to_group_map.get(tag)
            if group:
                used_exclusive_groups.add(group)

    # 2. ポーズの選択
    if maybe(rng, probs["full_body"]):
        # 4つの全身ポーズカテゴリから1つだけを選択する
        posture_category = pick(rng, ["pose_standing", "pose_sitting", "pose_lying", "pose_dynamic"])
        tag = _handle_exclusive_selection(pools[posture_category])
        if tag: chosen_tags.append(tag)

    if maybe(rng, probs["upper_body"]):
        tag = _handle_exclusive_selection(pools["upper_body"])
        if tag: chosen_tags.append(tag)

    if maybe(rng, probs["lower_body"]):
        tag = _handle_exclusive_selection(pools["lower_body"])
        if tag: chosen_tags.append(tag)
        
    if maybe(rng, probs["view"]):
        tag = _handle_exclusive_selection(pools["view"])
        if tag: chosen_tags.append(tag)

    # 3. 表情の選択
    if maybe(rng, probs["expression"]):
        chosen_tags.append(pick(rng, pools["mouth"]))
        chosen_tags.append(pick(rng, pools["eyes"]))
        if maybe(rng, 0.6): chosen_tags.append(pick(rng, pools["brows"]))
        
        # 視線ターゲットの処理
        if gaze_target != "自動":
            # "closed" は排他グループではない特別なケース
            if gaze_target == "closed":
                chosen_tags.append("closed eyes")
            else:
                tag = gaze_target
                group = tag_to_group_map.get(tag)
                if group not in used_exclusive_groups:
                    chosen_tags.append(tag)
                    if group: used_exclusive_groups.add(group)
        else:
            # 自動の場合は排他性を考慮して選択
             tag = _handle_exclusive_selection(pools["eyes"]) # gazeはeyesプールの一部
             if tag: chosen_tags.append(tag)


        # 感情ムードの選択
        mood_pool = pools.get(f"mood_{expr_mode}", [])
        if mood_pool:
            chosen_tags.append(pick(rng, mood_pool))

    # 4. エフェクト
    if maybe(rng, probs["effects"]):
        chosen_tags.append(pick(rng, pools["effects"]))

    # 最終的なサニタイズと結合
    unique_tags = merge_unique(chosen_tags)
    sanitized_tags = _sanitize(unique_tags)
    return join_clean(sanitized_tags)


# ===== ComfyUIノードクラス =====
class PoseEmotionTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31 - 1}),
                # [更新] UI項目を刷新
                "表情モード": (list(EXPR_MODE_JP.keys()), {"default": "日常"}),
                "構図の複雑さ": (list(COMPLEXITY_JP.keys()), {"default": "標準"}),
                "アダルト表現": (list(NSFW_JP.keys()), {"default": "オフ"}),
                "テーマ": (list(THEME_PACK_JP.keys()), {"default": "なし"}),
                "視線ターゲット": (["自動", "looking at viewer", "looking away", "looking up", "downcast gaze", "side glance", "closed"], {"default": "自動"}),
                "最大文字数": ("INT", {"default": 160, "min": 0, "max": 4096}),
                "小文字化": ("BOOL", {"default": True}),
            },
            "optional": {
                # [更新] 確率スライダーをカテゴリベースに集約
                "確率: 全身ポーズ": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05}),
                "確率: 上半身": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05}),
                "確率: 下半身": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05}),
                "確率: 視点/構図": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05}),
                "確率: 表情": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05}),
                "確率: エフェクト": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.05}),
            }
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "tagging"

    def generate(self, seed, **kwargs):
        rng = rng_from_seed(seed)
        expr_mode = EXPR_MODE_JP.get(kwargs.get("表情モード", "日常"), "daily")
        complexity = COMPLEXITY_JP.get(kwargs.get("構図の複雑さ", "標準"), "normal")
        nsfw_level = NSFW_JP.get(kwargs.get("アダルト表現", "オフ"), "off")
        theme = THEME_PACK_JP.get(kwargs.get("テーマ", "なし"), "none")
        gaze_target = kwargs.get("視線ターゲット", "自動")
        max_len = int(kwargs.get("最大文字数", 160))
        lowercase = bool(kwargs.get("小文字化", True))

        # 確率プロファイルとUIからの倍率を適用
        base_probs = _complexity_profile(complexity)
        probs = {
            "full_body":  base_probs["full_body"]  * kwargs.get("確率: 全身ポーズ", 1.0),
            "upper_body": base_probs["upper_body"] * kwargs.get("確率: 上半身", 1.0),
            "lower_body": base_probs["lower_body"] * kwargs.get("確率: 下半身", 1.0),
            "view":       base_probs["view"]       * kwargs.get("確率: 視点/構図", 1.0),
            "expression": base_probs["expression"] * kwargs.get("確率: 表情", 1.0),
            "effects":    base_probs["effects"]    * kwargs.get("確率: エフェクト", 1.0),
        }

        # 語彙プールを取得
        pools = _get_vocab_pools(nsfw_level)

        # タグを生成
        tag = _compose(rng, probs, pools, expr_mode, theme, gaze_target)
        tag = normalize(tag, lowercase)
        tag = limit_len(tag, max_len)

        return (tag,)

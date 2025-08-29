# pose_emotion_tag.py (改訂版)
# 新しい語彙体系 (improved_pose_emotion_vocab.py) に完全対応。
# - 排他タググループ機能の実装
# - 感情テーマパックのブースト機能
# - UIのシンプル化とロジックの刷新
# - [改良] 最大文字数までタグを充填する機能を追加

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
EXPR_MODE_JP = {
    "日常": "daily", "魅惑": "allure", "喜び": "joy",
    "悲しみ": "sadness", "怒り": "anger", "官能": "erotic",
}
THEME_PACK_JP = {name.replace("_", " "): name for name in EMOTION_THEME_PACKS.keys()}
THEME_PACK_JP["なし"] = "none"

COMPLEXITY_JP = {"単純": "simple", "標準": "normal", "複雑": "complex"}
NSFW_JP = {"オフ": "off", "アダルト寄り(非露骨)": "suggestive", "アダルト(露骨フィルタ)": "explicit"}

# ===== 確率プロファイル関数 =====
def _complexity_profile(level: str) -> Dict[str, float]:
    base = dict(view=0.8, full_body=1.0, upper_body=0.8, lower_body=0.6, expression=1.0, effects=0.5)
    if level == "simple":
        base.update(view=0.5, upper_body=0.5, lower_body=0.3, effects=0.2)
    elif level == "complex":
        base.update(view=0.95, upper_body=0.95, lower_body=0.8, effects=0.7)
    return base

# ===== 語彙プール準備関数 =====
def _get_vocab_pools(nsfw_level: str) -> Dict[str, List[str]]:
    try:
        from .vocab.pose_emotion_vocab import EXPLICIT_SEX_POSES, EXPLICIT_SEX_LEXICON
    except ImportError:
        EXPLICIT_SEX_POSES = []
        EXPLICIT_SEX_LEXICON = []
        
    pools = {
        "view": merge_unique(VIEW_ANGLES, VIEW_FRAMING),
        "pose_standing": POSE_STANDING[:], "pose_sitting": POSE_SITTING[:],
        "pose_lying": POSE_LYING[:], "pose_dynamic": POSE_DYNAMIC[:],
        "upper_body": merge_unique(HAND_POSITIONS, HAND_GESTURES, SPINE_AND_SHOULDERS),
        "lower_body": LEG_POSITIONS[:], "mouth": MOUTH_BASE[:],
        "eyes": EYES_BASE[:], "brows": BROWS_BASE[:], "effects": EFFECTS[:],
    }
    for mode, data in EXPRESSION_MODES.items():
        pools[f"mood_{mode}"] = data["mood"]

    if nsfw_level in ["suggestive", "explicit"]:
        pools["upper_body"].extend(EXTRA_NSFW_POSE)
        pools["lower_body"].extend(EXTRA_NSFW_POSE)
        for mode in ["allure", "erotic"]:
            pools[f"mood_{mode}"].extend(EXTRA_NSFW_EXPR)
        pools["effects"].extend(EXTRA_NSFW_EXPR)

    if nsfw_level == "explicit":
        pools["pose_dynamic"].extend(EXPLICIT_SEX_POSES)
        pools["mood_erotic"].extend(EXPLICIT_SEX_LEXICON)
    return pools

# ===== サニタイズ関数 =====
_BLOCK_PATTERNS = None
def _compile_block_patterns():
    global _BLOCK_PATTERNS
    if _BLOCK_PATTERNS is None:
        if not EXPLICIT_BLOCKLIST:
            _BLOCK_PATTERNS = False; return
        terms = sorted(EXPLICIT_BLOCKLIST, key=lambda s: (-len(s), s))
        pat = r"|".join(re.escape(t) for t in terms if t)
        _BLOCK_PATTERNS = re.compile(pat, re.IGNORECASE) if pat else False
    return _BLOCK_PATTERNS

def _sanitize(seq: List[str]) -> List[str]:
    pat = _compile_block_patterns()
    if not pat: return [s.strip() for s in seq if s and s.strip()]
    return [s.strip() for s in seq if s and s.strip() and not pat.search(s)]

# ===== タグ生成コア関数 =====
# [修正] 戻り値を (タグのリスト, 使用済み排他グループのセット) に変更
def _compose(rng, probs: Dict[str, float], pools: Dict[str, List[str]],
             expr_mode: str, theme: str, gaze_target: str,
             tag_to_group_map: Dict[str, str]) -> Tuple[List[str], Set[str]]:

    chosen_tags: List[str] = []
    used_exclusive_groups: Set[str] = set()

    def _handle_exclusive_selection(pool: List[str]) -> str | None:
        available_pool = [t for t in pool if tag_to_group_map.get(t) not in used_exclusive_groups]
        if not available_pool: return None
        tag = pick(rng, available_pool)
        if tag:
            group = tag_to_group_map.get(tag)
            if group: used_exclusive_groups.add(group)
        return tag

    if theme != "none" and theme in EMOTION_THEME_PACKS:
        pack = EMOTION_THEME_PACKS[theme]
        boost_tags = pack.get("pose_boost", []) + pack.get("expr_boost", []) + pack.get("camera_boost", [])
        chosen_tags.extend(boost_tags)
        for tag in boost_tags:
            group = tag_to_group_map.get(tag)
            if group: used_exclusive_groups.add(group)

    if maybe(rng, probs["full_body"]):
        cat = pick(rng, ["pose_standing", "pose_sitting", "pose_lying", "pose_dynamic"])
        if tag := _handle_exclusive_selection(pools[cat]): chosen_tags.append(tag)
    if maybe(rng, probs["upper_body"]):
        if tag := _handle_exclusive_selection(pools["upper_body"]): chosen_tags.append(tag)
    if maybe(rng, probs["lower_body"]):
        if tag := _handle_exclusive_selection(pools["lower_body"]): chosen_tags.append(tag)
    if maybe(rng, probs["view"]):
        if tag := _handle_exclusive_selection(pools["view"]): chosen_tags.append(tag)

    if maybe(rng, probs["expression"]):
        chosen_tags.append(pick(rng, pools["mouth"]))
        chosen_tags.append(pick(rng, pools["eyes"]))
        if maybe(rng, 0.6): chosen_tags.append(pick(rng, pools["brows"]))
        
        if gaze_target != "自動":
            if gaze_target == "closed": chosen_tags.append("closed eyes")
            else:
                group = tag_to_group_map.get(gaze_target)
                if group not in used_exclusive_groups:
                    chosen_tags.append(gaze_target)
                    if group: used_exclusive_groups.add(group)
        else:
            if tag := _handle_exclusive_selection(pools["eyes"]): chosen_tags.append(tag)

        if mood_pool := pools.get(f"mood_{expr_mode}", []):
            chosen_tags.append(pick(rng, mood_pool))

    if maybe(rng, probs["effects"]):
        chosen_tags.append(pick(rng, pools["effects"]))

    unique_tags = merge_unique(*[chosen_tags])
    sanitized_tags = _sanitize(unique_tags)
    return sanitized_tags, used_exclusive_groups


# ===== ComfyUIノードクラス =====
class PoseEmotionTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31 - 1}),
                "表情モード": (list(EXPR_MODE_JP.keys()), {"default": "日常"}),
                "構図の複雑さ": (list(COMPLEXITY_JP.keys()), {"default": "標準"}),
                "アダルト表現": (list(NSFW_JP.keys()), {"default": "オフ"}),
                "テーマ": (list(THEME_PACK_JP.keys()), {"default": "なし"}),
                "視線ターゲット": (["自動", "looking at viewer", "looking away", "looking up", "downcast gaze", "side glance", "closed"], {"default": "自動"}),
                "最大文字数": ("INT", {"default": 160, "min": 0, "max": 4096}),
            },
            "optional": {
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

    def generate(self, seed, 表情モード, 構図の複雑さ, アダルト表現, テーマ, 視線ターゲット, 最大文字数, **kwargs):
        rng = rng_from_seed(seed)
        expr_mode = EXPR_MODE_JP.get(表情モード, "daily")
        complexity = COMPLEXITY_JP.get(構図の複雑さ, "normal")
        nsfw_level = NSFW_JP.get(アダルト表現, "off")
        theme = THEME_PACK_JP.get(テーマ, "none")
        gaze_target = 視線ターゲット
        max_len = int(最大文字数)
        lowercase = True

        base_probs = _complexity_profile(complexity)
        probs = {
            "full_body":  base_probs["full_body"]  * kwargs.get("確率: 全身ポーズ", 1.0),
            "upper_body": base_probs["upper_body"] * kwargs.get("確率: 上半身", 1.0),
            "lower_body": base_probs["lower_body"] * kwargs.get("確率: 下半身", 1.0),
            "view":       base_probs["view"]       * kwargs.get("確率: 視点/構図", 1.0),
            "expression": base_probs["expression"] * kwargs.get("確率: 表情", 1.0),
            "effects":    base_probs["effects"]    * kwargs.get("確率: エフェクト", 1.0),
        }

        pools = _get_vocab_pools(nsfw_level)
        
        tag_to_group_map = {tag: name for name, tags in EXCLUSIVE_TAG_GROUPS.items() for tag in tags}

        # 1. 最初のタグセットを生成
        current_tags, used_groups = _compose(rng, probs, pools, expr_mode, theme, gaze_target, tag_to_group_map)

        # 2. [新規] 最大文字数までタグを充填
        # 全カテゴリの語彙を一つのリストにまとめ、シャッフルする
        fill_pool = [tag for pool in pools.values() for tag in pool]
        rng.shuffle(fill_pool)

        for candidate_tag in fill_pool:
            # 既に存在するタグ、または排他グループが使用済みのタグはスキップ
            if not candidate_tag or candidate_tag in current_tags:
                continue
            if tag_to_group_map.get(candidate_tag) in used_groups:
                continue

            # 追加後の文字列長をチェック (+2 は ", " の分)
            if len(join_clean(current_tags + [candidate_tag])) > max_len:
                continue

            # タグを追加し、使用済み排他グループを更新
            current_tags.append(candidate_tag)
            group = tag_to_group_map.get(candidate_tag)
            if group:
                used_groups.add(group)

        # 最終的な文字列を生成
        tag = join_clean(current_tags)
        tag = normalize(tag, lowercase)
        # 念のため最終的な文字数制限をかける
        tag = limit_len(tag, max_len)

        return (tag,)

from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from .util import rng_from_seed, maybe, pick, join_clean, limit_len, normalize, merge_unique

from .vocab.pose_emotion_vocab import (
    VIEW_ANGLES,
    VIEW_FRAMING,
    POSE_STANDING,
    POSE_SITTING,
    POSE_LYING,
    POSE_DYNAMIC,
    HAND_POSITIONS,
    HAND_GESTURES,
    SPINE_AND_SHOULDERS,
    LEG_POSITIONS,
    MOUTH_BASE,
    EYES_BASE,
    BROWS_BASE,
    EFFECTS,
    MOOD_JOY,
    MOOD_SADNESS,
    MOOD_ANGER,
    MOOD_NEUTRAL,
    MOOD_ALLURE,
    MOOD_EROTIC,
    EXPRESSION_MODES,
    EMOTION_THEME_PACKS,
    EXCLUSIVE_TAG_GROUPS,
    EXTRA_NSFW_POSE,
    EXTRA_NSFW_EXPR,
    EXPLICIT_BLOCKLIST,
)

# ===== 日本語UIマップ =====
EXPR_MODE_JP = {
    "日常": "daily",
    "魅惑": "allure",
    "喜び": "joy",
    "悲しみ": "sadness",
    "怒り": "anger",
    "官能": "erotic",
}
THEME_PACK_JP = {name.replace("_", " "): name for name in EMOTION_THEME_PACKS.keys()}
THEME_PACK_JP["なし"] = "none"

COMPLEXITY_JP = {"単純": "simple", "標準": "normal", "複雑": "complex"}
NSFW_JP = {"オフ": "off", "アダルト寄り(非露骨)": "suggestive", "アダルト(露骨フィルタ)": "explicit"}

# ===== 定数とテーマプロファイル =====
FULL_BODY_POOLS = ["pose_standing", "pose_sitting", "pose_dynamic", "pose_lying"]
EXPRESSION_POOLS = ["mouth", "eyes", "brows"]
HIGH_LEVEL_PRIORITY = ["camera", "full_body", "upper_body", "lower_body", "expression", "effects"]

MOOD_CATEGORIES: Dict[str, Sequence[str]] = {
    "joy": MOOD_JOY,
    "sadness": MOOD_SADNESS,
    "anger": MOOD_ANGER,
    "neutral": MOOD_NEUTRAL,
    "allure": MOOD_ALLURE,
    "erotic": MOOD_EROTIC,
}

MOOD_TAG_TO_LABEL: Dict[str, str] = {}
for label, tags in MOOD_CATEGORIES.items():
    for tag in tags:
        MOOD_TAG_TO_LABEL[tag] = label

CATEGORY_SOURCES: Dict[str, Sequence[str]] = {
    "view": merge_unique(VIEW_ANGLES, VIEW_FRAMING),
    "pose_standing": POSE_STANDING,
    "pose_sitting": POSE_SITTING,
    "pose_dynamic": POSE_DYNAMIC,
    "pose_lying": POSE_LYING,
    "upper_body": merge_unique(HAND_POSITIONS, HAND_GESTURES, SPINE_AND_SHOULDERS),
    "lower_body": LEG_POSITIONS,
    "mouth": MOUTH_BASE,
    "eyes": EYES_BASE,
    "brows": BROWS_BASE,
    "effects": EFFECTS,
}

BLOCKLIST_TERMS: Tuple[str, ...] = tuple(EXPLICIT_BLOCKLIST)


def _theme_tag_groups(theme_pack: Optional[Dict[str, object]]) -> List[Tuple[str, List[str]]]:
    groups: List[Tuple[str, List[str]]] = []
    if not theme_pack:
        return groups

    tags_section = theme_pack.get("tags", {}) if isinstance(theme_pack, dict) else {}
    if isinstance(tags_section, dict):
        for group_name, values in tags_section.items():
            if not values:
                continue
            cleaned = [tag for tag in values if tag]
            if cleaned:
                groups.append((group_name, cleaned))
    return groups


def _flatten_theme_tags(theme_pack: Optional[Dict[str, object]]) -> List[str]:
    if not theme_pack:
        return []
    return merge_unique(*[tags for _, tags in _theme_tag_groups(theme_pack)])


def _theme_profile_from_pack(theme_pack: Optional[Dict[str, object]]) -> Optional[Dict[str, object]]:
    if not theme_pack:
        return None

    focus = theme_pack.get("focus", {}) if isinstance(theme_pack, dict) else {}
    conflicts = theme_pack.get("conflicts", {}) if isinstance(theme_pack, dict) else {}

    pose_focus = list(focus.get("pose", [])) if isinstance(focus, dict) else []
    raw_expressions = focus.get("expression", []) if isinstance(focus, dict) else []
    if isinstance(raw_expressions, str):
        preferred_expressions = [raw_expressions]
    else:
        preferred_expressions = list(raw_expressions or [])

    pose_conflicts = set()
    mood_conflicts = set()
    camera_conflicts = set()
    blocked_tags = set()
    if isinstance(conflicts, dict):
        pose_conflicts = set(conflicts.get("pose_categories", []) or [])
        mood_conflicts = {str(label).lower() for label in conflicts.get("mood_labels", []) or []}
        camera_conflicts = {str(tag).lower() for tag in conflicts.get("camera_tags", []) or []}
        blocked_tags = {str(tag).lower() for tag in conflicts.get("tags", []) or []}

    return {
        "pose_focus": pose_focus,
        "preferred_expressions": preferred_expressions,
        "pose_conflicts": pose_conflicts,
        "mood_conflicts": mood_conflicts,
        "camera_conflicts": camera_conflicts,
        "blocked_tags": blocked_tags,
    }


def _high_level_for(category: Optional[str]) -> Optional[str]:
    if not category:
        return None
    if category == "view":
        return "camera"
    if category in {"upper_body"}:
        return "upper_body"
    if category in {"lower_body"}:
        return "lower_body"
    if category in {"mouth", "eyes", "brows"} or category.startswith("mood_"):
        return "expression"
    if category == "effects":
        return "effects"
    if category.startswith("pose_"):
        return "full_body"
    return None


def _complexity_profile(level: str) -> Dict[str, float]:
    base = dict(view=0.8, full_body=1.0, upper_body=0.8, lower_body=0.6, expression=1.0, effects=0.5)
    if level == "simple":
        base.update(view=0.5, upper_body=0.5, lower_body=0.3, effects=0.2)
    elif level == "complex":
        base.update(view=0.95, upper_body=0.95, lower_body=0.8, effects=0.7)
    return base


def _get_vocab_pools(nsfw_level: str) -> Tuple[Dict[str, List[str]], Dict[str, Set[str]]]:
    pools: Dict[str, List[str]] = {
        "view": list(CATEGORY_SOURCES["view"]),
        "pose_standing": list(CATEGORY_SOURCES["pose_standing"]),
        "pose_sitting": list(CATEGORY_SOURCES["pose_sitting"]),
        "pose_dynamic": list(CATEGORY_SOURCES["pose_dynamic"]),
        "pose_lying": list(CATEGORY_SOURCES["pose_lying"]),
        "upper_body": list(CATEGORY_SOURCES["upper_body"]),
        "lower_body": list(CATEGORY_SOURCES["lower_body"]),
        "mouth": list(CATEGORY_SOURCES["mouth"]),
        "eyes": list(CATEGORY_SOURCES["eyes"]),
        "brows": list(CATEGORY_SOURCES["brows"]),
        "effects": list(CATEGORY_SOURCES["effects"]),
    }

    for mode, data in EXPRESSION_MODES.items():
        pools[f"mood_{mode}"] = list(data.get("mood", []))

    if nsfw_level in {"suggestive", "explicit"}:
        pools["upper_body"].extend(EXTRA_NSFW_POSE)
        pools["lower_body"].extend(EXTRA_NSFW_POSE)
        for mode in ["allure", "erotic"]:
            pools.setdefault(f"mood_{mode}", [])
            pools[f"mood_{mode}"].extend(EXTRA_NSFW_EXPR)
        pools["effects"].extend(EXTRA_NSFW_EXPR)

    tag_category_map: Dict[str, Set[str]] = {}

    def _register(category: str, tags: Iterable[str]) -> None:
        for tag in tags:
            if not tag:
                continue
            tag_category_map.setdefault(tag, set()).add(category)

    for category, tags in pools.items():
        _register(category, tags)

    return pools, tag_category_map


def _build_theme_bias(theme_pack: Optional[Dict[str, object]], pools: Dict[str, List[str]]) -> Dict[str, List[str]]:
    bias: Dict[str, List[str]] = {name: [] for name in pools.keys()}
    if not theme_pack:
        return bias

    for _, tags in _theme_tag_groups(theme_pack):
        for tag in tags:
            for pool_name, pool in pools.items():
                if tag in pool and tag not in bias[pool_name]:
                    bias[pool_name].append(tag)
    return bias


def _primary_pool_for_tag(tag: str, tag_category_map: Dict[str, Set[str]]) -> Optional[str]:
    categories = list(tag_category_map.get(tag, []))
    if not categories:
        return None
    preferred_order = ["view"] + FULL_BODY_POOLS + ["upper_body", "lower_body", "eyes", "mouth", "brows", "effects"]
    for candidate in preferred_order:
        if candidate in categories:
            return candidate
    return categories[0]


def _is_blocked_tag(tag: str, nsfw_level: str) -> bool:
    if nsfw_level == "explicit":
        return False
    lowered = tag.strip().lower()
    for blocked in BLOCKLIST_TERMS:
        if blocked in lowered:
            return True
    return False


def _is_conflicting_with_theme(
    tag: str,
    pool_name: Optional[str],
    theme_profile: Optional[Dict[str, object]],
    tag_category_map: Dict[str, Set[str]],
) -> bool:
    if not theme_profile:
        return False

    lowered = tag.lower()
    blocked_tags = theme_profile.get("blocked_tags")
    if blocked_tags and lowered in blocked_tags:
        return True

    mood_label = MOOD_TAG_TO_LABEL.get(tag)
    mood_conflicts = theme_profile.get("mood_conflicts") or set()
    if mood_label and mood_label in mood_conflicts:
        return True

    pose_conflicts: Set[str] = set(theme_profile.get("pose_conflicts", set()))
    if pose_conflicts:
        for category in tag_category_map.get(tag, set()):
            if category in pose_conflicts:
                return True

    camera_conflicts: Set[str] = set(theme_profile.get("camera_conflicts", set()))
    if pool_name == "view" and camera_conflicts:
        if any(keyword in lowered for keyword in camera_conflicts):
            return True
    return False


def _can_use_tag(
    tag: str,
    pool_name: Optional[str],
    selected_tags: List[str],
    used_groups: Set[str],
    nsfw_level: str,
    theme_profile: Optional[Dict[str, object]],
    tag_to_group_map: Dict[str, str],
    tag_category_map: Dict[str, Set[str]],
) -> bool:
    if not tag or tag in selected_tags:
        return False
    if _is_blocked_tag(tag, nsfw_level):
        return False
    if _is_conflicting_with_theme(tag, pool_name, theme_profile, tag_category_map):
        return False
    group = tag_to_group_map.get(tag)
    if group and group in used_groups:
        return False
    return True


def _try_add_tag(
    tag: Optional[str],
    pool_name: Optional[str],
    selected_tags: List[str],
    used_groups: Set[str],
    used_high_level: Set[str],
    nsfw_level: str,
    theme_profile: Optional[Dict[str, object]],
    tag_to_group_map: Dict[str, str],
    tag_category_map: Dict[str, Set[str]],
    max_len: Optional[int] = None,
) -> bool:
    if not tag:
        return False
    if not _can_use_tag(tag, pool_name, selected_tags, used_groups, nsfw_level, theme_profile, tag_to_group_map, tag_category_map):
        return False

    if max_len is not None:
        prospective = selected_tags + [tag]
        if len(join_clean(prospective)) > max_len:
            return False

    selected_tags.append(tag)
    group = tag_to_group_map.get(tag)
    if group:
        used_groups.add(group)
    for category in tag_category_map.get(tag, set()):
        high = _high_level_for(category)
        if high:
            used_high_level.add(high)
    return True


def _select_from_pool(
    rng,
    pool_name: str,
    pools: Dict[str, List[str]],
    theme_bias: Dict[str, List[str]],
    selected_tags: List[str],
    used_groups: Set[str],
    used_high_level: Set[str],
    nsfw_level: str,
    theme_profile: Optional[Dict[str, object]],
    tag_to_group_map: Dict[str, str],
    tag_category_map: Dict[str, Set[str]],
    max_len: Optional[int] = None,
) -> Optional[str]:
    pool = pools.get(pool_name, [])
    if not pool:
        return None

    prioritized = merge_unique(theme_bias.get(pool_name, []), pool)
    available = [
        tag
        for tag in prioritized
        if _can_use_tag(tag, pool_name, selected_tags, used_groups, nsfw_level, theme_profile, tag_to_group_map, tag_category_map)
    ]
    if not available:
        return None

    bias_candidates = [tag for tag in theme_bias.get(pool_name, []) if tag in available]
    choice_source = bias_candidates if bias_candidates and maybe(rng, 0.65) else available
    choice = pick(rng, choice_source)
    if _try_add_tag(choice, pool_name, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map, max_len=max_len):
        return choice
    return None


def _resolve_pose_order(theme_profile: Optional[Dict[str, object]]) -> List[str]:
    default_order = list(FULL_BODY_POOLS)
    if not theme_profile:
        return default_order
    focus = list(theme_profile.get("pose_focus", []))
    conflicts = set(theme_profile.get("pose_conflicts", set()))
    order = [pool for pool in focus if pool in FULL_BODY_POOLS and pool not in conflicts]
    order.extend(pool for pool in FULL_BODY_POOLS if pool not in order and pool not in conflicts)
    return order


def _select_theme_seed_tags(
    rng,
    theme_pack: Optional[Dict[str, object]],
    selected_tags: List[str],
    used_groups: Set[str],
    used_high_level: Set[str],
    nsfw_level: str,
    theme_profile: Optional[Dict[str, object]],
    tag_to_group_map: Dict[str, str],
    tag_category_map: Dict[str, Set[str]],
) -> None:
    if not theme_pack:
        return

    for _, tags in _theme_tag_groups(theme_pack):
        group_tags = list(tags)
        if not group_tags:
            continue
        rng.shuffle(group_tags)
        required = 1
        if len(group_tags) > 2 and maybe(rng, 0.5):
            required = 2
        for tag in group_tags[:required]:
            pool_name = _primary_pool_for_tag(tag, tag_category_map)
            _try_add_tag(tag, pool_name, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map)


def _select_mood_tag(
    rng,
    pools: Dict[str, List[str]],
    theme_bias: Dict[str, List[str]],
    selected_tags: List[str],
    used_groups: Set[str],
    used_high_level: Set[str],
    nsfw_level: str,
    theme_profile: Optional[Dict[str, object]],
    tag_to_group_map: Dict[str, str],
    tag_category_map: Dict[str, Set[str]],
    expr_mode: str,
) -> bool:
    pool_names: List[str] = []
    base_pool_name = f"mood_{expr_mode}"
    if base_pool_name in pools:
        pool_names.append(base_pool_name)

    preferred_exprs: Sequence[str] = []
    if theme_profile:
        raw_preferred = theme_profile.get("preferred_expressions", [])
        if isinstance(raw_preferred, str):
            preferred_exprs = [raw_preferred]
        else:
            preferred_exprs = list(raw_preferred or [])

    for preferred in preferred_exprs:
        if preferred and preferred != expr_mode:
            preferred_name = f"mood_{preferred}"
            if preferred_name in pools and preferred_name not in pool_names:
                pool_names.append(preferred_name)

    prioritized: List[Tuple[str, str]] = []
    for pool_name in pool_names:
        prioritized.extend((pool_name, tag) for tag in merge_unique(theme_bias.get(pool_name, []), pools.get(pool_name, [])))

    available = [
        (pool_name, tag)
        for pool_name, tag in prioritized
        if _can_use_tag(tag, pool_name, selected_tags, used_groups, nsfw_level, theme_profile, tag_to_group_map, tag_category_map)
    ]
    if not available:
        return False

    bias_candidates = [item for item in available if item[1] in theme_bias.get(item[0], [])]
    pool_name, tag = pick(rng, bias_candidates if bias_candidates and maybe(rng, 0.7) else available)
    return _try_add_tag(tag, pool_name, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map)


def _select_expression_bundle(
    rng,
    pools: Dict[str, List[str]],
    theme_bias: Dict[str, List[str]],
    selected_tags: List[str],
    used_groups: Set[str],
    used_high_level: Set[str],
    nsfw_level: str,
    theme_profile: Optional[Dict[str, object]],
    tag_to_group_map: Dict[str, str],
    tag_category_map: Dict[str, Set[str]],
    expr_mode: str,
    gaze_target: str,
    max_len: Optional[int],
) -> bool:
    added = False
    if _select_from_pool(rng, "mouth", pools, theme_bias, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map, max_len=max_len):
        added = True

    if gaze_target == "自動":
        if _select_from_pool(rng, "eyes", pools, theme_bias, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map, max_len=max_len):
            added = True
    else:
        manual_tag = "closed eyes" if gaze_target == "closed" else gaze_target
        pool_name = "eyes" if manual_tag in pools.get("eyes", []) else _primary_pool_for_tag(manual_tag, tag_category_map)
        if _try_add_tag(manual_tag, pool_name, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map, max_len=max_len):
            added = True

    if maybe(rng, 0.6):
        if _select_from_pool(rng, "brows", pools, theme_bias, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map, max_len=max_len):
            added = True

    if _select_mood_tag(rng, pools, theme_bias, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map, expr_mode):
        added = True

    return added


def _categories_for_high_level(high_level: str, mood_pool_names: Sequence[str]) -> List[str]:
    if high_level == "camera":
        return ["view"]
    if high_level == "full_body":
        return list(FULL_BODY_POOLS)
    if high_level == "upper_body":
        return ["upper_body"]
    if high_level == "lower_body":
        return ["lower_body"]
    if high_level == "effects":
        return ["effects"]
    if high_level == "expression":
        return list(EXPRESSION_POOLS) + list(mood_pool_names)
    return []


def _fill_remaining(
    rng,
    pools: Dict[str, List[str]],
    theme_bias: Dict[str, List[str]],
    theme_related_tags: List[str],
    selected_tags: List[str],
    used_groups: Set[str],
    used_high_level: Set[str],
    nsfw_level: str,
    theme_profile: Optional[Dict[str, object]],
    tag_to_group_map: Dict[str, str],
    tag_category_map: Dict[str, Set[str]],
    max_len: int,
    mood_pool_names: Sequence[str],
) -> None:
    buckets: Dict[int, List[Tuple[Optional[str], str]]] = {0: [], 1: [], 2: []}
    seen: Set[str] = set()

    for tag in theme_related_tags:
        if tag in selected_tags or not tag:
            continue
        pool_name = _primary_pool_for_tag(tag, tag_category_map)
        buckets[0].append((pool_name, tag))

    for high_level in HIGH_LEVEL_PRIORITY:
        if high_level in used_high_level:
            continue
        for pool_name in _categories_for_high_level(high_level, mood_pool_names):
            if pool_name not in pools:
                continue
            prioritized = merge_unique(theme_bias.get(pool_name, []), pools.get(pool_name, []))
            for tag in prioritized:
                buckets[1].append((pool_name, tag))

    for pool_name, pool in pools.items():
        prioritized = merge_unique(theme_bias.get(pool_name, []), pool)
        for tag in prioritized:
            buckets[2].append((pool_name, tag))

    for priority in sorted(buckets.keys()):
        rng.shuffle(buckets[priority])
        for pool_name, tag in buckets[priority]:
            if tag in seen:
                continue
            seen.add(tag)
            if _try_add_tag(tag, pool_name, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map, max_len=max_len):
                if len(join_clean(selected_tags)) >= max_len:
                    return


def _generate_tags(
    rng,
    probs: Dict[str, float],
    pools: Dict[str, List[str]],
    tag_category_map: Dict[str, Set[str]],
    tag_to_group_map: Dict[str, str],
    expr_mode: str,
    theme: str,
    gaze_target: str,
    nsfw_level: str,
    max_len: int,
) -> List[str]:
    selected_tags: List[str] = []
    used_groups: Set[str] = set()
    used_high_level: Set[str] = set()

    theme_pack = EMOTION_THEME_PACKS.get(theme) if theme != "none" else None
    theme_profile = _theme_profile_from_pack(theme_pack)
    theme_bias = _build_theme_bias(theme_pack, pools)
    theme_related_tags = _flatten_theme_tags(theme_pack)

    _select_theme_seed_tags(rng, theme_pack, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map)

    if maybe(rng, probs.get("view", 0.0)):
        _select_from_pool(rng, "view", pools, theme_bias, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map, max_len=max_len)

    if maybe(rng, probs.get("full_body", 0.0)):
        for pool_name in _resolve_pose_order(theme_profile):
            if _select_from_pool(rng, pool_name, pools, theme_bias, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map, max_len=max_len):
                break

    if maybe(rng, probs.get("upper_body", 0.0)):
        _select_from_pool(rng, "upper_body", pools, theme_bias, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map, max_len=max_len)

    if maybe(rng, probs.get("lower_body", 0.0)):
        _select_from_pool(rng, "lower_body", pools, theme_bias, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map, max_len=max_len)

    if maybe(rng, probs.get("expression", 0.0)):
        _select_expression_bundle(
            rng,
            pools,
            theme_bias,
            selected_tags,
            used_groups,
            used_high_level,
            nsfw_level,
            theme_profile,
            tag_to_group_map,
            tag_category_map,
            expr_mode,
            gaze_target,
            max_len,
        )

    if maybe(rng, probs.get("effects", 0.0)):
        _select_from_pool(rng, "effects", pools, theme_bias, selected_tags, used_groups, used_high_level, nsfw_level, theme_profile, tag_to_group_map, tag_category_map, max_len=max_len)

    preferred_exprs: Set[str] = set()
    if theme_profile:
        raw_preferred = theme_profile.get("preferred_expressions", [])
        if isinstance(raw_preferred, str):
            preferred_exprs = {raw_preferred}
        else:
            preferred_exprs = {str(expr) for expr in raw_preferred if expr}

    mood_pool_names: List[str] = []
    for mode in {expr_mode} | preferred_exprs:
        pool_name = f"mood_{mode}"
        if pool_name in pools and pool_name not in mood_pool_names:
            mood_pool_names.append(pool_name)

    _fill_remaining(
        rng,
        pools,
        theme_bias,
        theme_related_tags,
        selected_tags,
        used_groups,
        used_high_level,
        nsfw_level,
        theme_profile,
        tag_to_group_map,
        tag_category_map,
        max_len,
        mood_pool_names,
    )

    return merge_unique(selected_tags)


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
            },
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
            "full_body": base_probs["full_body"] * kwargs.get("確率: 全身ポーズ", 1.0),
            "upper_body": base_probs["upper_body"] * kwargs.get("確率: 上半身", 1.0),
            "lower_body": base_probs["lower_body"] * kwargs.get("確率: 下半身", 1.0),
            "view": base_probs["view"] * kwargs.get("確率: 視点/構図", 1.0),
            "expression": base_probs["expression"] * kwargs.get("確率: 表情", 1.0),
            "effects": base_probs["effects"] * kwargs.get("確率: エフェクト", 1.0),
        }

        pools, tag_category_map = _get_vocab_pools(nsfw_level)
        tag_to_group_map = {tag: name for name, tags in EXCLUSIVE_TAG_GROUPS.items() for tag in tags}

        tags = _generate_tags(
            rng,
            probs,
            pools,
            tag_category_map,
            tag_to_group_map,
            expr_mode,
            theme,
            gaze_target,
            nsfw_level,
            max_len,
        )

        prompt = join_clean(tags)
        prompt = normalize(prompt, lowercase)
        prompt = limit_len(prompt, max_len)

        return (prompt,)


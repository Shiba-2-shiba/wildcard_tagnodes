"""Background tag generator built on concept packs."""

from typing import Dict, List, Sequence

from .util import rng_from_seed, maybe, pick, join_clean, normalize
from .vocab.background_vocab import (
    CONCEPT_PACKS,
    GENERAL_DEFAULTS,
    THEME_TO_PACKS,
    THEME_CHOICES,
    EXCLUSIVE_TAG_GROUPS,
)

FILTER_OPTIONS = ["指定しない", "屋内のみ", "屋外のみ"]


def _resolve_theme_selection(rng, selections: Sequence[str]) -> List[str]:
    explicit: List[str] = []
    omakase = 0
    for value in selections:
        if not value or value == "none":
            continue
        if value == "おまかせ":
            omakase += 1
        else:
            explicit.append(value)

    available = [theme for theme in THEME_TO_PACKS.keys() if theme not in explicit]
    rng.shuffle(available)
    for _ in range(omakase):
        if not available:
            break
        explicit.append(available.pop())

    seen = set()
    ordered: List[str] = []
    for key in explicit:
        if key in seen:
            continue
        seen.add(key)
        ordered.append(key)
    return ordered


def _allowed_settings(filter_mode: str) -> List[str]:
    if filter_mode == "屋内のみ":
        return ["indoor", "mixed"]
    if filter_mode == "屋外のみ":
        return ["outdoor", "mixed"]
    return ["indoor", "outdoor", "mixed"]


def _candidate_pack_keys(theme_keys: Sequence[str], allowed_settings: Sequence[str]) -> List[str]:
    candidates: List[str] = []
    for theme in theme_keys:
        candidates.extend(THEME_TO_PACKS.get(theme, []))
    candidates = [key for key in candidates if CONCEPT_PACKS.get(key, {}).get("setting") in allowed_settings]

    if candidates:
        seen = set()
        ordered: List[str] = []
        for key in candidates:
            if key in seen:
                continue
            seen.add(key)
            ordered.append(key)
        return ordered

    fallback = [
        key
        for key, pack in CONCEPT_PACKS.items()
        if pack.get("setting") in allowed_settings
    ]
    return fallback


def _options_for_category(pack: Dict[str, object], category: str, setting: str) -> List[str]:
    values = list(pack.get(category, []) or [])
    if values:
        return values

    if category in {"lighting", "details", "texture", "fx"}:
        return list(GENERAL_DEFAULTS.get(category, []))

    if category == "architecture":
        if setting == "indoor":
            return list(GENERAL_DEFAULTS.get("architecture_indoor", []))
        if setting == "outdoor":
            return list(GENERAL_DEFAULTS.get("architecture_outdoor", []))
        return list(GENERAL_DEFAULTS.get("architecture_indoor", [])) + list(GENERAL_DEFAULTS.get("architecture_outdoor", []))

    if category == "props":
        if setting == "indoor":
            return list(GENERAL_DEFAULTS.get("props_indoor", []))
        if setting == "outdoor":
            return list(GENERAL_DEFAULTS.get("props_outdoor", []))
        return list(GENERAL_DEFAULTS.get("props_indoor", [])) + list(GENERAL_DEFAULTS.get("props_outdoor", []))

    return []


def _exclusive_for(tag: str) -> List[str]:
    exclusive: List[str] = []
    for groups in EXCLUSIVE_TAG_GROUPS.values():
        for group in groups:
            if tag in group:
                exclusive.extend(item for item in group if item != tag)
    return exclusive


def _build_tags(
    rng,
    pack_key: str,
    確率_照明: float,
    確率_詳細: float,
    確率_質感: float,
    確率_天候_季節: float,
    確率_時間帯: float,
    確率_効果_演出: float,
    確率_建築_構造: float,
    確率_小道具: float,
) -> List[str]:
    pack = CONCEPT_PACKS[pack_key]
    setting = pack.get("setting", "outdoor")

    selected: List[str] = []
    exclusive_tags = set()

    def add_tag(tag: str) -> None:
        if not tag:
            return
        if tag in selected or tag in exclusive_tags:
            return
        selected.append(tag)
        exclusive_tags.update(_exclusive_for(tag))

    environment = list(pack.get("environment", []) or [])
    if environment:
        add_tag(pick(rng, environment))

    for tag in pack.get("core", []) or []:
        add_tag(tag)

    for extra in pack.get("extras", []) or []:
        if maybe(rng, 0.5):
            add_tag(extra)

    if pack.get("mood"):
        add_tag(pack["mood"])  # type: ignore[index]

    if pack.get("weather") and maybe(rng, 確率_天候_季節):
        add_tag(pick(rng, list(pack["weather"])))  # type: ignore[index]

    if pack.get("time") and maybe(rng, 確率_時間帯):
        add_tag(pick(rng, list(pack["time"])))  # type: ignore[index]

    if maybe(rng, 確率_照明):
        lighting_options = _options_for_category(pack, "lighting", setting)
        if lighting_options:
            add_tag(pick(rng, lighting_options))

    if maybe(rng, 確率_詳細):
        detail_options = _options_for_category(pack, "details", setting)
        if detail_options:
            add_tag(pick(rng, detail_options))

    if maybe(rng, 確率_質感):
        texture_options = _options_for_category(pack, "texture", setting)
        if texture_options:
            add_tag(pick(rng, texture_options))

    if maybe(rng, 確率_効果_演出):
        fx_options = _options_for_category(pack, "fx", setting)
        if fx_options:
            add_tag(pick(rng, fx_options))

    if maybe(rng, 確率_建築_構造):
        arch_options = _options_for_category(pack, "architecture", setting)
        if arch_options:
            add_tag(pick(rng, arch_options))

    if maybe(rng, 確率_小道具):
        prop_options = _options_for_category(pack, "props", setting)
        if prop_options:
            add_tag(pick(rng, prop_options))

    if not selected:
        add_tag("atmospheric background")

    return selected


class BackgroundTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31 - 1}),
            },
            "optional": {
                "テーマ1": (THEME_CHOICES,),
                "テーマ2": (THEME_CHOICES,),
                "テーマ3": (THEME_CHOICES,),
                "環境フィルター": (FILTER_OPTIONS,),
                "小文字化": ("BOOL", {"default": True}),
                "確率_照明": ("FLOAT", {"default": 0.85, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_詳細": ("FLOAT", {"default": 0.75, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_質感": ("FLOAT", {"default": 0.65, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_天候_季節": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_時間帯": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_効果_演出": ("FLOAT", {"default": 0.6, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_建築_構造": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率_小道具": ("FLOAT", {"default": 0.45, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def generate(
        self,
        seed,
        テーマ1="none",
        テーマ2="none",
        テーマ3="none",
        環境フィルター="指定しない",
        小文字化=True,
        確率_照明=0.85,
        確率_詳細=0.75,
        確率_質感=0.65,
        確率_天候_季節=0.5,
        確率_時間帯=0.7,
        確率_効果_演出=0.6,
        確率_建築_構造=0.5,
        確率_小道具=0.45,
    ):
        rng = rng_from_seed(seed)
        theme_keys = _resolve_theme_selection(rng, [テーマ1, テーマ2, テーマ3])
        allowed_settings = _allowed_settings(環境フィルター or "指定しない")
        candidates = _candidate_pack_keys(theme_keys, allowed_settings)
        if not candidates:
            candidates = [key for key, pack in CONCEPT_PACKS.items() if pack.get("setting") in allowed_settings]
        pack_key = pick(rng, candidates)

        tags = _build_tags(
            rng,
            pack_key,
            確率_照明,
            確率_詳細,
            確率_質感,
            確率_天候_季節,
            確率_時間帯,
            確率_効果_演出,
            確率_建築_構造,
            確率_小道具,
        )

        prompt = join_clean(tags)
        prompt = normalize(prompt, 小文字化)
        return (prompt,)

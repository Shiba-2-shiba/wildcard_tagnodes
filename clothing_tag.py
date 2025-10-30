"""Clothing tag generator using structured concept packs."""

import random
from typing import Dict, List, Optional, Sequence, Tuple

from .util import rng_from_seed, maybe, pick, join_clean, limit_len, normalize
from .vocab.clothing_vocab import (
    CONCEPT_PACKS,
    THEME_TO_PACKS,
    THEME_CHOICES,
    EXPOSURE_TAGS,
    EROTIC_ACCENTS,
    STATE_TAGS,
    PALETTE_DEFAULT_PROBABILITIES,
    OPTIONAL_DETAIL_PROBABILITY,
    STATE_DETAIL_PROBABILITY,
    OUTERWEAR_SELECTION_PROBABILITY,
)

MODE_MAP_JP = {"一般": "non_erotic", "セクシー": "erotic"}
EXPOSURE_MAP_JP = {"なし": "none", "マイルド": "mild", "大胆": "bold", "過激": "explicit"}

PaletteProbabilities = Dict[str, float]


def _resolve_theme_keys(values: Sequence[Optional[str]]) -> List[str]:
    keys: List[str] = []
    for value in values:
        if value and value != "none":
            keys.append(value)
    # preserve order while deduplicating
    seen: set = set()
    ordered: List[str] = []
    for key in keys:
        if key in seen:
            continue
        seen.add(key)
        ordered.append(key)
    return ordered


def _candidate_pack_keys(category: str, theme_keys: Sequence[str]) -> List[str]:
    available = list(CONCEPT_PACKS.get(category, {}).keys())
    themed: List[str] = []
    for theme in theme_keys:
        themed.extend(THEME_TO_PACKS.get(theme, {}).get(category, []))
    themed = [key for key in themed if key in CONCEPT_PACKS.get(category, {})]
    return themed or available


def _select_pack_key(rng: random.Random, category: str, theme_keys: Sequence[str], hint: Optional[str] = None) -> str:
    available = _candidate_pack_keys(category, theme_keys)
    if hint and hint in CONCEPT_PACKS.get(category, {}):
        return hint
    return pick(rng, available)


def _flatten_choice(choice) -> List[str]:  # type: ignore[no-untyped-def]
    if isinstance(choice, (list, tuple)):
        return [str(item) for item in choice if item]
    if choice:
        return [str(choice)]
    return []


def _merge_probabilities(pack: Dict[str, object]) -> PaletteProbabilities:
    merged = dict(PALETTE_DEFAULT_PROBABILITIES)
    overrides = pack.get("palette_probabilities", {})
    if isinstance(overrides, dict):
        for key, value in overrides.items():
            try:
                merged[key] = float(value)
            except (TypeError, ValueError):
                continue
    return merged


def _apply_optional_details(rng: random.Random, pack: Dict[str, object], add_tag) -> None:  # type: ignore[no-untyped-def]
    details = list(pack.get("optional_details", []) or [])
    if not details:
        return
    rng.shuffle(details)
    prob = pack.get("optional_detail_probability", OPTIONAL_DETAIL_PROBABILITY)
    try:
        probability = float(prob)
    except (TypeError, ValueError):
        probability = OPTIONAL_DETAIL_PROBABILITY
    for detail in details:
        if maybe(rng, probability):
            for tag in _flatten_choice(detail):
                add_tag(tag)


def _add_state_tag(rng: random.Random, pack: Dict[str, object], add_tag) -> None:  # type: ignore[no-untyped-def]
    states = list(pack.get("states", []) or [])
    if not states and pack.get("use_general_states"):
        states = list(STATE_TAGS)
    if not states:
        return
    if maybe(rng, STATE_DETAIL_PROBABILITY):
        tag = pick(rng, states)
        add_tag(tag)


def _expand_pack(
    rng: random.Random,
    category: str,
    pack_key: str,
    existing: List[str],
    forbidden: Optional[set] = None,
) -> Tuple[List[str], set, Dict[str, object]]:
    pack = CONCEPT_PACKS[category][pack_key]
    accumulated: List[str] = []
    forbidden = set(forbidden or set())
    forbidden.update(pack.get("exclusive_tags", []) or [])
    existing_set = set(existing)

    def add_tag(tag: Optional[str]) -> None:
        if not tag:
            return
        cleaned = str(tag).strip()
        if not cleaned:
            return
        if cleaned in forbidden:
            return
        if cleaned in existing_set or cleaned in accumulated:
            return
        accumulated.append(cleaned)

    for tag in pack.get("core", []) or []:
        add_tag(tag)

    for options in (pack.get("choices", {}) or {}).values():
        if not options:
            continue
        choice = pick(rng, list(options))
        for tag in _flatten_choice(choice):
            add_tag(tag)

    palette = pack.get("palette", {}) or {}
    palette_probs = _merge_probabilities(pack)
    for palette_name, probability in palette_probs.items():
        options = palette.get(palette_name, [])
        if not options:
            continue
        if maybe(rng, max(0.0, min(1.0, probability))):
            add_tag(pick(rng, list(options)))

    _apply_optional_details(rng, pack, add_tag)
    _add_state_tag(rng, pack, add_tag)

    accents = list(pack.get("accent_tags", []) or [])
    if accents:
        for accent in accents:
            if maybe(rng, 0.5):
                add_tag(accent)

    forbidden.update(pack.get("blocked_tags", []) or [])
    return accumulated, forbidden, pack


def _choose_outfit_category(rng: random.Random, erotic: bool) -> str:
    if erotic:
        return "dresses" if maybe(rng, 0.55) else "separates"
    return "dresses" if maybe(rng, 0.45) else "separates"


def _resolve_exposure_profile(
    exposure_level: str,
    erotic: bool,
    pack: Dict[str, object],
) -> Tuple[List[str], float]:
    level = (exposure_level or "none").lower()
    if level == "none":
        return [], 0.0
    if level == "explicit" and not erotic:
        return [], 0.0

    pool: List[str] = list(EXPOSURE_TAGS.get(level, []))
    if level == "mild":
        probability = 0.5 if erotic else 0.3
    elif level == "bold":
        probability = 0.75 if erotic else 0.5
    else:  # explicit
        probability = 0.9 if erotic else 0.0

    bias = str(pack.get("exposure_bias", "")).lower()
    if bias and bias == level:
        probability = min(1.0, probability + 0.15)
    elif bias and level == "bold" and bias == "explicit":
        probability = min(1.0, probability + 0.1)
    return pool, probability


def _append_if_unique(tags: List[str], new_tag: Optional[str]) -> None:
    if not new_tag:
        return
    cleaned = str(new_tag).strip()
    if not cleaned:
        return
    if cleaned in tags:
        return
    tags.append(cleaned)


def _trim_to_length(tags: List[str], max_len: int) -> List[str]:
    if max_len <= 0:
        return []
    trimmed: List[str] = []
    for tag in tags:
        candidate = trimmed + [tag]
        if len(join_clean(candidate)) <= max_len:
            trimmed.append(tag)
        else:
            break
    return trimmed


def _compose(
    rng: random.Random,
    theme_keys: Sequence[str],
    erotic: bool,
    exposure_level: str,
    max_len: int,
) -> str:
    selected: List[str] = []
    forbidden: set = set()

    outfit_category = _choose_outfit_category(rng, erotic)
    base_key = _select_pack_key(rng, outfit_category, theme_keys)
    base_tags, forbidden, base_pack = _expand_pack(rng, outfit_category, base_key, selected, forbidden)
    selected.extend(base_tags)

    outerwear_prob = OUTERWEAR_SELECTION_PROBABILITY
    outerwear_hint = base_pack.get("outerwear_hint") if isinstance(base_pack, dict) else None
    if outerwear_hint:
        outerwear_prob = max(outerwear_prob, 0.45)
    if maybe(rng, outerwear_prob):
        outer_key = _select_pack_key(rng, "outerwear", theme_keys, hint=outerwear_hint if isinstance(outerwear_hint, str) else None)
        outer_tags, forbidden, _ = _expand_pack(rng, "outerwear", outer_key, selected, forbidden)
        selected.extend(outer_tags)

    if erotic:
        accent_source = list(base_pack.get("accent_tags", []) or [])
        if not accent_source:
            accent_source = list(EROTIC_ACCENTS)
        if accent_source and maybe(rng, 0.65):
            _append_if_unique(selected, pick(rng, accent_source))

    pool, probability = _resolve_exposure_profile(exposure_level, erotic, base_pack)
    if pool and maybe(rng, probability):
        _append_if_unique(selected, pick(rng, pool))

    selected = list(dict.fromkeys(selected))
    selected = _trim_to_length(selected, max_len)
    return join_clean(selected)


class ClothingTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31 - 1}),
                "モード": (list(MODE_MAP_JP.keys()),),
                "露出度": (list(EXPOSURE_MAP_JP.keys()), {"default": "マイルド"}),
                "最大文字数": ("INT", {"default": 150, "min": 30, "max": 4096}),
            },
            "optional": {
                "テーマ1": (THEME_CHOICES,),
                "テーマ2": (THEME_CHOICES,),
                "テーマ3": (THEME_CHOICES,),
                "小文字化": ("BOOL", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def generate(
        self,
        seed,
        モード,
        露出度,
        最大文字数,
        テーマ1="none",
        テーマ2="none",
        テーマ3="none",
        小文字化=True,
        **kwargs,
    ):
        rng = rng_from_seed(seed)
        mode_en = MODE_MAP_JP.get(モード, "non_erotic")
        exposure_en = EXPOSURE_MAP_JP.get(露出度, "none")
        theme_keys = _resolve_theme_keys([テーマ1, テーマ2, テーマ3])

        tag = _compose(rng, theme_keys, erotic=(mode_en == "erotic"), exposure_level=exposure_en, max_len=最大文字数)
        tag = normalize(tag, 小文字化)
        tag = limit_len(tag, 最大文字数)
        return (tag,)

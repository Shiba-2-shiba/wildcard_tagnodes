# appearance_tag.py
# 顔造形・体型・髪を多段階で生成するノード

from typing import Dict, List, Optional, Sequence, Tuple

from .util import (
    rng_from_seed,
    maybe,
    pick,
    join_clean,
    limit_len,
    normalize,
    merge_unique,
)
from .vocab.appearance_vocab import (
    BODY_SHAPES,
    BODY_DETAILS,
    SKIN_DETAILS,
    HAIR_LENGTHS,
    HAIR_TEXTURES,
    HAIR_STYLES,
    HAIR_BANGS_PART,
    HAIR_COLORS,
    HAIR_COLOR_MIX,
    FACE_SHAPES,
    FACE_DETAILS,
    EYE_SHAPES,
    NOSE_SHAPES,
    LIP_SHAPES,
    BODY_ACCENTS,
    SKIN_ACCENTS,
    FACE_ACCENTS,
    HAIR_ACCENTS,
    SENSUAL_ACCENTS,
    THEMES,
    EXCLUSIVE_GROUPS,
)


MODE_MAP_JP = {"一般": "normal", "セクシー": "sexy"}
THEME_CHOICES = ["none"] + sorted(list(THEMES.keys()))


def _copy_list(values: Sequence[str]) -> List[str]:
    return list(values or [])


def _prepare_vocab(theme_keys: List[str]) -> Dict[str, List[str]]:
    vocab = dict(
        body_shapes=_copy_list(BODY_SHAPES),
        body_details=_copy_list(BODY_DETAILS),
        skin_tones=_copy_list(SKIN_DETAILS.get("tones", [])),
        skin_features=_copy_list(SKIN_DETAILS.get("features", [])),
        skin_finishes=_copy_list(SKIN_DETAILS.get("finishes", [])),
        hair_lengths=_copy_list(HAIR_LENGTHS),
        hair_textures=_copy_list(HAIR_TEXTURES),
        hair_styles=_copy_list(HAIR_STYLES),
        hair_bangs=_copy_list(HAIR_BANGS_PART),
        hair_colors=_copy_list(HAIR_COLORS),
        hair_color_mix=_copy_list(HAIR_COLOR_MIX),
        face_shapes=_copy_list(FACE_SHAPES),
        eye_shapes=_copy_list(EYE_SHAPES),
        nose_shapes=_copy_list(NOSE_SHAPES),
        lip_shapes=_copy_list(LIP_SHAPES),
        face_details=_copy_list(FACE_DETAILS),
        body_accents=_copy_list(BODY_ACCENTS),
        skin_accents=_copy_list(SKIN_ACCENTS),
        face_accents=_copy_list(FACE_ACCENTS),
        hair_accents=_copy_list(HAIR_ACCENTS),
        body_shape_bias=[],
        body_detail_bias=[],
        skin_tone_bias=[],
        skin_feature_bias=[],
        hair_length_bias=[],
        hair_texture_bias=[],
        hair_style_bias=[],
        hair_bang_bias=[],
        hair_color_bias=[],
        hair_mix_bias=[],
        face_shape_bias=[],
        eye_shape_bias=[],
        nose_shape_bias=[],
        lip_shape_bias=[],
        face_detail_bias=[],
        decor_body_bias=[],
        decor_skin_bias=[],
        decor_face_bias=[],
        decor_hair_bias=[],
    )

    for key in theme_keys:
        theme = THEMES.get(key)
        if not theme:
            continue

        body = theme.get("body", {})
        if body:
            vocab["body_shapes"] = merge_unique(vocab["body_shapes"], body.get("shapes", []))
            vocab["body_details"] = merge_unique(vocab["body_details"], body.get("details", []))
            vocab["body_shape_bias"] = merge_unique(vocab["body_shape_bias"], body.get("shapes", []))
            vocab["body_detail_bias"] = merge_unique(vocab["body_detail_bias"], body.get("details", []))

        skin = theme.get("skin", {})
        if skin:
            vocab["skin_tones"] = merge_unique(vocab["skin_tones"], skin.get("tones", []))
            vocab["skin_features"] = merge_unique(vocab["skin_features"], skin.get("features", []))
            vocab["skin_finishes"] = merge_unique(vocab["skin_finishes"], skin.get("finishes", []))
            vocab["skin_tone_bias"] = merge_unique(vocab["skin_tone_bias"], skin.get("tones", []))
            vocab["skin_feature_bias"] = merge_unique(vocab["skin_feature_bias"], skin.get("features", []))

        hair = theme.get("hair", {})
        if hair:
            vocab["hair_lengths"] = merge_unique(vocab["hair_lengths"], hair.get("lengths", []))
            vocab["hair_textures"] = merge_unique(vocab["hair_textures"], hair.get("textures", []))
            vocab["hair_styles"] = merge_unique(vocab["hair_styles"], hair.get("styles", []))
            vocab["hair_bangs"] = merge_unique(vocab["hair_bangs"], hair.get("bangs", []))
            vocab["hair_colors"] = merge_unique(vocab["hair_colors"], hair.get("colors", []))
            vocab["hair_color_mix"] = merge_unique(vocab["hair_color_mix"], hair.get("mix", []))
            vocab["hair_length_bias"] = merge_unique(vocab["hair_length_bias"], hair.get("lengths", []))
            vocab["hair_texture_bias"] = merge_unique(vocab["hair_texture_bias"], hair.get("textures", []))
            vocab["hair_style_bias"] = merge_unique(vocab["hair_style_bias"], hair.get("styles", []))
            vocab["hair_bang_bias"] = merge_unique(vocab["hair_bang_bias"], hair.get("bangs", []))
            vocab["hair_color_bias"] = merge_unique(vocab["hair_color_bias"], hair.get("colors", []))
            vocab["hair_mix_bias"] = merge_unique(vocab["hair_mix_bias"], hair.get("mix", []))

        face = theme.get("face", {})
        if face:
            vocab["face_shapes"] = merge_unique(vocab["face_shapes"], face.get("shapes", []))
            vocab["eye_shapes"] = merge_unique(vocab["eye_shapes"], face.get("eyes", []))
            vocab["nose_shapes"] = merge_unique(vocab["nose_shapes"], face.get("nose", []))
            vocab["lip_shapes"] = merge_unique(vocab["lip_shapes"], face.get("lips", []))
            vocab["face_details"] = merge_unique(vocab["face_details"], face.get("details", []))
            vocab["face_shape_bias"] = merge_unique(vocab["face_shape_bias"], face.get("shapes", []))
            vocab["eye_shape_bias"] = merge_unique(vocab["eye_shape_bias"], face.get("eyes", []))
            vocab["nose_shape_bias"] = merge_unique(vocab["nose_shape_bias"], face.get("nose", []))
            vocab["lip_shape_bias"] = merge_unique(vocab["lip_shape_bias"], face.get("lips", []))
            vocab["face_detail_bias"] = merge_unique(vocab["face_detail_bias"], face.get("details", []))

        decor = theme.get("decor", {})
        if decor:
            vocab["body_accents"] = merge_unique(vocab["body_accents"], decor.get("body", []))
            vocab["skin_accents"] = merge_unique(vocab["skin_accents"], decor.get("skin", []))
            vocab["face_accents"] = merge_unique(vocab["face_accents"], decor.get("face", []))
            vocab["hair_accents"] = merge_unique(vocab["hair_accents"], decor.get("hair", []))
            vocab["decor_body_bias"] = merge_unique(vocab["decor_body_bias"], decor.get("body", []))
            vocab["decor_skin_bias"] = merge_unique(vocab["decor_skin_bias"], decor.get("skin", []))
            vocab["decor_face_bias"] = merge_unique(vocab["decor_face_bias"], decor.get("face", []))
            vocab["decor_hair_bias"] = merge_unique(vocab["decor_hair_bias"], decor.get("hair", []))

    return vocab


def _get_exclusive_tags(first_tag: str) -> List[str]:
    blocked: List[str] = []
    for groups in EXCLUSIVE_GROUPS.values():
        for tags in groups.values():
            if first_tag in tags:
                for other_tags in groups.values():
                    blocked.extend(other_tags)
                break
    return blocked


def _add_tag(collector: List[str], exclusive: set, tag: Optional[str], alias: Optional[Sequence[str]] = None) -> bool:
    if not tag:
        return False
    alias_list = [tag]
    if alias:
        alias_list.extend([a for a in alias if a])
    if any(a in exclusive for a in alias_list):
        return False
    collector.append(tag)
    for item in alias_list:
        exclusive.add(item)
        for blocked in _get_exclusive_tags(item):
            exclusive.add(blocked)
    return True


def _register_choice(exclusive: set, choice: Optional[str]) -> None:
    if not choice:
        return
    exclusive.add(choice)
    for blocked in _get_exclusive_tags(choice):
        exclusive.add(blocked)


def _choose_with_bias(rng, pool: List[str], bias: List[str], probability: float) -> Optional[str]:
    if bias and maybe(rng, probability):
        candidate = pick(rng, bias)
        if candidate:
            return candidate
    return pick(rng, pool)


def _scaled_prob(base: float, maximum: float, factor: float) -> float:
    factor = max(0.0, min(1.0, factor))
    return base + (maximum - base) * factor


def _format_hair_length(length: Optional[str]) -> Optional[str]:
    if not length:
        return None
    if "cut" in length or "bob" in length:
        return length
    return f"{length} hair"


def _format_hair_texture(texture: Optional[str]) -> Optional[str]:
    if not texture:
        return None
    if "hair" in texture:
        return texture
    return f"{texture} hair"


def _format_hair_color(color: Optional[str]) -> Optional[str]:
    if not color:
        return None
    if any(word in color for word in ["balayage", "ombre", "streaks", "gradient", "highlights", "melt"]):
        return color
    if "hair" in color:
        return color
    return f"{color} hair"


def _pick_from_pool(rng, pool: List[str], bias: List[str], probability: float, exclusive: set) -> Optional[str]:
    available = [t for t in pool if t not in exclusive]
    if not available:
        return None
    biased = [t for t in bias if t in available]
    return _choose_with_bias(rng, available, biased, probability)


def _stage_three_enrich(
    rng,
    tags: List[str],
    exclusive: set,
    vocab: Dict[str, List[str]],
    body_complexity: float,
    face_complexity: float,
    sexy: bool,
    max_len: int,
) -> None:
    stage_sources: List[Tuple[str, List[str], List[str], float]] = [
        ("body", vocab["body_accents"], vocab["decor_body_bias"], _scaled_prob(0.25, 0.7, body_complexity)),
        ("skin", vocab["skin_accents"], vocab["decor_skin_bias"], _scaled_prob(0.3, 0.85, body_complexity)),
        ("face", vocab["face_accents"], vocab["decor_face_bias"], _scaled_prob(0.35, 0.9, face_complexity)),
        ("hair", vocab["hair_accents"], vocab["decor_hair_bias"], _scaled_prob(0.3, 0.75, face_complexity)),
    ]
    if sexy:
        stage_sources.append(("sensual", _copy_list(SENSUAL_ACCENTS), [], 0.45))

    attempts_without_progress = 0
    while stage_sources and len(join_clean(tags)) < max_len and attempts_without_progress < 8:
        category, pool, bias, probability = rng.choice(stage_sources)
        if not pool:
            stage_sources.remove((category, pool, bias, probability))
            continue
        available = [t for t in pool if t not in exclusive and t not in tags]
        if not available or not maybe(rng, probability):
            attempts_without_progress += 1
            continue
        biased = [t for t in bias if t in available]
        candidate = _choose_with_bias(rng, available, biased, probability)
        if not candidate:
            attempts_without_progress += 1
            continue
        prospective = join_clean(tags + [candidate])
        if max_len and len(prospective) > max_len:
            attempts_without_progress += 1
            continue
        _add_tag(tags, exclusive, candidate)
        attempts_without_progress = 0


class AppearanceTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31 - 1}),
            },
            "optional": {
                "モード": (list(MODE_MAP_JP.keys()), {"default": "一般"}),
                "テーマ1": (THEME_CHOICES, {"default": "none"}),
                "テーマ2": (THEME_CHOICES, {"default": "none"}),
                "テーマ3": (THEME_CHOICES, {"default": "none"}),
                "最大文字数": ("INT", {"default": 160, "min": 0, "max": 4096}),
                "小文字化": ("BOOL", {"default": True}),
                "顔の造形の複雑さ": ("FLOAT", {"default": 0.65, "min": 0.0, "max": 1.0, "step": 0.01}),
                "身体的特徴の複雑さ": ("FLOAT", {"default": 0.55, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def generate(
        self,
        seed: int,
        モード: str = "一般",
        テーマ1: str = "none",
        テーマ2: str = "none",
        テーマ3: str = "none",
        最大文字数: int = 160,
        小文字化: bool = True,
        顔の造形の複雑さ: float = 0.65,
        身体的特徴の複雑さ: float = 0.55,
        **kwargs,
    ):
        rng = rng_from_seed(seed)
        sexy = MODE_MAP_JP.get(モード, "normal") == "sexy"

        theme_keys = []
        for key in [テーマ1, テーマ2, テーマ3]:
            if key and key != "none" and key in THEMES and key not in theme_keys:
                theme_keys.append(key)

        vocab = _prepare_vocab(theme_keys)

        face_complexity = max(0.0, min(1.0, 顔の造形の複雑さ))
        body_complexity = max(0.0, min(1.0, 身体的特徴の複雑さ))

        tags: List[str] = []
        exclusive_tags: set = set()

        # ===== Stage 1: Core traits =====
        body_shape = _pick_from_pool(
            rng,
            vocab["body_shapes"],
            vocab["body_shape_bias"],
            _scaled_prob(0.35, 0.7, body_complexity),
            exclusive_tags,
        )
        _add_tag(tags, exclusive_tags, body_shape)

        skin_tone = _pick_from_pool(
            rng,
            vocab["skin_tones"],
            vocab["skin_tone_bias"],
            _scaled_prob(0.4, 0.85, body_complexity),
            exclusive_tags,
        )
        _add_tag(tags, exclusive_tags, skin_tone)

        face_shape = _pick_from_pool(
            rng,
            vocab["face_shapes"],
            vocab["face_shape_bias"],
            _scaled_prob(0.45, 0.85, face_complexity),
            exclusive_tags,
        )
        _add_tag(tags, exclusive_tags, face_shape)

        hair_length_choice = _pick_from_pool(
            rng,
            vocab["hair_lengths"],
            vocab["hair_length_bias"],
            _scaled_prob(0.35, 0.7, face_complexity),
            exclusive_tags,
        )
        _register_choice(exclusive_tags, hair_length_choice)

        color_mix_probability = _scaled_prob(0.2, 0.55, face_complexity)
        hair_mix_choice = None
        if maybe(rng, color_mix_probability):
            hair_mix_choice = _pick_from_pool(
                rng,
                vocab["hair_color_mix"],
                vocab["hair_mix_bias"],
                min(0.9, color_mix_probability + 0.25),
                exclusive_tags,
            )
        hair_color_choice = None
        if not hair_mix_choice:
            hair_color_choice = _pick_from_pool(
                rng,
                vocab["hair_colors"],
                vocab["hair_color_bias"],
                0.85,
                exclusive_tags,
            )
        _register_choice(exclusive_tags, hair_mix_choice or hair_color_choice)

        # ===== Stage 2: Detailed traits =====
        body_detail_prob = _scaled_prob(0.3, 0.75, body_complexity)
        body_detail = _pick_from_pool(
            rng,
            vocab["body_details"],
            vocab["body_detail_bias"],
            body_detail_prob,
            exclusive_tags,
        )
        _add_tag(tags, exclusive_tags, body_detail)

        skin_feature_prob = _scaled_prob(0.25, 0.75, body_complexity)
        if maybe(rng, skin_feature_prob):
            skin_feature = _pick_from_pool(
                rng,
                vocab["skin_features"],
                vocab["skin_feature_bias"],
                skin_feature_prob,
                exclusive_tags,
            )
            _add_tag(tags, exclusive_tags, skin_feature)

        skin_finish_prob = _scaled_prob(0.3, 0.8, body_complexity)
        if maybe(rng, skin_finish_prob):
            skin_finish = _pick_from_pool(
                rng,
                vocab["skin_finishes"],
                [],
                skin_finish_prob,
                exclusive_tags,
            )
            _add_tag(tags, exclusive_tags, skin_finish)

        eye_shape = _pick_from_pool(
            rng,
            vocab["eye_shapes"],
            vocab["eye_shape_bias"],
            _scaled_prob(0.4, 0.85, face_complexity),
            exclusive_tags,
        )
        _add_tag(tags, exclusive_tags, eye_shape)

        nose_shape = _pick_from_pool(
            rng,
            vocab["nose_shapes"],
            vocab["nose_shape_bias"],
            _scaled_prob(0.35, 0.8, face_complexity),
            exclusive_tags,
        )
        _add_tag(tags, exclusive_tags, nose_shape)

        lip_shape = _pick_from_pool(
            rng,
            vocab["lip_shapes"],
            vocab["lip_shape_bias"],
            _scaled_prob(0.35, 0.85, face_complexity),
            exclusive_tags,
        )
        _add_tag(tags, exclusive_tags, lip_shape)

        face_detail_prob = _scaled_prob(0.35, 0.8, face_complexity)
        if maybe(rng, face_detail_prob):
            face_detail = _pick_from_pool(
                rng,
                vocab["face_details"],
                vocab["face_detail_bias"],
                face_detail_prob,
                exclusive_tags,
            )
            if _add_tag(tags, exclusive_tags, face_detail):
                # chance for a secondary complementary detail when complexity is high
                if maybe(rng, face_complexity * 0.35):
                    secondary_detail = _pick_from_pool(
                        rng,
                        vocab["face_details"],
                        vocab["face_detail_bias"],
                        face_detail_prob * 0.8,
                        exclusive_tags,
                    )
                    _add_tag(tags, exclusive_tags, secondary_detail)

        hair_texture_prob = _scaled_prob(0.4, 0.8, face_complexity)
        if maybe(rng, hair_texture_prob):
            hair_texture_choice = _pick_from_pool(
                rng,
                vocab["hair_textures"],
                vocab["hair_texture_bias"],
                hair_texture_prob,
                exclusive_tags,
            )
            _register_choice(exclusive_tags, hair_texture_choice)
            hair_texture_tag = _format_hair_texture(hair_texture_choice)
            _add_tag(tags, exclusive_tags, hair_texture_tag, alias=[hair_texture_choice] if hair_texture_choice else None)

        hair_style_prob = _scaled_prob(0.35, 0.75, face_complexity)
        if maybe(rng, hair_style_prob):
            hair_style_choice = _pick_from_pool(
                rng,
                vocab["hair_styles"],
                vocab["hair_style_bias"],
                hair_style_prob,
                exclusive_tags,
            )
            _register_choice(exclusive_tags, hair_style_choice)
            _add_tag(tags, exclusive_tags, hair_style_choice)

        hair_bang_prob = _scaled_prob(0.35, 0.75, face_complexity)
        if maybe(rng, hair_bang_prob):
            hair_bang_choice = _pick_from_pool(
                rng,
                vocab["hair_bangs"],
                vocab["hair_bang_bias"],
                hair_bang_prob,
                exclusive_tags,
            )
            _register_choice(exclusive_tags, hair_bang_choice)
            _add_tag(tags, exclusive_tags, hair_bang_choice)

        hair_length_tag = _format_hair_length(hair_length_choice)
        _add_tag(
            tags,
            exclusive_tags,
            hair_length_tag,
            alias=[hair_length_choice] if hair_length_choice else None,
        )

        hair_color_tag = _format_hair_color(hair_mix_choice or hair_color_choice)
        _add_tag(
            tags,
            exclusive_tags,
            hair_color_tag,
            alias=[hair_mix_choice or hair_color_choice] if (hair_mix_choice or hair_color_choice) else None,
        )

        # ===== Stage 3: Fill up to max length =====
        _stage_three_enrich(
            rng,
            tags,
            exclusive_tags,
            vocab,
            body_complexity,
            face_complexity,
            sexy,
            最大文字数,
        )

        tag_string = join_clean(tags)
        tag_string = normalize(tag_string, 小文字化)
        tag_string = limit_len(tag_string, 最大文字数)
        return (tag_string,)



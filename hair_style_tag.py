# hair_style_tag.py
# 髪型タグ生成ノード

from .util import rng_from_seed, maybe, pick, join_clean, limit_len, normalize
from .vocab.hair_style_vocab import LENGTHS, TEXTURES, ARRANGEMENTS, BANGS

class HairTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31 - 1}),
            },
            "optional": {
                "最大文字数": ("INT", {"default": 80, "min": 0, "max": 4096}),
                "小文字化": ("BOOL", {"default": True}),
                "確率: 髪質": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: アレンジ": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 前髪": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def generate(self, seed, 最大文字数=80, 小文字化=True,
                 確率_髪質=0.8, 確率_アレンジ=0.5, 確率_前髪=0.5, **kwargs):
        rng = rng_from_seed(seed)
        length = pick(rng, LENGTHS) or "short"
        texture = pick(rng, TEXTURES) if maybe(rng, 確率_髪質) else None
        arrangement = pick(rng, ARRANGEMENTS) if maybe(rng, 確率_アレンジ) else None
        bangs = pick(rng, BANGS) if maybe(rng, 確率_前髪) else None

        base = join_clean([length, texture, arrangement], sep=" ")
        if base:
            base = base + " hair"
        tag = join_clean([base, bangs], sep=", ")
        tag = normalize(tag, 小文字化)
        tag = limit_len(tag, 最大文字数)
        return (tag,)

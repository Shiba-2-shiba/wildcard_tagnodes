# art_style_tag.py
# アートスタイルタグ生成ノード

from .util import rng_from_seed, maybe, pick, join_clean, limit_len, normalize
from .vocab.art_style_vocab import STYLES, GENRES

class ArtStyleTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31 - 1}),
            },
            "optional": {
                "最大文字数": ("INT", {"default": 80, "min": 0, "max": 4096}),
                "小文字化": ("BOOL", {"default": True}),
                "確率: ジャンル": ("FLOAT", {"default": 0.6, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def generate(self, seed, 最大文字数=80, 小文字化=True, 確率_ジャンル=0.6, **kwargs):
        rng = rng_from_seed(seed)
        style = pick(rng, STYLES) or "digital painting"
        genre = pick(rng, GENRES) if maybe(rng, 確率_ジャンル) else None
        tag = join_clean([genre, style])
        tag = normalize(tag, 小文字化)
        tag = limit_len(tag, 最大文字数)
        return (tag,)

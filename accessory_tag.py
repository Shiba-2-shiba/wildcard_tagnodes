# accessory_tag.py
# アクセサリータグ生成ノード

from .util import rng_from_seed, maybe, pick, join_clean, limit_len, normalize
from .vocab.accessory_vocab import HEADWEAR, EYEWEAR, JEWELRY, HANDHELD

class AccessoryTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 42, "min": 0, "max": 2**31 - 1}),
            },
            "optional": {
                "最大文字数": ("INT", {"default": 100, "min": 0, "max": 4096}),
                "小文字化": ("BOOL", {"default": True}),
                "確率: 頭": ("FLOAT", {"default": 0.4, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 顔": ("FLOAT", {"default": 0.35, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 体": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "確率: 手持ち": ("FLOAT", {"default": 0.4, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Text/Wildcards"

    def generate(self, seed, 最大文字数=100, 小文字化=True,
                 確率_頭=0.4, 確率_顔=0.35, 確率_体=0.5, 確率_手持ち=0.4, **kwargs):
        rng = rng_from_seed(seed)
        parts = []
        if maybe(rng, 確率_頭): parts.append(pick(rng, HEADWEAR))
        if maybe(rng, 確率_顔): parts.append(pick(rng, EYEWEAR))
        if maybe(rng, 確率_体): parts.append(pick(rng, JEWELRY))
        if maybe(rng, 確率_手持ち): parts.append(pick(rng, HANDHELD))
        if not parts:
            all_items = HEADWEAR + EYEWEAR + JEWELRY + HANDHELD
            parts.append(pick(rng, all_items))
        tag = join_clean(parts)
        tag = normalize(tag, 小文字化)
        tag = limit_len(tag, 最大文字数)
        return (tag,)

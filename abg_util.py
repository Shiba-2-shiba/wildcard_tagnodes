# abg_util.py
# Advanced Background Tag Node 専用のユーティリティファイル

import re, random
from typing import List, Optional

def rng_from_seed(seed: int) -> random.Random:
    return random.Random(int(seed) & 0xFFFFFFFF)

def maybe(rng: random.Random, p: float) -> bool:
    return rng.random() < max(0.0, min(1.0, p))

def pick(rng: random.Random, arr: List[str]) -> Optional[str]:
    if not arr:
        return None
    return rng.choice(arr)

# Advanced Background Tag Node用に区切り文字を ", " に変更したバージョン
def join_clean(parts: List[str], sep: str=", ") -> str:
    parts = [p.strip() for p in parts if p and p.strip()]
    s = sep.join(parts)
    return re.sub(r"\s+", " ", s).strip()

def normalize(s: str, lowercase: bool) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s.lower() if lowercase else s

def merge_unique(*lists: List[str]) -> List[str]:
    seen = set()
    out = []
    for lst in lists:
        for x in lst or []:
            if x not in seen:
                seen.add(x)
                out.append(x)
    return out

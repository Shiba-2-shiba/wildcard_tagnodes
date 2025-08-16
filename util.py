# util.py
# 共通ユーティリティ（外部ファイル読込機能を削除）

import re, random
from typing import List, Optional

# ===== ランダム & 文字処理 =====
def rng_from_seed(seed: int) -> random.Random:
    return random.Random(int(seed) & 0xFFFFFFFF)

def maybe(rng: random.Random, p: float) -> bool:
    return rng.random() < max(0.0, min(1.0, p))

def pick(rng: random.Random, arr: List[str]) -> Optional[str]:
    if not arr:
        return None
    return rng.choice(arr)

def join_clean(parts: List[str], sep: str=", ") -> str:
    parts = [p.strip() for p in parts if p and p.strip()]
    s = sep.join(parts)
    return re.sub(r"\s+", " ", s).strip()

def limit_len(s: str, max_len: int) -> str:
    if max_len <= 0:
        return s
    return s[:max_len]

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

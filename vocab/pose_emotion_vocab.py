# -*- coding: utf-8 -*-
"""
vocab/improved_pose_emotion_vocab.py (Full Script / Standalone)

ワイルドカードノードの語彙ブラッシュアップ版。
- 外部ファイル読み込みを廃止し、全語彙をスクリプト内に直接定義
- 語彙の大幅な拡張
- カテゴリの再整理と体系化
- 感情表現の多角化（eroticモードを追加）
- 排他タググループの導入
- 感情を軸にしたテーマパックの導入
- ブロックリスト生成機能を実装
"""

from __future__ import annotations
from typing import List, Dict, Set

# ========================================
# ユーティリティ関数
# ========================================
def _dedupe(seq: List[str]) -> List[str]:
    """順序を保った重複除去（大小文字は無視して同一視）"""
    seen = set()
    out: List[str] = []
    for s in seq:
        k = (s or "").strip().lower()
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(s.strip())
    return out

def _merge_unique(*lists: List[str]) -> List[str]:
    buf: List[str] = []
    for lst in lists:
        buf.extend(lst or [])
    return _dedupe(buf)

# ========================================
# 1. 語彙の整理と拡張
# ========================================

# --- 視点・構図 (View & Framing) ---
VIEW_ANGLES = [
    "front view", "three-quarter view", "profile view", "back view",
    "from above", "from below", "dutch angle", "worm's-eye view", "bird's-eye view",
    "wide angle", "fisheye lens effect", "cinematic angle",
]
VIEW_FRAMING = [
    "full shot", "long shot", "medium shot", "medium close-up", "close-up", "extreme close-up",
    "cowboy shot", "waist shot", "bust shot", "face shot", "over-the-shoulder shot",
    "point of view shot",
]

# --- ポーズ: 全身 (Pose: Full Body) ---
POSE_STANDING = [
    "standing", "contrapposto", "relaxed stance", "standing with hands on hips",
    "standing with arms crossed", "standing at attention", "power stance", "wide stance",
    "leaning against a wall", "one leg forward", "shifting weight", "looking over shoulder",
]
POSE_SITTING = [
    "sitting", "sitting on a chair", "sitting on the floor", "sitting cross-legged",
    "sitting with legs to one side", "kneeling", "sitting on heels (seiza)", "crouching",
    "squatting", "perched on a stool", "lounging on a sofa", "hugging knees",
]
POSE_LYING = [
    "lying on back", "lying on stomach", "lying on side", "fetal position",
    "reclining", "sprawled out", "starfish position",
]
POSE_DYNAMIC = [
    "walking", "running", "jumping", "leaping", "dancing", "twirling",
    "action pose", "dynamic pose", "mid-air", "landing", "stretching", "yoga pose",
    "fighting stance", "kicking", "punching", "dodging",
]

# --- ポーズ: 上半身 (Pose: Upper Body) ---
HAND_POSITIONS = [
    "hands on hips", "arms crossed", "hands behind back", "hands behind head",
    "hands clasped in front", "hands clasped behind", "waving", "pointing",
    "hands in pockets", "one hand raised", "arms outstretched", "shrugging",
]
HAND_GESTURES = [
    "hand on cheek", "fingers to lips", "touching hair", "adjusting glasses",
    "hand on neck", "cupping chin", "facepalm", "thumbs up", "peace sign",
    "fist clenched", "open palm", "praying hands", "blowing a kiss",
]
SPINE_AND_SHOULDERS = [
    "arched back", "slumped shoulders", "shoulders back", "chest out",
    "leaning forward", "leaning back", "twisting torso", "shrugging shoulders",
    "head tilt", "looking up", "looking down",
]

# --- ポーズ: 下半身 (Pose: Lower Body) ---
LEG_POSITIONS = [
    "legs crossed", "legs apart", "standing on one leg", "one knee raised",
    "legs straight", "knees bent", "on tiptoes", "feet together", "feet apart",
    "pigeon-toed", "bow-legged", "walking stride", "running stride",
]

# --- 表情: 基本 (Expression: Base) ---
MOUTH_BASE = [
    "closed mouth", "slight smile", "soft smile", "gentle smile", "faint smile",
    "lips parted", "half-open mouth", "open mouth", "pout", "smirk", "grin",
    "toothy smile", "laughing", "shouting", "gasping", "yawning", "biting lip",
    "licking lips", "whistling",
]
EYES_BASE = [
    "open eyes", "closed eyes", "half-closed eyes", "narrowed eyes", "wide eyes",
    "looking at viewer", "looking away", "looking up", "looking down", "looking aside",
    "side glance", "rolling eyes", "winking", "squinting", "gentle gaze", "sharp gaze",
    "sleepy eyes", "tears in eyes", "sparkling eyes", "bedroom eyes",
]
BROWS_BASE = [
    "relaxed brows", "raised brows", "furrowed brows", "knitted brows",
    "one brow raised", "worried brows",
]

# --- 表情: 感情 (Expression: Emotion) ---
MOOD_JOY = ["happy", "cheerful", "joyful", "elated", "ecstatic", "beaming", "gleeful", "content", "pleased", "amused"]
MOOD_SADNESS = ["sad", "unhappy", "melancholy", "sorrowful", "dejected", "depressed", "heartbroken", "crying", "tearful"]
MOOD_ANGER = ["angry", "furious", "enraged", "annoyed", "irritated", "frustrated", "pouting", "glaring", "scowling"]
MOOD_SURPRISE = ["surprised", "shocked", "astonished", "amazed", "startled", "gasping"]
MOOD_FEAR = ["afraid", "scared", "terrified", "anxious", "nervous", "worried"]
MOOD_NEUTRAL = ["neutral expression", "calm", "serene", "thoughtful", "pensive", "bored", "apathetic", "serious"]
MOOD_ALLURE = ["seductive", "alluring", "flirtatious", "coy", "shy", "mischievous", "playful", "confident", "smug", "inviting"]
MOOD_EROTIC = ["lustful", "aroused", "passionate", "sensual", "yearning", "in heat", "ecstasy", "orgasmic expression", "breathless", "smoldering intensity"]

# --- その他 (Others) ---
EFFECTS = ["blush", "heavy blush", "sweat", "beads of sweat", "tears", "streaming tears", "wind-blown hair", "motion blur"]

# ========================================
# 2. モードとテーマパックの再構築
# ========================================

POSE_MODES: Dict[str, Dict[str, List[str]]] = {
    "daily": {
        "standing": POSE_STANDING, "sitting": POSE_SITTING, "lying": POSE_LYING,
        "hands": _merge_unique(HAND_POSITIONS, HAND_GESTURES),
        "legs": LEG_POSITIONS, "spine": SPINE_AND_SHOULDERS,
    },
    "action": {
        "standing": POSE_STANDING, "dynamic": POSE_DYNAMIC,
        "hands": _merge_unique(HAND_POSITIONS, ["fist clenched", "pointing", "open palm"]),
        "legs": LEG_POSITIONS, "spine": SPINE_AND_SHOULDERS,
    },
}

EXPRESSION_MODES: Dict[str, Dict[str, List[str]]] = {
    "daily": {"mood": _merge_unique(MOOD_NEUTRAL, MOOD_JOY, MOOD_SADNESS)},
    "allure": {"mood": MOOD_ALLURE},
    "joy": {"mood": MOOD_JOY},
    "sadness": {"mood": MOOD_SADNESS},
    "anger": {"mood": MOOD_ANGER},
    "erotic": {"mood": _merge_unique(MOOD_ALLURE, MOOD_EROTIC)},
}

EMOTION_THEME_PACKS: Dict[str, Dict[str, object]] = {
    "Jubilant_Joy": {
        "tags": {
            "pose": [
                "jumping with arms wide",
                "dancing mid-spin",
                "cheerful skip",
                "hands raised in celebration",
                "leaping forward",
            ],
            "expression": [
                "radiant smile",
                "beaming eyes",
                "joyful laughter",
                "sparkling eyes",
                "grinning with delight",
            ],
            "camera": ["wide angle", "dynamic full-body shot", "slightly tilted celebration shot"],
            "accent": ["confetti burst", "sunlit glow"],
        },
        "focus": {
            "pose": ["pose_dynamic", "pose_standing"],
            "expression": ["joy"],
        },
        "conflicts": {
            "pose_categories": ["pose_lying"],
            "mood_labels": ["sadness", "anger", "erotic", "allure"],
            "tags": ["tears", "crying", "melancholy", "grimace"],
        },
    },
    "Quiet_Sorrow": {
        "tags": {
            "pose": [
                "hugging knees close",
                "sitting curled on the floor",
                "slumped shoulders",
                "head bowed and hands clasped",
                "leaning against a wall in solitude",
            ],
            "expression": [
                "softly crying",
                "tearful gaze",
                "downturned lips",
                "glassy eyes",
                "somber expression",
            ],
            "camera": ["intimate close-up", "overhead melancholy shot", "window light with rain"],
            "accent": ["raindrops on cheeks", "dim ambient glow"],
        },
        "focus": {
            "pose": ["pose_sitting", "pose_lying"],
            "expression": ["sadness"],
        },
        "conflicts": {
            "pose_categories": ["pose_dynamic"],
            "mood_labels": ["joy", "anger", "erotic", "allure"],
            "camera_tags": ["dutch angle", "hero shot"],
            "tags": ["radiant smile", "laughing", "celebratory"],
        },
    },
    "Burning_Anger": {
        "tags": {
            "pose": [
                "power stance with clenched fists",
                "forward-leaning confrontation",
                "shouting mid-gesture",
                "arms thrown wide in fury",
            ],
            "expression": [
                "furious glare",
                "snarling",
                "teeth bared",
                "brows sharply furrowed",
                "shouting with intensity",
            ],
            "camera": ["low angle", "dynamic dutch angle", "high-contrast lighting"],
            "accent": ["embers flying", "crackling aura"],
        },
        "focus": {
            "pose": ["pose_dynamic", "pose_standing"],
            "expression": ["anger"],
        },
        "conflicts": {
            "pose_categories": ["pose_lying"],
            "mood_labels": ["joy", "sadness", "erotic"],
            "tags": ["tearful", "soft smile", "bashful"],
        },
    },
    "Seductive_Allure": {
        "tags": {
            "pose": [
                "arched back with one hand in hair",
                "leaning forward with inviting gaze",
                "seated with crossed legs and tilted chin",
                "standing with hip cocked",
            ],
            "expression": [
                "sultry smile",
                "languid eyes",
                "biting lip",
                "playful wink",
                "half-lidded gaze",
            ],
            "camera": ["medium close-up", "bust shot", "soft rim lighting"],
            "accent": ["softly glowing highlights", "perfumed haze"],
        },
        "focus": {
            "pose": ["pose_standing", "pose_sitting", "pose_dynamic"],
            "expression": ["allure"],
        },
        "conflicts": {
            "pose_categories": ["pose_lying"],
            "mood_labels": ["sadness", "anger"],
            "tags": ["tears", "rage", "awkward grin"],
        },
    },
    "Deep_Ponder": {
        "tags": {
            "pose": [
                "sitting cross-legged with chin in hand",
                "leaning on railing lost in thought",
                "hand resting against temple",
                "standing with arms gently folded",
            ],
            "expression": [
                "thoughtful gaze",
                "soft focus eyes",
                "subtle smile of contemplation",
                "slight frown in concentration",
            ],
            "camera": ["face shot", "shoulder-level portrait", "window light profile"],
            "accent": ["dust motes in sunlight", "pen poised above notebook"],
        },
        "focus": {
            "pose": ["pose_sitting", "pose_standing"],
            "expression": ["daily", "neutral"],
        },
        "conflicts": {
            "pose_categories": ["pose_dynamic", "pose_lying"],
            "mood_labels": ["anger", "erotic"],
            "tags": ["tears", "wild laughter", "scream"],
        },
    },
    "Passionate_Embrace": {
        "tags": {
            "pose": [
                "arched back against unseen partner",
                "lying back with arms overhead",
                "legs entwined",
                "hands gripping sheets",
            ],
            "expression": [
                "breathless",
                "eyes half closed",
                "biting lip",
                "flushed ecstasy",
                "soft moan",
            ],
            "camera": ["tight crop", "close-up", "dramatic chiaroscuro lighting"],
            "accent": ["glowing sweat sheen", "rumpled fabric"],
        },
        "focus": {
            "pose": ["pose_lying", "pose_sitting"],
            "expression": ["erotic", "allure"],
        },
        "conflicts": {
            "pose_categories": ["pose_dynamic", "pose_standing"],
            "mood_labels": ["sadness", "anger", "joy"],
            "tags": ["tears", "smirk", "grin"],
        },
    },
}

# ========================================
# 3. 排他タググループの導入
# ========================================
EXCLUSIVE_TAG_GROUPS: Dict[str, List[str]] = {
    "posture": _merge_unique(POSE_STANDING, POSE_SITTING, POSE_LYING, POSE_DYNAMIC),
    "gaze_direction": ["looking at viewer", "looking away", "looking up", "looking down", "looking aside"],
    "arm_state": ["arms crossed", "arms outstretched", "hands on hips", "waving"],
}

# ========================================
# 4. NSFW語彙の管理（スクリプト内定義版）
# ========================================

# --- サジェスティブ（非露骨）強化語彙 ---
NSFW_SUGGESTIVE_HAND = ["hand tracing collarbone", "thumb grazing lower lip", "hands adjusting strap", "fingers hooking hem lightly", "hand on inner thigh (implied)"]
NSFW_SUGGESTIVE_LEG = ["thighs gently pressed", "tiptoe with arched back", "one knee inward tilt"]
NSFW_SUGGESTIVE_SPINE = ["exaggerated hip tilt", "deep back arch", "shoulders drawn back subtly"]
NSFW_SUGGESTIVE_CAMERA = ["tight crop on lips", "tight crop on neckline", "crop just above bust"]
NSFW_SUGGESTIVE_INTER = ["pinching fabric at hip", "gathering hem slightly", "playing with necklace"]
NSFW_SUGGESTIVE_MOUTH = ["moist-looking lips", "parted lips with soft breath"]
NSFW_SUGGESTIVE_EYES = ["smoldering gaze", "languid eyes"]
NSFW_SUGGESTIVE_MOOD = ["sensual allure", "shy arousal", "yearning warmth"]
NSFW_SUGGESTIVE_BLUSH = ["deep blush", "full body blush"]
NSFW_SUGGESTIVE_SWEAT = ["subtle perspiration on collarbone", "glistening skin"]
NSFW_SUGGESTIVE_MICRO = ["barely parted teeth", "quivering lips"]

# --- 露骨な語彙（スクリプト内直書き） ---
# [更新] ユーザー提供の語彙を直接リストとして定義
EXPLICIT_SEX_POSES: List[str] = [
    "missionary position",
    "cowgirl position",
    "reverse cowgirl",
    "riding on top",
    "standing sex",
    "against the wall",
    "legs wrapped around waist",
    "lap sitting sex",
    "straddling partner",
    "deep penetration",
    "grinding hips",
    "hip thrusting",
    "side-by-side sex",
    "spooning sex",
    "prone bone position",
    "doggystyle position",
    "on hands and knees",
    "from behind",
    "bent over sex",
    "arched back sex pose",
    "full body embrace",
    "intertwined legs",
    "lifting partner",
    "holding ankles",
    "leaning back in partner's arms",
]

EXPLICIT_SEX_LEXICON: List[str] = _dedupe([
    "torogao",
    "rolling eyes",
    "sweat",
    "screaming",
    "spit",
    "fucked silly",
    "mind break",
    "female orgasm",
    "motion lines",
    "aroused",
    "moaning",
    "blush",
    "plap",
    "ahegao",
    "smile",
    "tongue",
    "tongue out",
    "rough sex",
    "forced sex",
    "rape",
    "embarrassed",
    "clenched teeth",
])

EXTRA_EROTIC_POSES: List[str] = [] # 外部読み込み廃止のため空リストに

# --- 統合プール ---
EXTRA_NSFW_POSE: List[str] = _merge_unique(
    NSFW_SUGGESTIVE_HAND, NSFW_SUGGESTIVE_LEG, NSFW_SUGGESTIVE_SPINE,
    NSFW_SUGGESTIVE_CAMERA, NSFW_SUGGESTIVE_INTER,
    EXTRA_EROTIC_POSES,
    EXPLICIT_SEX_POSES,
)

EXTRA_NSFW_EXPR: List[str] = _merge_unique(
    NSFW_SUGGESTIVE_MOUTH, NSFW_SUGGESTIVE_EYES, NSFW_SUGGESTIVE_MOOD,
    NSFW_SUGGESTIVE_BLUSH, NSFW_SUGGESTIVE_SWEAT, NSFW_SUGGESTIVE_MICRO,
    EXPLICIT_SEX_LEXICON,
)

# --- ブロック集合の自動生成 ---
def _compile_blockset() -> Set[str]:
    """露骨語を明示的な単語リストでブロック対象へ。"""
    manual_block_words = {"rape", "forced sex"}
    base: Set[str] = {word.lower() for word in manual_block_words}
    for tag in _merge_unique(EXPLICIT_SEX_LEXICON, EXPLICIT_SEX_POSES):
        if not tag:
            continue
        base.add(tag.lower())
    return base

EXPLICIT_BLOCKLIST: Set[str] = _compile_blockset()

# ========================================
# 5. エクスポート
# ========================================
__all__ = [
    # 語彙
    "VIEW_ANGLES", "VIEW_FRAMING", "POSE_STANDING", "POSE_SITTING", "POSE_LYING", "POSE_DYNAMIC",
    "HAND_POSITIONS", "HAND_GESTURES", "SPINE_AND_SHOULDERS", "LEG_POSITIONS",
    "MOUTH_BASE", "EYES_BASE", "BROWS_BASE",
    "MOOD_JOY", "MOOD_SADNESS", "MOOD_ANGER", "MOOD_SURPRISE", "MOOD_FEAR", "MOOD_NEUTRAL", "MOOD_ALLURE", "MOOD_EROTIC",
    "EFFECTS",
    # モードとテーマ
    "POSE_MODES", "EXPRESSION_MODES", "EMOTION_THEME_PACKS",
    # 排他グループ
    "EXCLUSIVE_TAG_GROUPS",
    # NSFW関連
    "NSFW_SUGGESTIVE_HAND", "NSFW_SUGGESTIVE_LEG", "NSFW_SUGGESTIVE_SPINE",
    "NSFW_SUGGESTIVE_CAMERA", "NSFW_SUGGESTIVE_INTER",
    "NSFW_SUGGESTIVE_MOUTH", "NSFW_SUGGESTIVE_EYES", "NSFW_SUGGESTIVE_MOOD",
    "NSFW_SUGGESTIVE_BLUSH", "NSFW_SUGGESTIVE_SWEAT", "NSFW_SUGGESTIVE_MICRO",
    "EXTRA_NSFW_POSE", "EXTRA_NSFW_EXPR",
    "EXPLICIT_BLOCKLIST",
]

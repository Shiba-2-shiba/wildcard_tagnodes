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
from pathlib import Path
from typing import List, Dict, Set
import re

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

EMOTION_THEME_PACKS: Dict[str, Dict[str, List[str]]] = {
    "Jubilant_Joy": {
        "pose_boost": ["jumping", "dancing", "twirling", "arms outstretched", "leaping"],
        "expr_boost": ["ecstatic", "beaming", "laughing", "joyful", "sparkling eyes"],
        "camera_boost": ["wide angle", "full shot", "dynamic pose"],
    },
    "Quiet_Sorrow": {
        "pose_boost": ["hugging knees", "sitting on the floor", "slumped shoulders", "head down", "covering face"],
        "expr_boost": ["melancholy", "crying", "tearful", "sorrowful", "furrowed brows"],
        "camera_boost": ["close-up", "from above", "rainy"],
    },
    "Burning_Anger": {
        "pose_boost": ["power stance", "fist clenched", "fighting stance", "pointing"],
        "expr_boost": ["furious", "glaring", "scowling", "shouting", "enraged"],
        "camera_boost": ["dutch angle", "low angle", "dramatic lighting"],
    },
    "Seductive_Allure": {
        "pose_boost": ["arched back", "looking over shoulder", "touching hair", "one leg forward"],
        "expr_boost": ["seductive", "flirtatious", "biting lip", "winking", "smirk"],
        "camera_boost": ["medium close-up", "bust shot", "soft lighting"],
    },
    "Deep_Ponder": {
        "pose_boost": ["sitting cross-legged", "cupping chin", "leaning forward", "hand on cheek"],
        "expr_boost": ["pensive", "thoughtful", "serious", "neutral expression", "knitted brows"],
        "camera_boost": ["face shot", "point of view shot", "window light"],
    },
    "Passionate_Embrace": {
        "pose_boost": ["arched back", "lying on back", "hands behind head", "legs wrapped around", "embracing"],
        "expr_boost": ["lustful", "ecstasy", "biting lip", "breathless", "half-closed eyes", "passionate"],
        "camera_boost": ["close-up", "tight crop", "dramatic lighting", "shadows"],
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
    "Man and woman lie facing each other, close, legs entwined. He thrusts slowly while looking in her eyes. Closeness allows deep connection.",
    "Woman straddles man, leaning forward, supporting herself with hands. He enters her from behind. Deep penetration and control for her.",
    "Man kneels, woman wraps legs around him. He holds her waist, thrusting deeply. Intimacy and eye contact.",
    "Woman lies on edge of bed, legs lifted. Man stands, entering from above. Depth and pleasure for her, standing power for him.",
    "Man sits, woman straddles him backwards. She controls pace, he enjoys view.",
    "Woman leans against wall, man stands behind. He enters, holding her hips. Balance and support for her, dominance for him.",
    "Man lies, woman straddles, facing away. She sets pace, he watches her reactions.",
    "Man and woman stand, she wraps legs around him. He lifts, lowers at his pace. Strength and endurance.",
    "Woman lies, man kneels between legs. He controls depth and speed.",
    "Woman kneels, man stands behind. He holds her hips, she grabs his arms. Lean, sweaty bodies.",
    "Man lies, woman on top, facing him. He guides her movements. Eye contact.",
    "Woman sits, man kneels before her. She controls depth, he licks and kisses.",
    "Man lies, woman on top, facing away. She sets rhythm, he grips breasts.",
    "Man sits, woman faces side, straddles. He supports her with arms, she bounces.",
    "Woman lies, man kneels at side. He enters from above, she spreads legs wide.",
    "Man and woman sit, facing each other. They move together, slow and sensual.",
    "Man sits, woman straddles, facing away. He grips thighs, she sets pace.",
    "Man sits, woman on knees, facing him. He holds her hips, she rocks.",
    "Man kneels, woman straddles, facing away. She rides fast, he grips buttocks.",
    "Man sits, woman leans on elbow, facing him. He controls angle, she moves hips.",
    "Woman stands, man kneels, entering from behind. He holds her waist, she looks back.",
    "Man kneels, woman sits on lap, facing him. He controls depth, she grinds.",
    "Woman lies, man kneels, entering from side. He supports her head, she spreads legs.",
    "Man sits, woman straddles, facing side. He holds her waist, she leans back.",
    "Man and woman stand, facing each other, he lifts her. He has control, she wraps legs around.",
    "Woman kneels, man stands, facing her. He holds her hips, she grabs chest.",
    "Woman sits, man kneels behind. He grips her hips, she rests hands on floor.",
    "Woman lies, man kneels beside, entering from side. He supports her, she relaxes.",
    "Man lies, woman kneels, facing him. He grips her waist, she rocks.",
    "Woman sits, man kneels, facing away. He holds her hips, she grinds.",
    "Man stands, woman hangs from pull-up bar, he enters from behind. Thrill and danger.",
    "Man and woman stand, facing each other, he lifts her. She wraps legs around.",
    "Woman sits, man kneels, facing her. He holds her waist, she grinds.",
    "Woman lies, man kneels, entering from side. He supports her head, she closes eyes.",
    "Man sits, woman straddles, facing him. He grips thighs, she moves hips.",
    "Woman kneels, man stands, facing her. He holds her hips, she touches chest.",
    "Man lies, woman straddles, facing away. He grips her waist, she sets rhythm.",
    "Man kneels, woman straddles, facing him. He grips her buttocks, she bounces.",
    "Woman lies, man kneels, entering from side. He supports her, she arches back.",
    "Man sits, woman on lap, facing away. He holds her hips, she leans forward.",
    "Woman sits, man kneels behind. He grips her hips, she braces on hands.",
    "Man and woman lie side by side, facing same direction. He enters her from behind, shallow strokes. Soft and intimate.",
    "Woman on hands and knees, man stands behind. He holds her hips, deep penetration. Powerful and animalistic.",
    "Man and woman stand, she wraps legs around him. He lifts and lowers. Balance and strength.",
    "Woman lies on back, man kneels between legs. He supports her with hands. Sensitivity and intimacy.",
    "Man sits, woman straddles, facing away. She sets pace, he caresses breasts.",
    "Woman crouches, man stands. He grips her hips, she bounces.",
    "Man lies, woman sits on lap, facing away. He holds her hips, she grinds.",
    "Man and woman lie face to face, legs entwined. Shallow and sensual.",
    "Woman kneels, man stands, entering from behind. He holds her hair, she moans.",
    "Man kneels, woman sits on lap, facing him. He grips her hips, she rocks.",
    "Woman lies, man kneels beside, entering from side. He supports her head, she closes eyes.",
    "Woman crouches, man stands, facing her. He holds her hips, she bends forward.",
    "Man lies, woman on all fours. He enters from behind, dominant.",
    "Man sits, woman straddles, facing away. He grips her waist, she sets pace.",
    "Woman kneels, man stands, facing her. He holds her hips, she touches her feet.",
    "Man lies, woman sits on lap, facing away. He holds her hips, she leans forward.",
    "Man kneels, woman straddles, facing him. He grips her thighs, she bounces.",
    "Woman lies, man kneels, entering from side. He supports her head, she arches back.",
    "Man sits, woman on lap, facing him. He holds her hips, she grinds.",
    "Woman sits, man kneels behind. He grips her hips, she leans back.",
    "Man lies, woman sits on lap, facing him. He grips her waist, she rocks.",
    "Woman kneels, man stands, facing her. He holds her hips, she touches her breasts.",
    "Man lies, woman straddles, facing away. He grips her buttocks, she sets pace.",
    "Woman lies, man kneels, entering from side. He supports her, she closes eyes.",
    "Man kneels, woman straddles, facing him. He grips her waist, she moves hips.",
    "Man lies, woman on all fours, he enters from behind. Dominant and primal.",
    "Man sits, woman straddles, facing him. He grips thighs, she sets pace.",
    "Woman kneels, man stands, facing her. He holds her hips, she touches her toes.",
    "Man and woman embrace, making love while standing. Their bodies press together as he thrusts into her.",
    "Woman on top, riding man's hardness. Her movements control the intensity as his hands roam her body.",
    "Man on back, woman straddling him, facing away. His grip on her waist guides their connection.",
    "Woman leaning against surface, man behind, filling her. His hands support her as she moans in pleasure.",
    "Woman sitting, man kneeling before her. She rides his length with controlled ease.",
    "Man and woman sit facing, moving in a slow dance of desire. Their eyes locked as they connect.",
    "Woman on man's lap, facing away, taking him in. He watches her reactions to every stroke.",
    "Man reclining, woman on top, facing him. He admires her beauty while she moves.",
    "Woman sits, man kneeling, enjoying her every sound. He explores her body with his mouth.",
    "Woman lying, man kneeling, entering from the side. He cradles her head gently.",
    "Man sitting, woman straddling, facing him. His hands explore her body as she rides him.",
    "Woman kneeling, man standing, entering from behind. He grips her hips, pulling her close.",
    "Man lying, woman straddling, facing away. He reaches for her breasts, guiding her motion.",
    "Woman sitting, man kneeling, facing her. He enters her slowly, savoring the moment.",
    "Man kneeling, woman straddling, facing him. He grips her buttocks, matching her rhythm.",
    "Woman lying, man kneeling, entering from the side. He supports her comfortably.",
    "Man sitting, woman on lap, facing away. His hands caress her as she leans forward.",
    "Woman sitting, man kneeling behind. Her hands brace on the floor as he drives deeper.",
    "Man and woman sitting close, moving in harmony. Their lips meet as they share passion.",
    "Woman kneeling, man standing, behind her. He whispers sweet nothings in her ear.",
    "Man lying, woman on top, facing away. He reaches under her, touching her intimately.",
    "Woman sitting, man kneeling, facing her. He kisses her neck as she rocks on his member.",
    "Man kneeling, woman straddling, facing him. He massages her back as she rides him.",
    "Woman lying, man kneeling, entering from the side. He cradles her head, whispering encouragement.",
    "Man sitting, woman on lap, facing away. He holds her hips, pulling her closer.",
    "Woman sitting, man kneeling, facing her. He enters her softly, savoring the moment.",
    "Man kneeling, woman straddling, facing him. He grips her thighs, urging her on.",
    "Woman lying, man kneeling, entering from the side. He supports her weight, watching her expression.",
    "Man sitting, woman on lap, facing him. He grips her hips, encouraging her movement.",
    "Woman kneeling, man standing, behind her. His hands explore her body as she enjoys the sensation.",
    "Man lying, woman kneeling, facing him. He holds her hips, feeling her muscles clench.",
    "Woman sitting, man kneeling, facing away. He kisses her neck, matching her pace.",
    "Man and woman sit facing, intertwining their limbs. Their breaths mingle as they make love.",
    "Woman crouching, man standing, facing her. He grips her hips, lifting and lowering her.",
    "Man lying, woman on all fours, taking him deep. He dominates their encounter.",
    "Man sitting, woman straddling, facing him. He grips her thighs, feeling her heat.",
    "Woman kneeling, man standing, facing her. He pulls her hair slightly, increasing intensity.",
    "Man lying, woman on all fours, behind her. He penetrates her deeply, relentlessly.",
    "Man sitting, woman on lap, facing away. He holds her hips, her sounds fill the room.",
    "Woman sitting, man kneeling behind. He plays with her nipples, heightening her pleasure.",
    "Man and woman stand, their bodies entwined. They move together in a passionate frenzy.",
    "Woman crouching, man standing, facing her. He holds her hips, watching her expressions.",
    "Man lying, woman on all fours, entering from behind. He gazes at her curves.",
    "Man sitting, woman straddles, facing him. He kisses her passionately, their tongues intertwine.",
    "Woman kneeling, man standing, facing her. He grips her hips, their eyes lock.",
    "Man lying, woman straddling, facing away. He strokes her clit, bringing her closer to climax.",
    "Man kneeling, woman straddling, facing him. He grips her waist, her moans fill the air.",
    "Woman lying, man kneeling, entering from the side. He supports her head, their gazes meet."
]

# [更新] ユーザー提供の語彙をパースしてリスト化
_raw_lexicon = [
    "torogao, rolling eyes, sweat, screaming, spit, fucked silly, mind break, female orgasm, motion lines, aroused, moaning, blush, plap,",
    "Ahegao, sweat, spit, fucked silly, plap, mind break, female orgasm, rolling eyes, motion lines, aroused, moaning, blush, smile, tongue, tongue out,",
    " sweat, rolling eyes, spit, fucked silly, plap, mind break, female orgasm, rolling eyes, motion lines, aroused, moaning, blush, rough sex, forced sex, rape,",
    "sweat, spit, plap, mind break, female orgasm, motion lines, aroused, moaning, blush",
    "sweat, spit, fucked silly, plap, mind break, female orgasm, motion lines, aroused, moaning, blush",
    "embarrassed, clenched teeth, sweat, spit, fucked silly, plap, mind break, female orgasm, rolling eyes, motion lines, aroused, moaning, blush,"
]
EXPLICIT_SEX_LEXICON: List[str] = _dedupe([tag.strip() for line in _raw_lexicon for tag in line.split(',') if tag.strip()])

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
    """露骨語をフレーズとサブワードでブロック対象へ。"""
    base: Set[str] = set()
    # [更新] rape, forced sex などの特に強い単語を明示的にブロックリストへ追加
    manual_block_words = {"rape", "forced sex"}
    base.update(manual_block_words)

    for s in _merge_unique(EXPLICIT_SEX_LEXICON, EXPLICIT_SEX_POSES):
        low = s.lower()
        base.add(low)
        for w in re.split(r"[^a-zA-Z0-9]+", low):
            if len(w) >= 8: # 一定文字数以上の単語をブロック対象に追加
                base.add(w)
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

# -*- coding: utf-8 -*-
"""
vocab/pose_emotion_vocab.py

ポーズ＋表情の語彙を統合し、外部テキスト（提供ファイル）由来のNSFW語彙（露骨含む）も
「語彙として保持」しつつ、最終出力で除去するためのブロック集合(EXPLICIT_BLOCKLIST)を生成する。
実際の出力サニタイズはノード実装側(pose_emotion_tag.py)で行う想定。

・既存の pose_vocab / expression_vocab を取り込み、モード（daily/action/…）を維持して拡張
・外部テキストを起動時に読み込んで EXTRA_NSFW_POSE / EXTRA_NSFW_EXPR に統合
・同外部テキストから EXPLICIT_BLOCKLIST を自動生成（フレーズ＆サブワード）
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Set
import re

# ===== 既存の語彙を取り込み =====
from .pose_vocab import (
    POSE_VIEW,
    POSE_BODY_DAILY, POSE_MOTION_DAILY, POSE_PROPS_DAILY,
    POSE_BODY_ACTION, POSE_MOTION_ACTION, POSE_PROPS_ACTION,
)
from .expression_vocab import (
    MOUTH_DAILY, EYES_DAILY, MOOD_DAILY,
    MOUTH_ALLURE, EYES_ALLURE, MOOD_ALLURE,
    BROW_COMMON,
)

# ===== 実用ユーティリティ（ローカル簡易） =====
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

# ===== 既存＋基本拡張（安全側）の細分カテゴリ =====
# ポーズ側（核＋細分）
HAND_PLACEMENT = [
    "hand on cheek", "hand on neck", "hand on chest", "one hand on waist",
    "fingers through hair", "hand near lips",
]
LEG_POSITION = [
    "legs crossed", "one leg raised on surface", "knees together",
    "on tiptoes", "kneeling with one knee up",
]
SPINE_SHOULDER = [
    "arched back", "gentle S-curve", "waist shift", "shoulders relaxed",
]
CAMERA_FRAMING = [
    "bust-up shot", "waist-up shot", "full-length shot", "close-up face",
]
INTERACTION = [
    "leaning against wall", "holding fabric", "touching hair", "sitting on chair",
]

# 表情側（核＋細分）
LID_STATE = ["half-closed lids", "wide-open lids", "sleepy eyes"]
EYE_GAZE  = ["looking at viewer", "downcast gaze", "side glance", "upward glance"]
MOUTH_ACTION = _merge_unique(MOUTH_DAILY, MOUTH_ALLURE, [
    "soft smile", "half-open lips", "gentle smirk",
])
BLUSH = ["light blush", "cheeks slightly flushed"]
SWEAT = ["dewy sheen"]          # 汗だく表現ではなく艶寄り
TEAR  = ["shimmering eyes"]     # 泣き顔ではなく潤み表現
MICRO_EXP = ["slight brow knit", "tiny mouth corner lift"]

# ===== サジェスティブ（非露骨）強化語彙 =====
NSFW_SUGGESTIVE_HAND = [
    "hand tracing collarbone", "thumb grazing lower lip", "hands adjusting strap",
    "fingers hooking hem lightly", "hand on inner thigh (implied)",
]
NSFW_SUGGESTIVE_LEG = [
    "thighs gently pressed", "tiptoe with arched back", "one knee inward tilt",
]
NSFW_SUGGESTIVE_SPINE = [
    "exaggerated hip tilt", "deep back arch", "shoulders drawn back subtly",
]
NSFW_SUGGESTIVE_CAMERA = [
    "tight crop on lips", "tight crop on neckline", "crop just above bust",
]
NSFW_SUGGESTIVE_INTER = [
    "pinching fabric at hip", "gathering hem slightly", "playing with necklace",
]
NSFW_SUGGESTIVE_MOUTH = [
    "biting lower lip", "moist-looking lips", "parted lips with soft breath",
]
NSFW_SUGGESTIVE_EYES = [
    "bedroom eyes", "smoldering gaze", "languid eyes",
]
NSFW_SUGGESTIVE_MOOD = [
    "sensual allure", "shy arousal", "yearning warmth",
]
NSFW_SUGGESTIVE_BLUSH = ["deep blush"]
NSFW_SUGGESTIVE_SWEAT = ["subtle perspiration on collarbone"]
NSFW_SUGGESTIVE_MICRO = ["barely parted teeth"]

# ===== モード集合（既存ベース＋軽い追加） =====
POSE_MODES: Dict[str, Dict[str, List[str]]] = {
    "daily": {
        "body": POSE_BODY_DAILY,
        "view": POSE_VIEW,
        "motion": POSE_MOTION_DAILY,
        "props": POSE_PROPS_DAILY,
    },
    "action": {
        "body": _merge_unique(POSE_BODY_DAILY, POSE_BODY_ACTION),
        "view": POSE_VIEW,
        "motion": _merge_unique(POSE_MOTION_DAILY, POSE_MOTION_ACTION),
        "props": _merge_unique(POSE_PROPS_DAILY, POSE_PROPS_ACTION),
    },
    # 追加モードは最小種でスタート（運用で随時拡充）
    "fashion": {
        "body": ["contrapposto", "waist shift"],
        "view": POSE_VIEW,
        "motion": ["hip sway", "hair flip"],
        "props": ["holding fabric"],
    },
    "gravure": {
        "body": ["arched back", "on tiptoes"],
        "view": CAMERA_FRAMING,
        "motion": ["over-the-shoulder glance"],
        "props": ["lifting hem"],
    },
}

EXPRESSION_MODES: Dict[str, Dict[str, List[str]]] = {
    "daily": {
        "mouth": MOUTH_DAILY,
        "eyes": EYES_DAILY,
        "mood": MOOD_DAILY,
        "brow": BROW_COMMON,
    },
    "allure": {
        "mouth": _merge_unique(MOUTH_DAILY, MOUTH_ALLURE),
        "eyes":  _merge_unique(EYES_DAILY,  EYES_ALLURE),
        "mood":  _merge_unique(MOOD_DAILY,  MOOD_ALLURE),
        "brow":  BROW_COMMON,
    },
    "cute":  {"mouth": ["soft smile"], "eyes": ["doe-eyed look"], "mood": ["cheerful"], "brow": BROW_COMMON},
    "cool":  {"mouth": ["closed mouth"], "eyes": ["relaxed eyes"], "mood": ["serene look"], "brow": BROW_COMMON},
}

# ===== テーマパック（軽ブースト用の束） =====
THEME_PACKS: Dict[str, Dict[str, List[str]]] = {
    "runway": {
        "pose_boost": ["contrapposto", "waist shift", "front view"],
        "expr_boost": ["confident allure"],
        "camera_boost": ["full-length shot"],
    },
    "pinup": {
        "pose_boost": ["arched back", "on tiptoes", "over-the-shoulder glance"],
        "expr_boost": ["playful tease", "seductive smile"],
        "camera_boost": ["bust-up shot", "waist-up shot"],
    },
}

# ===== 外部テキスト由来のNSFW語彙を読み込む =====
# 置き場所の候補：パッケージ直下の `vocab/external/` または /mnt/data
_CANDIDATE_DIRS: List[Path] = [
    Path(__file__).resolve().parent / "external",
    Path("/mnt/data"),
]

# ファイル名（あなたの提供物を想定）
_EXTERNAL_FILES: Dict[str, List[str]] = {
    "pose_sex":         ["pose_sex.txt"],            # 性行為ポーズ（露骨な記述を含みうる）
    "sexual_emotions":  ["sexual emotions.txt"],     # 露骨な性的語彙（強語彙含む）
    "pose_erotic":      ["pose_erotic.txt"],         # 官能寄りポーズ
    "pose_action":      ["pose_action.txt"],         # アクション/動作ポーズ
    "hand_gestures":    ["pose_hand_gestures.txt"],  # 手のジェスチャ
    # 必要なら "C_sexpose.txt" 等をここに追加
}

def _load_lines(candidates: List[str]) -> List[str]:
    """候補ディレクトリから最初に見つかったファイルを読み込み、行配列で返す。"""
    print(f"--- 外部ファイル読み込み試行: {candidates}") # ← 追加
    for d in _CANDIDATE_DIRS:
        for fn in candidates:
            p = d / fn
            if p.exists():
                print(f"[読込成功] => {p}") # ← 追加
                raw = p.read_text(encoding="utf-8", errors="ignore").splitlines()
                # 基本は行ごとにフレーズとして保持（説明文っぽい長文も語彙として残す）
                out = [ (s or "").strip() for s in raw if (s or "").strip() ]
                return _dedupe(out)
    print(f"[読込失敗] ファイルが見つかりません: {candidates}") # ← 追加
    return []

# 外部語彙のロード（※露骨表現を含みうる。ここでは「保持」のみ）
EXPLICIT_SEX_POSES:   List[str] = _load_lines(_EXTERNAL_FILES["pose_sex"])
EXPLICIT_SEX_LEXICON: List[str] = _load_lines(_EXTERNAL_FILES["sexual_emotions"])

# suggestive/補助側（任意）
EXTRA_EROTIC_POSES:   List[str] = _load_lines(_EXTERNAL_FILES["pose_erotic"])
EXTRA_ACTION_POSES:   List[str] = _load_lines(_EXTERNAL_FILES["pose_action"])
EXTRA_HAND_GESTURES:  List[str] = _load_lines(_EXTERNAL_FILES["hand_gestures"])

# ===== 統合プール =====
# ・EXTRA_NSFW_POSE/EXTRA_NSFW_EXPR は “語彙として保持” するための統合リスト
# ・最終出力段で sanitize することで、露骨語は実際の出力には現れない設計
EXTRA_NSFW_POSE: List[str] = _merge_unique(
    # ベース（安全側）
    HAND_PLACEMENT, LEG_POSITION, SPINE_SHOULDER, CAMERA_FRAMING, INTERACTION,
    NSFW_SUGGESTIVE_HAND, NSFW_SUGGESTIVE_LEG, NSFW_SUGGESTIVE_SPINE,
    NSFW_SUGGESTIVE_CAMERA, NSFW_SUGGESTIVE_INTER,
    # ユーザ提供（安全寄り）
    EXTRA_EROTIC_POSES, EXTRA_ACTION_POSES, EXTRA_HAND_GESTURES,
    # ユーザ提供（露骨を含みうる）
    EXPLICIT_SEX_POSES,
)

EXTRA_NSFW_EXPR: List[str] = _merge_unique(
    # ベース（安全側）
    MOUTH_ACTION, EYE_GAZE, LID_STATE, MICRO_EXP, BLUSH, SWEAT, TEAR,
    NSFW_SUGGESTIVE_MOUTH, NSFW_SUGGESTIVE_EYES, NSFW_SUGGESTIVE_MOOD,
    NSFW_SUGGESTIVE_BLUSH, NSFW_SUGGESTIVE_SWEAT, NSFW_SUGGESTIVE_MICRO,
    # ユーザ提供（露骨を含みうる）
    EXPLICIT_SEX_LEXICON,
)

# ===== ブロック集合の自動生成 =====
def _compile_blockset() -> Set[str]:
    """
    外部テキスト由来の露骨語（性行為・性器・非同意・暴力などを含む強語彙）を
    そのままフレーズで登録し、加えて簡易にサブワードも抽出してブロック対象へ。
    """
    base: Set[str] = set()

    # 露骨な語彙（フレーズ単位）
    for s in _merge_unique(EXPLICIT_SEX_LEXICON, EXPLICIT_SEX_POSES):
        low = s.lower()
        base.add(low)
        # サブワードを抽出（4文字以上を対象にする簡易ルール）
        for w in re.split(r"[^a-zA-Z0-9]+", low):
            if len(w) >= 8:
                base.add(w)

    # ここで手動補強ワードがあれば base.add("...") を追加可能
    return base

EXPLICIT_BLOCKLIST: Set[str] = _compile_blockset()

# ===== エクスポート =====
__all__ = [
    # 既存＋拡張カテゴリ
    "HAND_PLACEMENT", "LEG_POSITION", "SPINE_SHOULDER", "CAMERA_FRAMING", "INTERACTION",
    "LID_STATE", "EYE_GAZE", "MOUTH_ACTION", "BLUSH", "SWEAT", "TEAR", "MICRO_EXP",
    # サジェスティブ追加
    "NSFW_SUGGESTIVE_HAND", "NSFW_SUGGESTIVE_LEG", "NSFW_SUGGESTIVE_SPINE",
    "NSFW_SUGGESTIVE_CAMERA", "NSFW_SUGGESTIVE_INTER",
    "NSFW_SUGGESTIVE_MOUTH", "NSFW_SUGGESTIVE_EYES", "NSFW_SUGGESTIVE_MOOD",
    "NSFW_SUGGESTIVE_BLUSH", "NSFW_SUGGESTIVE_SWEAT", "NSFW_SUGGESTIVE_MICRO",
    # モードとテーマ
    "POSE_MODES", "EXPRESSION_MODES", "THEME_PACKS",
    # 外部テキスト由来の統合プール
    "EXTRA_NSFW_POSE", "EXTRA_NSFW_EXPR",
    # 出力側で使うブロック集合
    "EXPLICIT_BLOCKLIST",
]
# vocab/pose_emotion_vocab.py の一番下に追加

print("#################### EXPLICIT_BLOCKLIST Content ####################")
# 中身をアルファベット順にソートして見やすくする
print(sorted(list(EXPLICIT_BLOCKLIST)))
print("#####################################################################")

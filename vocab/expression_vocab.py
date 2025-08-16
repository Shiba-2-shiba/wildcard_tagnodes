# vocab/expression_vocab.py
# 表情タグの語彙リスト

# ========================
# モード別語彙
# ========================

# --- 日常 (Daily): 穏やかで普段使いしやすい表現 ---
MOUTH_DAILY = [
    "soft smile", "closed mouth", "slight smile", "lips parted slightly", "open-mouth smile"
]
EYES_DAILY = [
    "gentle gaze", "looking at viewer", "relaxed eyes", "closed eyes", "happy eyes"
]
MOOD_DAILY = [
    "calm mood", "gentle warmth", "thoughtful expression", "serene look", "cheerful"
]

# --- 魅惑 (Allure): 色気や誘うような表現 ---
MOUTH_ALLURE = [
    "half-open lips", "slight pout", "biting lip", "gentle smirk", "licking lips", "seductive smile"
]
EYES_ALLURE = [
    "sultry gaze", "doe-eyed look", "side glance", "upward glance", "bedroom eyes", "wistful gaze", "mesmerizing eyes"
]
MOOD_ALLURE = [
    "shy charm", "playful tease", "confident allure", "innocent warmth", "mischievous vibe", "smoldering look", "inviting look"
]

# ========================
# 共通語彙
# ========================
# 眉の表現はどちらのモードでも共通して使用
BROW_COMMON = [
    "relaxed brows", "raised brows", "slightly furrowed brows"
]
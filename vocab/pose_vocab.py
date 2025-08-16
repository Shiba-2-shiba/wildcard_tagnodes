# vocab/pose_vocab.py
# ポーズ関連の語彙リスト

# ========================
# 共通の語彙
# ========================

# 視点・アングル
POSE_VIEW = [
    "front view", "three-quarter view", "profile view", "back view",
    "from below", "from above", "low angle", "high angle", "close-up torso",
    "waist-up shot", "full-length shot"
]

# ========================
# 「日常 (Daily)」モードの語彙
# ========================

# 基本的な体のポーズ
POSE_BODY_DAILY = [
    "standing straight", "contrapposto", "arched back", "leaning forward",
    "leaning against wall", "bent knees", "on tiptoes", "crossed legs",
    "kneeling", "sitting on heels", "one knee up", "crouching", "hands on hips",
    "arms crossed", "hands behind head", "hands covering chest", "one hand on thigh",
    "hands clasped", "arms raised", "full body stretch", "sitting on a chair"
]

# 動き・仕草
POSE_MOTION_DAILY = [
    "head tilt", "shoulder roll", "hip sway", "hair flip",
    "step forward", "turning around", "lean-in pose", "over-the-shoulder glance"
]

# 小道具・体の部位への接触
POSE_PROPS_DAILY = [
    "touching hair", "holding fabric", "gripping collar", "adjusting stockings",
    "lifting hem", "pulling glove", "biting lip gesture", "covering eyes gently",
    "holding a cup", "looking at phone"
]


# ========================
# 「アクション (Action)」モードの語彙
# ========================

# アクション系の体のポーズ
POSE_BODY_ACTION = [
    "action pose", "dynamic pose", "fighting stance", "ready for battle",
    "jumping", "running", "dodging", "crouching low", "kicking", "punching",
    "drawing a weapon", "aiming", "defensive stance", "landing after a jump"
]

# アクション系の動き
POSE_MOTION_ACTION = [
    "motion blur", "speed lines", "dramatic angle", "intense focus",
    "battle cry expression", "effortful expression", "wind-blown hair"
]

# 武器・小道具
POSE_PROPS_ACTION = [
    "holding a sword", "wielding a staff", "gripping a dagger", "aiming a bow",
    "holding a gun", "casting a spell", "shield raised", "clenched fist"
]
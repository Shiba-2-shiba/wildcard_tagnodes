# vocab/appearance_vocab.py
# 統合語彙: 体型 + 胸サイズ + 髪（長さ/質感/スタイル/前髪・分け目/色/色ミックス）+ テーマバイアス
# - 「美人寄り」の審美語彙をベースに、kawaii テーマへ petite 系（childlike 等）を集約
# - 髪は「単色 or ミックス」を排他的に選択しやすいよう代表値を厳選
# - 胸サイズは段階 + 付随属性（NSFW 寄りは別確率）で制御

# ===== Body（体型） =====
BODY_BASE = [
    # 美人寄り・審美的で中立的な語彙
    "slender yet toned",
    "graceful silhouette",
    "elegant curves",
    "balanced physique",
    "hourglass figure",
    "model-like proportions",
    "petite yet elegant",
    "tall and graceful",
]

BODY_DETAILS = [
    "defined waistline",
    "long elegant legs",
    "feminine shoulders",
    "subtle curves",
    "radiant posture",
]

# ===== Bust（胸） =====
# 段階表現（過度なスラング/扇情的俗語は避けた表現）
BUST_SIZES = [
    "flat chest",
    "small breasts",
    "medium breasts",
    "large breasts",
    "extra large breasts",
]

# 付随属性（ソフト系）：自然で審美的な付加情報
BUST_OPTIONS_SOFT = [
    "natural shape",
    "subtle lift",
    "full bust",
    "firm",
]

# 付随属性（NSFW寄り）：独立確率で低めに運用
BUST_OPTIONS_NSFW = [
    "sagging breasts",
    "puffy nipples",
]

# ===== Hair（髪） =====
# 長さ：冗長さを避けた代表値（原資料から正規化）
HAIR_LENGTHS = [
    "pixie cut",
    "short",
    "bob",
    "lob",
    "shoulder-length",
    "collarbone-length",
    "long",
    "very long",
    "waist-length",
]

# 質感/仕上げ：質感とフィニッシュを混ぜて運用（タグ数の伸びを抑える）
HAIR_TEXTURES = [
    "straight",
    "wavy",
    "curly",
    "silky smooth",
    "voluminous waves",
    "luxurious curls",
    "soft straight",
    "glossy",
    "shiny",
    "natural",
]

# スタイル/アレンジ
HAIR_ARRANGEMENTS = [
    "elegant updo",
    "half-up half-down",
    "loose ponytail",
    "high ponytail",
    "low ponytail",
    "side braid",
    "braided updo",
    "messy bun",
    "twin tails",
]

# 前髪/分け目
HAIR_BANGS_PART = [
    "no bangs",
    "wispy bangs",
    "curtain bangs",
    "soft fringe",
    "side-swept bangs",
    "blunt bangs",
    "middle part",
    "deep side part",
]

# 単色（代表値）
HAIR_COLORS = [
    "black",
    "dark brown",
    "light brown",
    "blonde",
    "platinum blonde",
    "ash blonde",
    "auburn",
    "burgundy",
    "chestnut",
    "copper",
    "rose gold",
]

# ミックス/バレイヤージュ系（代表値）※単色とは排他運用を想定
HAIR_COLOR_MIX = [
    "chocolate and caramel",
    "honey and brown",
    "rose gold and blonde",
    "jet black and blonde",
    "emerald green and blonde",
    "cobalt blue and blonde",
]

# ===== Themes（テーマ） =====
# - body_bias: 体型の出目に傾きを与えるバイアス
# - hair_bias: 髪の出目に傾きを与えるバイアス（appearance_tag 側で確率適用）
THEMES = {
    "model": {
        "body_bias": [
            "model-like proportions",
            "tall and graceful",
            "balanced physique",
        ],
        "hair_bias": [
            "elegant updo",
            "waist-length",
            "glossy",
        ],
    },
    "kawaii": {
        # ★ petite 系と幼さニュアンスはここに集約（ユーザ要望）
        "body_bias": [
            "petite yet elegant",
            "childlike",
            "doll-like",
            "little girl frame",
            "girlish",
            "innocent look",
            "cute childish charm",
        ],
        "hair_bias": [
            "twin tails",
            "curtain bangs",
            "soft fringe",
        ],
    },
    "gothic": {
        "body_bias": [],
        "hair_bias": [
            "elegant updo",
            "deep side part",
            "black",
        ],
    },
    "wasou": {
        "body_bias": [],
        "hair_bias": [
            "elegant updo",
            "soft fringe",
            "low ponytail",
        ],
    },
}

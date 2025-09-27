# vocab/appearance_vocab.py
# 外見（体・肌・顔・髪）タグ用語彙の刷新版

# ===== Body =====
BODY_SHAPES = [
    "slender frame",
    "athletic build",
    "graceful curves",
    "petite frame",
    "statuesque form",
    "hourglass silhouette",
    "softly rounded figure",
    "toned dancer physique",
    "delicate build",
]

BODY_DETAILS = [
    "defined waistline",
    "long elegant legs",
    "sculpted abs",
    "soft shoulders",
    "delicate collarbones",
    "balletic posture",
    "lithe limbs",
    "graceful neck",
]

SKIN_DETAILS = {
    "tones": [
        "porcelain skin",
        "pale rosy skin",
        "fair neutral skin",
        "warm beige skin",
        "golden olive skin",
        "sun-kissed tan skin",
        "bronzed skin",
        "deep cocoa skin",
        "rich ebony skin",
    ],
    "features": [
        "dusting of freckles",
        "delicate freckles",
        "rosy cheeks",
        "soft blush",
        "beauty mark below eye",
        "beauty mark near lips",
        "subtle sun spots",
        "mole on cheek",
    ],
    "finishes": [
        "dewy complexion",
        "luminous glow",
        "velvety smooth skin",
        "matte porcelain finish",
        "radiant sheen",
    ],
}

# ===== Hair =====
HAIR_LENGTHS = [
    "pixie cut",
    "short crop",
    "chin-length bob",
    "shoulder-length",
    "collarbone-length",
    "mid-back length",
    "waist-length",
    "hip-length",
]

HAIR_TEXTURES = [
    "sleek straight",
    "silky straight",
    "soft wavy",
    "gentle waves",
    "loose curls",
    "defined curls",
    "spiral curls",
    "coily texture",
    "fluffy volume",
    "smooth layers",
]

HAIR_STYLES = [
    "loose flowing",
    "half-up half-down",
    "twin tails",
    "high ponytail",
    "low ponytail",
    "side ponytail",
    "loose braid",
    "braided crown",
    "messy bun",
    "elegant updo",
]

HAIR_BANGS_PART = [
    "no bangs",
    "wispy bangs",
    "soft fringe",
    "curtain bangs",
    "blunt bangs",
    "side-swept bangs",
    "middle part",
    "off-center part",
    "deep side part",
]

HAIR_COLORS = [
    "jet black",
    "blue-black",
    "dark brown",
    "chocolate brown",
    "chestnut brown",
    "auburn",
    "copper",
    "honey blonde",
    "strawberry blonde",
    "platinum blonde",
    "ash blonde",
    "silver gray",
    "rose pink",
    "lavender",
    "teal",
]

HAIR_COLOR_MIX = [
    "caramel and chestnut balayage",
    "honey and chocolate highlights",
    "rose gold ombre",
    "peach and blonde gradient",
    "silver and lavender melt",
    "black and crimson streaks",
    "teal and blue balayage",
]

# ===== Face =====
FACE_SHAPES = [
    "oval face",
    "round face",
    "heart-shaped face",
    "diamond-shaped face",
    "square face",
    "long face",
    "triangle face",
]

EYE_SHAPES = [
    "almond eyes",
    "round eyes",
    "upturned eyes",
    "downturned eyes",
    "monolid eyes",
    "hooded eyes",
    "deep-set eyes",
    "wide-set eyes",
    "narrow eyes",
]

NOSE_SHAPES = [
    "straight nose",
    "button nose",
    "upturned nose",
    "aquiline nose",
    "roman nose",
    "petite nose",
    "snub nose",
]

LIP_SHAPES = [
    "full lips",
    "heart-shaped lips",
    "bow-shaped lips",
    "thin lips",
    "soft pout",
    "defined cupid's bow",
    "plush lips",
]

FACE_DETAILS = [
    "high cheekbones",
    "sculpted cheekbones",
    "soft jawline",
    "sharp jawline",
    "defined jawline",
    "delicate chin",
    "prominent dimples",
    "rounded cheeks",
    "hollowed cheeks",
    "freckled cheeks",
]

# ===== Stage 3 Accents =====
BODY_ACCENTS = [
    "statuesque posture",
    "graceful stance",
    "elegant silhouette",
    "lithe physique",
    "poised demeanor",
    "ballerina poise",
    "delicate presence",
]

SKIN_ACCENTS = [
    "radiant skin",
    "glowing complexion",
    "velvety skin",
    "soft luminous skin",
    "glossy skin sheen",
    "silky smooth skin",
]

FACE_ACCENTS = [
    "sparkling eyes",
    "radiant gaze",
    "piercing gaze",
    "delicate features",
    "defined cheek contour",
    "glowing blush",
    "refined facial structure",
]

HAIR_ACCENTS = [
    "glossy hair",
    "lustrous hair",
    "silky hair",
    "voluminous hair",
    "flowing hair",
    "polished hair",
    "shiny hair",
]

SENSUAL_ACCENTS = [
    "sultry aura",
    "sensuous allure",
    "smoldering gaze",
    "tempting presence",
]

# ===== Themes =====
THEMES = {
    "model": {
        "body": {
            "shapes": ["statuesque form", "slender frame", "toned dancer physique"],
            "details": ["defined waistline", "long elegant legs"],
        },
        "skin": {
            "tones": ["sun-kissed tan skin", "golden olive skin"],
            "features": ["luminous glow"],
        },
        "hair": {
            "lengths": ["waist-length", "mid-back length"],
            "textures": ["sleek straight", "smooth layers"],
            "styles": ["elegant updo", "loose flowing"],
            "bangs": ["middle part", "no bangs"],
            "colors": ["dark brown", "platinum blonde"],
            "mix": ["caramel and chestnut balayage"],
        },
        "face": {
            "shapes": ["oval face", "diamond-shaped face"],
            "eyes": ["almond eyes"],
            "nose": ["straight nose"],
            "lips": ["full lips", "defined cupid's bow"],
            "details": ["high cheekbones", "sculpted cheekbones", "defined jawline"],
        },
        "decor": {
            "body": ["statuesque posture"],
            "skin": ["radiant skin"],
            "face": ["defined cheek contour"],
            "hair": ["glossy hair"],
        },
    },
    "kawaii": {
        "body": {
            "shapes": ["petite frame", "softly rounded figure"],
            "details": ["delicate collarbones", "soft shoulders"],
        },
        "skin": {
            "tones": ["pale rosy skin"],
            "features": ["rosy cheeks", "soft blush", "delicate freckles"],
        },
        "hair": {
            "lengths": ["shoulder-length", "collarbone-length"],
            "textures": ["soft wavy", "gentle waves"],
            "styles": ["twin tails", "loose braid"],
            "bangs": ["soft fringe", "wispy bangs"],
            "colors": ["honey blonde", "rose pink"],
            "mix": ["peach and blonde gradient"],
        },
        "face": {
            "shapes": ["round face"],
            "eyes": ["round eyes", "upturned eyes"],
            "nose": ["button nose", "petite nose"],
            "lips": ["soft pout", "heart-shaped lips"],
            "details": ["rounded cheeks", "prominent dimples", "soft jawline"],
        },
        "decor": {
            "body": ["delicate presence"],
            "skin": ["glowing blush"],
            "face": ["sparkling eyes"],
            "hair": ["shiny hair"],
        },
    },
    "gothic": {
        "body": {
            "shapes": ["statuesque form", "slender frame"],
            "details": ["graceful neck", "delicate collarbones"],
        },
        "skin": {
            "tones": ["porcelain skin"],
            "features": ["beauty mark below eye", "matte porcelain finish"],
        },
        "hair": {
            "lengths": ["waist-length", "mid-back length"],
            "textures": ["sleek straight"],
            "styles": ["elegant updo", "loose flowing"],
            "bangs": ["curtain bangs", "middle part"],
            "colors": ["jet black", "blue-black"],
            "mix": ["black and crimson streaks"],
        },
        "face": {
            "shapes": ["oval face", "diamond-shaped face"],
            "eyes": ["deep-set eyes", "downturned eyes"],
            "nose": ["straight nose"],
            "lips": ["bow-shaped lips", "full lips"],
            "details": ["sharp jawline", "high cheekbones"],
        },
        "decor": {
            "body": ["elegant silhouette"],
            "skin": ["velvety skin"],
            "face": ["piercing gaze"],
            "hair": ["polished hair"],
        },
    },
    "wasou": {
        "body": {
            "shapes": ["delicate build", "graceful curves"],
            "details": ["graceful neck", "balletic posture"],
        },
        "skin": {
            "tones": ["porcelain skin", "fair neutral skin"],
            "features": ["soft blush"],
        },
        "hair": {
            "lengths": ["mid-back length"],
            "textures": ["sleek straight", "smooth layers"],
            "styles": ["elegant updo", "low ponytail"],
            "bangs": ["soft fringe", "curtain bangs"],
            "colors": ["jet black", "dark brown"],
            "mix": ["caramel and chestnut balayage"],
        },
        "face": {
            "shapes": ["oval face", "heart-shaped face"],
            "eyes": ["almond eyes"],
            "nose": ["straight nose"],
            "lips": ["soft pout"],
            "details": ["soft jawline", "delicate chin"],
        },
        "decor": {
            "body": ["poised demeanor"],
            "skin": ["silky smooth skin"],
            "face": ["delicate features"],
            "hair": ["polished hair"],
        },
    },
}

# ===== Exclusive Groups =====
EXCLUSIVE_GROUPS = {
    "body_shape": {
        "BODY_SHAPES": BODY_SHAPES,
    },
    "skin_tone": {
        "SKIN_TONES": SKIN_DETAILS["tones"],
    },
    "jawline": {
        "FACE_DETAILS": ["soft jawline", "sharp jawline", "defined jawline"],
    },
    "face_shape": {
        "FACE_SHAPES": FACE_SHAPES,
    },
    "eye_shape": {
        "EYE_SHAPES": EYE_SHAPES,
    },
    "nose_shape": {
        "NOSE_SHAPES": NOSE_SHAPES,
    },
    "lip_shape": {
        "LIP_SHAPES": LIP_SHAPES,
    },
    "cheek_volume": {
        "FACE_DETAILS": ["rounded cheeks", "hollowed cheeks"],
    },
    "hair_length": {
        "HAIR_LENGTHS": HAIR_LENGTHS,
    },
    "hair_color": {
        "HAIR_COLORS": HAIR_COLORS,
        "HAIR_COLOR_MIX": HAIR_COLOR_MIX,
    },
    "hair_part": {
        "HAIR_BANGS_PART": HAIR_BANGS_PART,
    },
}


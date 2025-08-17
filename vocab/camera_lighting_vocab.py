# vocab/camera_lighting_vocab.py
# 機材語を避けた安全語彙 + モード別強調
# 参考: camera_angle_vocab.py, cameraView.txt, bw_lighting.txt

# ---- 角度・ショット（共通ベース） ----
COMMON_ANGLES = [
    "eye-level view", "low angle", "high angle",
    "bird's-eye view", "worm's-eye view",
    "over-the-shoulder", "dutch angle", "tilt-shift view"
]

# モード別のショット語彙
PORTRAIT_SHOTS = [
    "headshot", "close-up", "bust shot", "medium close-up",
    "three-quarter shot", "intimate framing", "tight portrait"
]
LANDSCAPE_SHOTS = [
    "wide shot", "full shot", "panoramic view", "sweeping vista",
    "aerial view", "extreme long shot", "telephoto compression view", "long exposure view"
]

# ---- ライト表現（機材連想語を回避） ----
LIGHT_STYLES_SAFE = [
    "soft glow", "diffused light", "ambient glow", "gentle highlights",
    "dramatic contrast", "cinematic tone", "natural sunlight",
    "subtle specular glow", "flat, even light", "chiaroscuro mood",
    "high-contrast look", "dappled light pattern", "gradual light falloff",
    "motivated light feel"
]

LIGHT_DIRECTIONS_SAFE = [
    "glowing outline",        # rim/back の代替
    "side glow",              # side
    "edge glow",              # edge/kicker
    "top-down glow",          # top/overhead
    "uplight shadow",         # under/low-angle
    "silhouette emphasis",    # silhouette
    "cross-lit feel",         # cross lighting を機材抜きで
    "background glow accent"  # background light の代替
]

LIGHT_TIMES = [
    "golden hour glow", "sunset tones", "noon brightness",
    "dawn mist", "blue hour calm", "moonlit night"
]

LIGHT_COLORS = [
    "warm glow", "cool tint", "neon hues", "color-shifted tones"
]

# ---- 女性モード（官能寄り） ----
PORTRAIT_EROTIC_TONE_TIER1 = [
    "soft skin highlights", "silky glow on skin", "delicate body contours",
    "subtle collarbone sheen", "gentle shadow along curves", "whispered contrast",
    "moist glow on lips", "velvety midtones", "breathed warmth near the neck",
    "intimate close framing", "satin-like complexion", "faint backlit outline",
    "tender rim of light", "slow falloff on skin", "calm, sultry mood",
]

PORTRAIT_EROTIC_TONE_TIER2 = [
    "languid pose with lingering gaze", "dewy sheen tracing the waist",
    "shadow-kissed neckline", "fabric clinging to gentle curves",
    "translucent hints along the silhouette", "low, smoldering light on skin",
    "breath-warm highlights at the nape", "soft glow mapping the hips and waist",
    "suggestive shoulder line", "damp highlights over the collarbone",
    "glossed skin in shallow focus", "sensual close framing",
    "shaded hollows with velvet depth", "sinuous outline under diffused glow",
    "subtle tension in posture",
]

PORTRAIT_EROTIC_TONE_TIER3 = [
    "intense chiaroscuro across curves", "humid glow tracing every contour",
    "barely-there fabric pressed to the body", "slow, intimate falloff over the torso",
    "smoldering gaze framed in tight close-up", "slick sheen catching the light",
    "shadow-play accentuating arched posture", "liquid highlights on warm skin",
    "suggestive silhouette with deep tonal range", "rich specular glaze on curves",
    "heated air and breath-soft haze", "lingering close focus on delicate texture",
    "deep, sultry tonality around the waistline", "murmured warmth at the skin’s edge",
    "cinematic intimacy with restrained mystery",
]

PORTRAIT_EROTIC_TONE = list(dict.fromkeys(
    PORTRAIT_EROTIC_TONE_TIER1 + PORTRAIT_EROTIC_TONE_TIER2 + PORTRAIT_EROTIC_TONE_TIER3
))

# ---- 風景モード（雄大さ強調） ----
LANDSCAPE_GRANDEUR_TONE = [
    "vast scale", "monumental composition", "epic sense of space",
    "towering perspective", "layered depth cues", "sweeping horizons",
    "dramatic cloudscape", "crepuscular rays", "atmospheric haze",
    "glacial clarity", "tectonic ridge lines"
]

# ---- 禁止・置換マップ ----
BAN_REPLACE = {
    "softbox": "soft glow",
    "umbrella": "diffused light",
    "beauty dish": "gentle highlight",
    "ring light": "circular glow",
    "snoot": "focused glow",
    "gobo": "shaped highlight",
    "reflector": "bounced glow",
    "three-point": "balanced lighting feel",
    "four-point": "multi-directional glow",
    "key light": "primary glow",
    "fill light": "soft fill",
    "backlight": "glowing outline",
    "hair light": "subtle edge glow",
    "practical light": "in-scene glow",
}

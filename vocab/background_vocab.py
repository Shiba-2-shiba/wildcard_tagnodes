# vocab/background_vocab.py
# background_tag.py から語彙リストを分離

# ========================
# デフォルト語彙（編集しやすいように分類）
# ========================

# ── 環境（ENV）: 屋内/屋外 を分離
BG_ENV_INDOOR = [
    # ベース室内
    "bedroom interior", "boudoir set", "hotel suite", "vanity table scene", "draped curtains",
    "silk sheets", "velvet chaise lounge", "dressing room", "soft rug floor", "full-length mirror",
    "studio cyclorama", "minimalist photo studio", "loft apartment", "tatami room", "ryokan suite",
]

BG_ENV_OUTDOOR = [
    # ベース屋外
    "rooftop garden", "quiet back alley", "cobblestone street", "lantern-lit lane",
    "neon-soaked street", "seaside boardwalk", "forest clearing", "bamboo grove",
    "flower meadow", "desert overlook", "rain-soaked boulevard", "snowy sidewalk",
]

# ── 照明/ライティング
BG_LIGHT = [
    "soft warm lighting", "low-key lighting", "rim lighting", "backlit glow", "window daylight",
    "neon accent lights", "candlelight ambience", "spotlit highlight", "golden-hour light",
    "moonlit ambience", "film noir lighting", "stage spotlight", "colored gel lighting",
]

# ── ディテール（小物・雰囲気）
BG_DETAILS = [
    "scattered petals", "sheer curtains", "hanging beads", "string lights", "perfume bottles",
    "pearls on table", "folded lingerie", "wall shadows", "bokeh background",
    "foggy haze", "raindrops on glass", "steamy window", "floating dust motes",
    "paper lanterns", "shoji screens", "calligraphy scrolls", "tatami mats",
]

# ── テクスチャ（面の質感）
BG_TEXTURE = [
    "silky textures", "velvet textures", "sheer fabrics", "glossy reflections", "matte backdrop",
    "brushed metal", "weathered wood", "polished marble", "frosted glass", "grainy film texture",
]

# ── 天候 / 季節
BG_WEATHER = [
    "clear sky", "overcast sky", "drizzle", "heavy rain", "snowfall", "blizzard",
    "misty air", "morning fog", "thunderstorm", "sun shower", "wet pavement shine",
    "pollen breeze", "falling cherry blossoms", "autumn leaves",
]

# ── 時間帯
BG_TIME = [
    "sunrise", "morning light", "noon light", "golden hour", "twilight", "blue hour",
    "midnight", "pre-dawn darkness",
]

# ── 効果/演出（FX）
BG_FX = [
    "volumetric light rays", "light leaks", "lens flare", "neon glow", "cinematic haze",
    "soft vignette", "prismatic diffraction", "reflections on wet ground",
]

# ── 建築/構造（屋内外の差し色）
BG_ARCH = [
    "arched doorway", "bay window", "spiral staircase", "exposed brick wall",
    "industrial pipes", "open beam ceiling", "paper sliding doors", "stone torii gate",
    "retro phone booth", "vintage signboard", "ramen shop counter",
]

# ── 小道具/プロップ（背景寄り）
BG_PROPS = [
    "full-length mirror", "dresser with cosmetics", "folding screen", "kimono stand",
    "umbrella rack", "neon sign", "vintage jukebox", "plants in pots", "tea set on tray",
]

# ========================
# テーマパック
# ========================

THEME_PACKS = {
    "futuristic": {
        "env_indoor": [
            "sleek starship interior", "space station viewport", "holographic command room",
            "neon backroom with servers", "cybernetic clinic",
        ],
        "env_outdoor": [
            "futuristic metropolis", "cyberpunk street scene", "floating city in the clouds",
            "advanced spaceport", "maglev transit hub",
        ],
        "details": [
            "holographic billboards", "floating UI panels", "bioluminescent plants",
            "robotic attendants", "laser light show", "quantum terminals",
        ],
        "texture": ["brushed alloy", "carbon fiber", "glass panels"],
        "light": ["neon rim light", "holographic glow"],
        "arch": ["transparent skybridge", "luminescent pylons"],
    },
    "school": {
        "env_indoor": [
            "classroom with wooden desks", "sunlit library aisles", "music room with stands",
            "science lab benches", "art room with easels",
        ],
        "env_outdoor": [
            "school courtyard under cherry blossoms", "track field bleachers",
        ],
        "details": ["chalk dust in air", "posters on walls", "trophy cabinet", "bento lunch on desk"],
        "texture": ["scuffed linoleum", "polished gym floor"],
        "light": ["fluorescent classroom lighting"],
        "arch": ["corridor with lockers"],
    },
    "abstract": {
        "env_indoor": ["gradient color field", "geometric mosaic backdrop", "wavy stripe composition"],
        "env_outdoor": [],
        "details": ["watercolor splashes", "mandala gradients", "glitter accents"],
        "texture": ["grainy pastel", "soft gradient with ripples"],
        "light": ["even softbox light"],
    },
    "asian": {
        "env_indoor": ["tea house interior", "tatami and shoji room", "zen meditation hall"],
        "env_outdoor": ["zen garden with koi pond", "shinto shrine approach", "bamboo forest path", "lantern-lit night market", "torii gate by the sea"],
        "details": ["paper lanterns", "calligraphy tools", "kimono fabrics"],
        "texture": ["washi paper", "lacquer wood"],
        "light": ["warm lantern light"],
        "arch": ["stone lanterns", "red torii gateways"],
    },
    "bathtub": {
        "env_indoor": [
            "luxury bathroom with freestanding tub", "clawfoot bathtub by window",
            "sunken stone bath", "japanese soaking tub in hinoki room",
        ],
        "env_outdoor": [],
        "details": ["steamy mirrors", "water droplets on skin", "bubbles overflowing", "bath tray with candles", "towels neatly folded"],
        "texture": ["polished tile", "frosted glass"],
        "light": ["soft steamy lighting"],
        "arch": ["arched window by tub"],
    },
    "beautiful": {
        "env_indoor": ["conservatory with flowers"],
        "env_outdoor": ["cherry blossom park", "lavender field at dusk", "coastal cliff overlook", "romantic city skyline at night", "enchanted forest walkway"],
        "details": ["falling petals", "fireflies", "rainbow mist by waterfall"],
        "texture": ["soft bokeh", "silky water long-exposure"],
        "light": ["golden-hour backlight", "moonlit sparkle"],
    },
    "city_streets": {
        "env_indoor": ["subway concourse interior"],
        "env_outdoor": ["night market street", "rainy neon alley", "quiet cobblestone lane", "subway platform", "rooftop overlooking skyline"],
        "details": ["steaming manhole", "vibrant street art", "shop signboards", "puddles reflecting lights", "food stall steam"],
        "texture": ["weathered brick", "wet asphalt gloss"],
        "light": ["neon signage glow", "streetlamp pools of light"],
        "arch": ["overhead power lines", "narrow alley canopies"],
    },
    "fantasy": {
        "env_indoor": ["wizard tower study", "crystal conservatory"],
        "env_outdoor": ["floating islands in sky", "enchanted forest with glowing mushrooms", "crystal cavern", "moonlit meadow"],
        "details": ["magical runes", "floating motes of light", "arcane artifacts"],
        "texture": ["iridescent crystal", "mossy stone"],
        "light": ["ethereal moonlight", "bioluminescent glow"],
        "arch": ["ancient stone archways"],
    },
    "waterside": {
        "env_indoor": ["indoor pool with skylight", "onsen bath hall"],
        "env_outdoor": ["riverbank under willows", "lakeside pier", "seaside cliffs", "waterfall basin", "canal promenade"],
        "details": ["ripples on water", "wet stone", "floating lotus", "sea spray"],
        "texture": ["shimmering water surface", "algae-slick rock"],
        "light": ["reflected caustics light", "misty backlight"],
        "arch": ["arched canal bridge", "wooden pier"],
    },
    "city_night": {
        "env_indoor": ["high-rise lounge bar", "glass elevator lobby"],
        "env_outdoor": ["skyline overlook", "busy crosswalk", "elevated highway viewpoint", "riverfront lights"],
        "details": ["longtail light trails", "LED billboards", "taxi queues"],
        "texture": ["wet asphalt gloss", "mirror-like windows"],
        "light": ["neon glow", "sodium-vapor streetlights"],
        "arch": ["steel truss bridge", "observation deck"],
    },
    "countryside": {
        "env_indoor": ["farmhouse kitchen", "barn interior"],
        "env_outdoor": ["wheat field", "country road lined with trees", "vineyard terraces", "meadow with hay bales"],
        "details": ["fireflies at dusk", "hanging fairy lights", "wooden fence"],
        "texture": ["weathered wood", "sun-bleached grass"],
        "light": ["soft sunset haze"],
        "arch": ["stone well", "windmill silhouette"],
    },
    "wa_architecture": {
        "env_indoor": ["washitsu with tokonoma", "tea ceremony room", "engawa veranda"],
        "env_outdoor": ["castle keep courtyard", "temple approach", "old machiya street"],
        "details": ["ikebana display", "kakejiku scroll", "stone garden patterns"],
        "texture": ["tatami weave", "sukiya lattice wood"],
        "light": ["paper lantern glow"],
        "arch": ["kawara tiled roof", "shoji partitions", "karamon gate"],
    },
    "space": {
        "env_indoor": ["orbital habitat ring", "observatory dome", "cryogenic bay"],
        "env_outdoor": ["asteroid surface vista", "lunar outpost exterior", "planetary ring overlook"],
        "details": ["floating dust in zero-g", "constellation backdrop", "planet rise"],
        "texture": ["brushed alloy", "regolith dust"],
        "light": ["starlight rim", "blue planet glow"],
        "arch": ["airlock corridor", "transparent observation bubble"],
    },
    "western_architecture": {
        "env_indoor": ["baroque ballroom", "gothic cathedral nave", "renaissance gallery hall", "victorian parlor"],
        "env_outdoor": ["cobbled plaza", "colonnaded courtyard", "mediterranean terrace", "parisian boulevard"],
        "details": ["stained glass refractions", "marble busts", "wrought-iron balcony"],
        "texture": ["polished marble", "aged limestone"],
        "light": ["clerestory light beams"],
        "arch": ["flying buttresses", "corinthian columns", "ornate balustrade"],
    },
}

# UIで使うテーマの選択肢リスト
THEME_CHOICES = ["none"] + sorted(list(THEME_PACKS.keys()))

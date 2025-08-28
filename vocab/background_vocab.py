# vocab/background_vocab.py
# background_tag.py から語彙リストを分離し、魅力的で多様な語彙をさらに大幅に拡充

# ========================
# デフォルト語彙（編集しやすいように分類）
# ========================

# ── 環境（ENV）: 屋内/屋外 を分離
BG_ENV_INDOOR = [
    # 室内：住居、商業、スタジオ、公共施設など
    "sun-drenched bedroom interior", "cozy reading nook", "boudoir set with silk drapery", "luxurious hotel suite",
    "vanity table scene with scattered cosmetics", "draped curtains gently billowing", "soft rug floor with scattered pillows",
    "full-length mirror reflecting morning light", "minimalist photo studio", "industrial loft apartment with exposed brick",
    "traditional tatami room", "ryokan suite with a garden view", "rustic farmhouse kitchen", "antique study filled with books",
    "glass greenhouse interior", "sunroom with lush plants", "abandoned factory floor with broken machinery",
    "cozy cafe with warm lighting", "bustling restaurant kitchen", "dusty old bookstore aisle",
    "minimalist art gallery interior", "grand museum hall", "empty swimming pool with echoing acoustics",
    "corporate office cubicle", "empty theater stage with a single spotlight", "backstage dressing room with mirrors",
    "vintage movie theater with plush seats", "retro record shop interior", "high-rise lounge bar with a city view",
    "glass elevator lobby", "subway concourse interior with distant train sounds", "dimly lit bus terminal",
    "gothic cathedral nave", "baroque ballroom", "secret hidden library", "ancient temple interior",
    "steamy locker room", "artist's studio with paint splatters", "green-screen studio",
    "dimly lit basement workshop", "attic with dusty furniture", "forgotten attic space",
]

BG_ENV_OUTDOOR = [
    # 屋外：自然、都市、交通など
    "rooftop garden overlooking the city", "quiet back alley with cobblestones", "lantern-lit lane at dusk",
    "neon-soaked street at night", "seaside boardwalk at sunrise", "deep forest clearing with soft moss",
    "serene bamboo grove", "wildflower meadow at golden hour", "vast desert overlook at twilight",
    "rain-soaked boulevard with shimmering reflections", "snowy sidewalk with streetlights glowing",
    "serene park gazebo", "lush botanical garden path", "mystical waterfall basin",
    "tranquil riverbank under weeping willows", "old lakeside pier at dawn", "picturesque canal promenade",
    "rustic country road lined with old fences", "vineyard terraces on a sunny afternoon", "meadow with hay bales at sunset",
    "bustling urban street corner", "pedestrian overpass at night", "busy train station platform",
    "suburban backyard with a swing set", "childhood playground at dusk", "abandoned construction site",
    "car junkyard filled with rusty cars", "rural gas station", "highway rest stop at midnight",
    "city skyline at dusk with shimmering lights", "suburban street at night with glowing windows",
    "quiet beach at sunrise with gentle waves", "mystical forest with ancient trees",
    "snowy mountain pass", "frozen lake with misty air", "autumn forest with vibrant colors",
]

# ── 照明/ライティング
BG_LIGHT = [
    "soft warm lighting", "low-key dramatic lighting", "rim lighting", "backlit glow",
    "window daylight filtering through dust", "colorful neon accent lights", "flickering candlelight ambience",
    "spotlit highlight on a single object", "golden-hour light", "ethereal moonlit ambience",
    "cinematic film noir lighting", "harsh stage spotlight", "colored gel lighting",
    "overhead fluorescent light", "glowing monitor light on a face", "soft fireplace glow",
    "powerful searchlight beams", "strobe light effect", "blurry headlights in the rain",
    "streetlamp pools of light", "paper lantern glow", "sunlight filtering through leaves",
    "dusty light rays", "subtle glow from a device screen", "volumetric light rays",
]

# ── ディテール（小物・雰囲気）
BG_DETAILS = [
    "scattered rose petals", "sheer curtains blowing in a breeze", "hanging crystal beads",
    "string lights illuminating the darkness", "perfume bottles on a vanity table",
    "pearls scattered on a table", "folded lingerie on a bed", "long wall shadows",
    "beautiful bokeh background", "foggy haze", "raindrops on a glass window",
    "steamy window with water streaks", "floating dust motes in the air", "paper lanterns",
    "shoji screens", "calligraphy scrolls", "tatami mats on the floor", "coffee steam rising",
    "whiskey glass on a table", "worn books on a shelf", "dusty vinyl records",
    "scattered papers on a desk", "crumpled clothes on the floor", "potted plants in the foreground",
    "billowing smoke", "holographic projections in the air", "digital screen reflections",
    "cracked plaster wall", "graffiti on the wall", "dramatic high contrast shadows",
    "soft vignette effect", "prismatic diffraction", "rain-soaked reflections",
]

# ── テクスチャ（面の質感）
BG_TEXTURE = [
    "silky textures", "velvet textures", "sheer fabrics", "glossy reflections", "matte backdrop",
    "brushed metal", "weathered wood", "polished marble", "frosted glass", "grainy film texture",
    "cracked concrete", "rusted steel", "wet asphalt gloss", "smooth stone wall",
    "rough brick texture", "fluffy cotton", "burlap sack", "silk and satin", "distressed leather",
    "reflective chrome", "smooth plastic surface", "mossy cobblestone", "peeling paint",
    "iridescent shimmer", "smooth silk folds", "woven wicker", "bamboo texture",
]

# ── 天候 / 季節
BG_WEATHER = [
    "clear sky", "overcast sky", "light drizzle", "heavy rain", "gentle snowfall",
    "violent blizzard", "misty air", "thick morning fog", "thunderstorm with lightning",
    "sun shower", "wet pavement shine", "pollen breeze", "falling cherry blossoms",
    "vibrant autumn leaves", "windy day with swirling leaves", "calm before a storm",
    "hazy summer day", "chilly winter air", "blinding sunlight", "calm ocean with gentle waves",
]

# ── 時間帯
BG_TIME = [
    "sunrise", "morning light", "high noon light", "golden hour", "twilight",
    "blue hour", "deep midnight", "pre-dawn darkness", "late evening", "afternoon sun",
]

# ── 効果/演出（FX）
BG_FX = [
    "volumetric light rays", "light leaks", "lens flare", "dynamic neon glow", "cinematic haze",
    "soft vignette", "prismatic diffraction", "reflections on wet ground", "steam rising from a manhole",
    "rain droplets on glass", "snow flurry in the air", "fire sparks and embers",
    "magical particles floating", "glowing motes of dust", "lens distortion",
    "glitching effect on a screen", "smoke trails", "long exposure light trails",
    "chromatic aberration", "dynamic shadows", "light shafts",
]

# ── 建築/構造（屋内外の差し色）
BG_ARCH = [
    "arched doorway", "bay window", "spiral staircase", "exposed brick wall",
    "industrial pipes", "open beam ceiling", "paper sliding doors", "stone torii gate",
    "retro phone booth", "vintage signboard", "ramen shop counter", "concrete overpass",
    "rusted fire escape", "ornate iron fence", "graffiti-covered wall", "abandoned train car",
    "gothic spires", "baroque columns", "flying buttresses", "modern glass facade",
    "sloping tiled roof", "wrought-iron balcony", "ancient stone ruins", "ruined castle walls",
    "suspension bridge cables", "monumental arch", "old stone well", "wooden windmill",
]

# ── 小道具/プロップ（背景寄り）
BG_PROPS = [
    "old CRT monitor", "vintage jukebox", "stacked books on a table", "record player",
    "tea set on a tray", "scattered petals on the ground", "potted plants",
    "bicycle leaning against a wall", "empty soda cans", "abandoned shopping cart",
    "old vending machine", "wooden crates", "old street lamp", "mailbox by the road",
    "dirty garbage cans", "weathered park bench", "swing set", "broken swings",
    "colorful kites in the sky", "laundry on a clothesline", "forgotten tricycle",
]

# ========================
# テーマパック
# ========================

THEME_PACKS = {
    "futuristic": {
        "env_indoor": [
            "sleek starship interior", "space station viewport", "holographic command room",
            "neon backroom with servers", "cybernetic clinic", "hi-tech laboratory",
            "futuristic shopping mall atrium", "subway tunnel with maglev trains",
            "glowing data center", "zero-gravity lounge", "cybernetic control room",
        ],
        "env_outdoor": [
            "futuristic metropolis", "cyberpunk street scene", "floating city in the clouds",
            "advanced spaceport", "maglev transit hub", "off-world colony", "lunar base exterior",
            "alien cityscape with glowing spires", "high-speed skyway", "holographic sky billboards",
            "neon-drenched alleyway", "holographic garden", "dystopian cityscape",
        ],
        "details": [
            "holographic billboards", "floating UI panels", "bioluminescent plants",
            "robotic attendants", "laser light show", "quantum terminals", "digital rain effect",
            "bio-mechanical implants", "cybernetic wires", "data streams in the air",
            "flying cars", "glowing synth-wave patterns", "transparent touchscreens",
        ],
        "texture": ["brushed alloy", "carbon fiber", "glass panels", "iridescent materials", "chrome plating", "glowing circuit patterns"],
        "light": ["neon rim light", "holographic glow", "fluorescent strip light", "bio-luminescent light"],
        "arch": ["transparent skybridge", "luminescent pylons", "data spine towers", "sleek modular buildings", "floating platforms"],
        "props": ["hovering drone", "floating robot companion", "plasma weapon rack"],
    },
    "school": {
        "env_indoor": [
            "classroom with wooden desks", "sunlit library aisles", "music room with stands",
            "science lab benches", "art room with easels", "school gymnasium", "school cafeteria",
            "auditorium stage", "empty hallway with lockers", "principal's office",
            "chemistry lab with bubbling beakers", "band room with scattered instruments",
        ],
        "env_outdoor": [
            "school courtyard under cherry blossoms", "track field bleachers", "school gate",
            "school rooftop", "fountain in the main courtyard", "sports field on a sunny day",
            "basketball court at sunset", "schoolyard with colorful markings", "bus stop in front of the school",
        ],
        "details": [
            "chalk dust in air", "posters on walls", "trophy cabinet", "bento lunch on desk",
            "scattered textbooks", "school bags on the floor", "pencils on a desk",
            "paper airplane flying", "school bulletin board", "backpacks hanging on hooks",
            "open book on a desk", "stack of old tests",
        ],
        "texture": ["scuffed linoleum", "polished gym floor", "worn wooden desks", "graffiti on locker doors"],
        "light": ["fluorescent classroom lighting", "sunlight through large windows", "gymnasium spotlights"],
        "arch": ["corridor with lockers", "brick facade", "school bell tower", "archway leading to courtyard"],
        "props": ["school desk and chair", "blackboard and chalk", "basketball hoop", "trophy case"],
    },
    "abstract": {
        "env_indoor": [
            "gradient color field", "geometric mosaic backdrop", "wavy stripe composition",
            "liquid metal surface", "shattered glass shards", "cloudy smoke in a void",
            "op art patterns", "infinite reflective surfaces",
            "liquid acrylic flow", "digital static noise field", "polygonal crystal formation",
        ],
        "env_outdoor": [],
        "details": [
            "watercolor splashes", "mandala gradients", "glitter accents", "floating shapes",
            "particles in the air", "light refracting through crystal", "soft bokeh light spots",
            "smoky swirls", "glowing lines", "shimmering particles",
        ],
        "texture": [
            "grainy pastel", "soft gradient with ripples", "smudged watercolor", "fractal patterns",
            "iridescent shimmer", "smooth silk folds",
        ],
        "light": ["even softbox light", "soft glow from behind", "spotlight on object", "multi-colored light"],
    },
    "asian": {
        "env_indoor": [
            "tea house interior", "tatami and shoji room", "zen meditation hall", "traditional Japanese inn room",
            "bamboo tea house", "ancient temple interior", "samurai clan hall", "lantern-lit hallway",
            "old dojo with wooden floor", "traditional calligraphy studio", "tea ceremony room with a view",
        ],
        "env_outdoor": [
            "zen garden with koi pond", "shinto shrine approach", "bamboo forest path", "lantern-lit night market",
            "torii gate by the sea", "pagoda rooftop", "old city street with traditional buildings",
            "floating village on a lake", "terraced rice paddies", "mountain temple", "rock garden",
            "cherry blossom festival", "rainy night in Tokyo",
        ],
        "details": [
            "paper lanterns", "calligraphy tools", "kimono fabrics", "falling cherry blossoms",
            "sakura petals floating on water", "incense smoke", "buddha statue", "koi fish swimming",
            "bamboo stalks", "bonsai tree on a table", "teahouse steam", "geisha parasol",
        ],
        "texture": ["washi paper", "lacquer wood", "tatami weave", "bamboo texture", "mossy stone"],
        "light": ["warm lantern light", "candlelight", "sunlight through shoji screen", "golden light on temple roof"],
        "arch": ["stone lanterns", "red torii gateways", "kawara tiled roof", "shoji partitions", "karamon gate", "pagoda spire"],
        "props": ["tea set on a tray", "kimono stand", "folding screen", "bamboo fountain"],
    },
    "bathtub": {
        "env_indoor": [
            "luxury bathroom with freestanding tub", "clawfoot bathtub by window",
            "sunken stone bath", "japanese soaking tub in hinoki room", "vintage tiled bathroom",
            "modern minimalist bathroom", "spa-like stone bath", "bathtub filled with rose petals",
            "candlelit bathroom",
        ],
        "env_outdoor": [],
        "details": [
            "steamy mirrors", "water droplets on skin", "bubbles overflowing", "bath tray with candles",
            "towels neatly folded", "floating rose petals", "floating bubbles", "soap foam",
        ],
        "texture": ["polished tile", "frosted glass", "wet marble floor", "smooth ceramic"],
        "light": ["soft steamy lighting", "window daylight", "candle glow", "dim light"],
    },
    "beautiful": {
        "env_indoor": [
            "conservatory with flowers", "ornate ballroom", "crystal conservatory", "grand library with skylight",
            "glowing hall of mirrors", "celestial observatory interior", "opulent opera house interior",
        ],
        "env_outdoor": [
            "cherry blossom park", "lavender field at dusk", "coastal cliff overlook", "romantic city skyline at night",
            "enchanted forest walkway", "starry night sky over a lake", "field of sunflowers",
            "autumn forest path", "snow-covered mountain vista", "seaside at golden hour",
            "wildflower meadow at sunrise", "rainbow waterfall", "field of fireflies",
        ],
        "details": [
            "falling petals", "fireflies", "rainbow mist by waterfall", "glittering dust motes",
            "sparkling water", "delicate spiderwebs with dew", "dancing butterflies",
        ],
        "texture": ["soft bokeh", "silky water long-exposure", "smooth polished surface", "delicate fabric"],
        "light": ["golden-hour backlight", "moonlit sparkle", "ethereal glow", "sunbeams filtering through trees"],
    },
    "city_streets": {
        "env_indoor": [
            "subway concourse interior", "bus station waiting area", "vintage diner interior",
            "small convenience store interior", "street-level cafe",
        ],
        "env_outdoor": [
            "night market street", "rainy neon alley", "quiet cobblestone lane", "subway platform",
            "rooftop overlooking skyline", "busy crosswalk", "elevated highway viewpoint",
            "sidewalk with street vendors", "busy traffic intersection", "pedestrian shopping street",
            "old town alleyway", "rainy alley with reflections", "steaming manhole in the street",
        ],
        "details": [
            "steaming manhole", "vibrant street art", "shop signboards", "puddles reflecting lights",
            "food stall steam", "longtail light trails", "LED billboards", "graffiti on walls",
            "passersby in a blur", "scattered trash on the sidewalk",
        ],
        "texture": ["weathered brick", "wet asphalt gloss", "rusted metal", "peeling paint"],
        "light": ["neon signage glow", "streetlamp pools of light", "headlights of passing cars", "dull city light"],
        "arch": [
            "overhead power lines", "narrow alley canopies", "steel truss bridge", "concrete overpass",
            "old retro phone booth", "vintage signboard", "ramen shop counter", "rusted fire escape",
            "arched cobblestone alleyway",
        ],
        "props": [
            "street vendor cart", "stacked cardboard boxes", "vending machine", "old street lamp",
            "park bench", "garbage cans", "bicycle leaning against a wall",
        ],
    },
    "city_night": {
        "env_indoor": ["high-rise lounge bar", "glass elevator lobby", "night club interior", "movie theater lobby"],
        "env_outdoor": [
            "skyline overlook", "busy crosswalk", "elevated highway viewpoint", "riverfront lights",
            "neon alley", "rooftop garden at night", "quiet city park after dark",
        ],
        "details": [
            "longtail light trails", "LED billboards", "taxi queues", "reflections on wet ground",
            "vibrant light reflections", "city glow in the clouds", "distant skyscraper lights",
        ],
        "texture": ["wet asphalt gloss", "mirror-like windows", "dark concrete", "reflective puddles"],
        "light": ["neon glow", "sodium-vapor streetlights", "car headlights and taillights", "city lights reflections"],
        "arch": ["steel truss bridge", "observation deck", "high-rise facade", "glowing futuristic tower"],
    },
    "countryside": {
        "env_indoor": ["farmhouse kitchen", "barn interior", "rustic cottage living room", "old wooden cabin"],
        "env_outdoor": [
            "wheat field", "country road lined with trees", "vineyard terraces", "meadow with hay bales",
            "rolling hills at sunset", "peaceful village street", "mountain valley", "calm lake at dawn",
        ],
        "details": [
            "fireflies at dusk", "hanging fairy lights", "wooden fence", "farm animals grazing",
            "wildflowers in a field", "old wooden water well", "stone wall covered in ivy",
        ],
        "texture": ["weathered wood", "sun-bleached grass", "rough stone", "dried hay"],
        "light": ["soft sunset haze", "gentle morning light", "moonlight over fields"],
        "arch": ["stone well", "windmill silhouette", "wooden cottage", "farmhouse barn"],
        "props": ["hay bales", "rusty tractor", "old wooden cart", "scarecrow"],
    },
    "wa_architecture": {
        "env_indoor": [
            "washitsu with tokonoma", "tea ceremony room", "engawa veranda", "traditional Japanese inn room",
            "ancient temple interior", "samurai clan hall", "lantern-lit hallway",
        ],
        "env_outdoor": [
            "zen garden with koi pond", "shinto shrine approach", "bamboo forest path", "lantern-lit night market",
            "torii gate by the sea", "castle keep courtyard", "temple approach", "old machiya street",
            "traditional Japanese garden", "pagoda rooftop", "terraced rice paddies", "mountain temple",
        ],
        "details": [
            "paper lanterns", "calligraphy tools", "kimono fabrics", "falling cherry blossoms",
            "sakura petals floating on water", "incense smoke", "buddha statue", "koi fish swimming",
            "bamboo stalks", "bonsai tree on a table", "teahouse steam", "geisha parasol",
        ],
        "texture": ["washi paper", "lacquer wood", "tatami weave", "bamboo texture", "mossy stone"],
        "light": ["warm lantern light", "candlelight", "sunlight through shoji screen", "golden light on temple roof"],
        "arch": ["stone lanterns", "red torii gateways", "kawara tiled roof", "shoji partitions", "karamon gate", "pagoda spire"],
        "props": ["tea set on a tray", "kimono stand", "folding screen", "bamboo fountain"],
    },
    "fantasy": {
        "env_indoor": [
            "wizard tower study", "crystal conservatory", "ancient library", "dragon's hoard cavern",
            "throne room of a castle", "alchemist's laboratory", "enchanted forest cottage",
        ],
        "env_outdoor": [
            "floating islands in sky", "enchanted forest with glowing mushrooms", "crystal cavern",
            "moonlit meadow", "fairy ring in a forest", "ancient ruins on a misty hill",
            "dragon's peak with lava flow", "castle courtyard", "mystical waterfall",
        ],
        "details": [
            "magical runes", "floating motes of light", "arcane artifacts", "glowing mushrooms",
            "magical glowing flora", "glowing crystals", "fairy dust in the air",
        ],
        "texture": ["iridescent crystal", "mossy stone", "ancient runes on rock", "dragon scales"],
        "light": ["ethereal moonlight", "bioluminescent glow", "arcane glow", "glowing crystals"],
        "arch": ["ancient stone archways", "spires of a wizard's tower", "crystal formations", "ruined castle walls"],
        "props": ["glowing orb", "spellbook on a pedestal", "magical scepter", "treasure chest"],
    },
}

# UIで使うテーマの選択肢リスト
THEME_CHOICES = ["none"] + sorted(list(THEME_PACKS.keys()))


# ========================
# 排他的な語彙グループ
# ========================
# 複数のグループに属する語彙は、単一のグループからのみ抽選されるようにする
# 例：日中の照明と夜間の照明は同時に選ばれないようにする
EXCLUSIVE_TAG_GROUPS = {
    "light_type": [
        # 昼間の照明
        ["window daylight filtering through dust", "golden-hour light", "sunlight filtering through leaves", "high noon light", "blinding sunlight"],
        # 夜間の照明
        ["flickering candlelight ambience", "ethereal moonlit ambience", "cinematic film noir lighting", "glowing monitor light on a face", "neon-soaked street at night", "neon signage glow"],
        # 屋外照明
        ["streetlamp pools of light", "powerful searchlight beams", "blurry headlights in the rain", "car headlights and taillights"],
    ],
    "weather_condition": [
        # 晴れ/乾燥した天候
        ["clear sky", "pollen breeze"],
        # 雨天/濡れた天候
        ["light drizzle", "heavy rain", "sun shower", "rain-soaked boulevard with shimmering reflections", "raindrops on a glass window", "wet pavement shine", "rain-soaked reflections"],
        # 雪天
        ["gentle snowfall", "violent blizzard", "snowy sidewalk with streetlights glowing"],
        # 霧/霞
        ["misty air", "thick morning fog", "hazy summer day"],
    ],
    "time_of_day": [
        # 朝/昼
        ["sunrise", "morning light", "high noon light", "golden hour", "afternoon sun"],
        # 夕方/夜
        ["twilight", "blue hour", "deep midnight", "pre-dawn darkness", "late evening"],
    ],
    "environmental_effects": [
        # 自然由来の光効果
        ["volumetric light rays", "dusty light rays", "sunbeams filtering through trees", "light shafts"],
        # 人工的な効果
        ["light leaks", "lens flare", "strobe light effect", "glitching effect on a screen"],
    ]
}

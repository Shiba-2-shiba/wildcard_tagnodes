# background_vocab.py
# 語彙を大幅に拡充し、テーマパックを屋内/屋外の構造に完全対応させた完成版

# ========================
# デフォルト語彙（拡充・再分類済み）
# ========================

# --- 環境 (ENV) ---
BG_ENV_INDOOR = [
    "sun-drenched bedroom interior", "cozy reading nook", "boudoir set with silk drapery", "luxurious hotel suite",
    "vanity table scene with scattered cosmetics", "minimalist photo studio", "industrial loft apartment with exposed brick",
    "traditional tatami room", "ryokan suite with a garden view", "rustic farmhouse kitchen", "antique study filled with books",
    "glass greenhouse interior", "sunroom with lush plants", "abandoned factory floor", "cozy cafe with warm lighting",
    "bustling restaurant kitchen", "dusty old bookstore aisle", "minimalist art gallery interior", "grand museum hall",
    "empty swimming pool", "corporate office cubicle", "empty theater stage with a single spotlight", "backstage dressing room",
    "vintage movie theater", "retro record shop interior", "high-rise lounge bar with a city view", "glass elevator lobby",
    "subway concourse interior", "dimly lit bus terminal", "gothic cathedral nave", "baroque ballroom", "secret hidden library",
    "ancient temple interior", "steamy locker room", "artist's studio with paint splatters", "green-screen studio", "dimly lit basement workshop",
    "opulent opera house", "grand library with skylight", "wizard's tower study", "alchemist's laboratory", "throne room of a castle"
]
BG_ENV_OUTDOOR = [
    "rooftop garden overlooking the city", "quiet back alley with cobblestones", "lantern-lit lane at dusk",
    "neon-soaked street at night", "seaside boardwalk at sunrise", "deep forest clearing with soft moss", "serene bamboo grove",
    "wildflower meadow at golden hour", "vast desert overlook at twilight", "rain-soaked boulevard", "snowy sidewalk",
    "serene park gazebo", "lush botanical garden path", "mystical waterfall basin", "tranquil riverbank",
    "old lakeside pier at dawn", "picturesque canal promenade", "rustic country road", "vineyard terraces",
    "meadow with hay bales at sunset", "bustling urban street corner", "pedestrian overpass at night", "busy train station platform",
    "suburban backyard with a swing set", "childhood playground at dusk", "abandoned construction site", "car junkyard", "rural gas station",
    "highway rest stop at midnight", "city skyline at dusk", "suburban street at night", "quiet beach at sunrise",
    "mystical forest with ancient trees", "snowy mountain pass", "frozen lake", "autumn forest with vibrant colors",
    "misty graveyard at midnight", "enchanted forest with glowing mushrooms", "floating islands in the sky", "castle courtyard"
]

# --- ディテール (DETAILS) ---
BG_DETAILS_INDOOR = [
    "scattered rose petals", "sheer curtains blowing in a breeze", "hanging crystal beads", "string lights illuminating the darkness",
    "perfume bottles on a vanity table", "pearls scattered on a table", "folded lingerie on a bed", "long wall shadows",
    "floating dust motes in sunbeam", "shoji screens", "calligraphy scrolls", "tatami mats on the floor",
    "coffee steam rising", "whiskey glass on a table with melting ice", "worn books on a shelf", "dusty vinyl records", "scattered playing cards",
    "crumpled clothes on the floor", "potted plants in the foreground", "billowing smoke from an incense stick", "cracked plaster wall",
    "steamy mirror with water streaks", "flickering fireplace", "ornate rug on wooden floor", "grandfather clock ticking"
]
BG_DETAILS_OUTDOOR = [
    "raindrops on a glass window", "puddles reflecting neon lights", "steaming manhole cover", "falling cherry blossom petals",
    "vibrant autumn leaves swirling in the wind", "paper lanterns glowing warmly", "graffiti on a brick wall", "rain-soaked reflections",
    "fireflies glowing at dusk", "pigeons taking flight from a square", "wet leaves clinging to pavement", "distant heat haze shimmering",
    "dewdrops on a spiderweb", "dandelion seeds drifting in the air"
]

# --- 建築/構造 (ARCH) ---
BG_ARCH_INDOOR = [
    "arched doorway", "bay window with a cushioned seat", "spiral staircase", "exposed brick wall", "industrial pipes overhead",
    "open beam ceiling", "paper sliding doors (shoji)", "baroque columns", "stained glass window", "vaulted ceiling",
    "hidden passageway behind a bookshelf", "ornate fireplace", "library stacks stretching to the ceiling", "grand staircase"
]
BG_ARCH_OUTDOOR = [
    "stone torii gate", "retro phone booth", "vintage signboard", "ramen shop counter open to the street", "concrete overpass",
    "rusted fire escape", "ornate iron fence", "abandoned train car on overgrown tracks", "gothic spires against the sky",
    "flying buttresses of a cathedral", "modern glass facade reflecting the sky", "sloping tiled roof (kawara)", "wrought-iron balcony",
    "ancient stone ruins", "ruined castle walls", "suspension bridge cables at night", "monumental arch", "old stone well", "wooden windmill"
]

# --- 小道具 (PROPS) ---
BG_PROPS_INDOOR = [
    "old CRT monitor displaying static", "vintage jukebox", "stacked books on a table", "record player spinning silently", "tea set on a lacquered tray",
    "potted bonsai tree", "candlestick with dripping wax", "crystal ball on a stand", "antique globe", "manual typewriter",
    "artist's easel with an unfinished painting", "birdcage, empty", "go board with stones"
]
BG_PROPS_OUTDOOR = [
    "bicycle leaning against a wall", "empty soda cans rolling on the ground", "abandoned shopping cart", "old vending machine humming",
    "wooden crates stacked in an alley", "old street lamp casting a pool of light", "mailbox by the road", "dirty garbage cans",
    "weathered park bench", "swing set moving gently in the breeze", "broken swings", "colorful kites tangled in a tree",
    "laundry on a clothesline", "forgotten tricycle", "street food stall", "newspaper stand", "fire hydrant", "bird bath", "wind chime"
]

# --- 共通カテゴリ (分割不要) ---
BG_LIGHT = [
    "soft warm lighting", "low-key dramatic lighting", "rim lighting", "backlit glow", "window daylight filtering through dust",
    "colorful neon accent lights", "flickering candlelight ambience", "spotlit highlight", "golden-hour light",
    "ethereal moonlit ambience", "cinematic film noir lighting", "harsh stage spotlight", "colored gel lighting",
    "overhead fluorescent light", "glowing monitor light on a face", "soft fireplace glow", "powerful searchlight beams",
    "strobe light effect", "blurry headlights in the rain", "streetlamp pools of light", "paper lantern glow",
    "sunlight filtering through leaves (komorebi)", "dusty light rays", "subtle glow from a device screen", "volumetric light rays"
]
BG_TEXTURE = [
    "silky textures", "velvet textures", "sheer fabrics", "glossy reflections", "matte backdrop", "brushed metal",
    "weathered wood", "polished marble", "frosted glass", "grainy film texture", "cracked concrete", "rusted steel",
    "wet asphalt gloss", "smooth stone wall", "rough brick texture", "fluffy cotton", "burlap sack", "silk and satin",
    "distressed leather", "reflective chrome", "smooth plastic surface", "mossy cobblestone", "peeling paint",
    "iridescent shimmer", "smooth silk folds", "woven wicker", "bamboo texture", "tarnished brass", "holographic surface"
]
BG_WEATHER = [
    "clear sky", "overcast sky", "light drizzle", "heavy rain", "gentle snowfall", "violent blizzard", "misty air",
    "thick morning fog", "thunderstorm with lightning", "sun shower", "wet pavement shine", "pollen breeze",
    "calm before a storm", "hazy summer day", "chilly winter air", "blinding sunlight", "calm ocean with gentle waves"
]
BG_TIME = [
    "sunrise", "morning light", "high noon light", "golden hour", "twilight", "blue hour", "deep midnight",
    "pre-dawn darkness", "late evening", "afternoon sun"
]
BG_FX = [
    "volumetric light rays", "light leaks", "lens flare", "dynamic neon glow", "cinematic haze", "soft vignette",
    "prismatic diffraction", "reflections on wet ground", "steam rising from a manhole", "rain droplets on glass",
    "snow flurry in the air", "fire sparks and embers", "magical particles floating", "glowing motes of dust",
    "lens distortion", "glitching effect on a screen", "smoke trails", "long exposure light trails", "chromatic aberration",
    "dynamic shadows", "light shafts", "beautiful bokeh background", "foggy haze"
]

# ========================
# テーマパック (構造更新・拡充済み)
# ========================
THEME_PACKS = {
    "cyberpunk_futuristic": {
        "env_indoor": ["sleek starship interior", "space station viewport", "holographic command room", "cybernetic clinic", "hi-tech laboratory", "glowing data center", "grimy noodle bar", "back-alley cybernetics clinic"],
        "env_outdoor": ["futuristic metropolis", "cyberpunk street scene", "floating city in the clouds", "maglev transit hub", "off-world colony", "dystopian cityscape", "acid rain-slicked streets", "mega-corporation ziggurat"],
        "details_indoor": ["floating UI panels", "robotic attendants", "cybernetic wires", "data streams in the air", "glitching computer screens"],
        "details_outdoor": ["holographic billboards", "flying cars (spinners)", "glowing synth-wave patterns", "holographic koi fish swimming in the air", "glitching neon signs"],
        "texture": ["brushed alloy", "carbon fiber", "glass panels", "iridescent materials", "chrome plating", "glowing circuit patterns", "wet asphalt"],
        "light": ["neon rim light", "holographic glow", "fluorescent strip light", "lens flare from flying vehicle"],
        "arch_indoor": ["transparent skybridge", "sleek modular buildings"],
        "arch_outdoor": ["luminescent pylons", "data spine towers", "floating platforms", "endless skyscrapers"],
        "props_indoor": ["hovering drone", "floating robot companion", "plasma weapon rack", "datajack terminal"],
        "props_outdoor": ["automated food stall", "armored police vehicle"],
    },
    "school": {
        "env_indoor": ["classroom with wooden desks", "sunlit library aisles", "science lab benches", "school gymnasium", "school cafeteria", "empty hallway with lockers", "music room", "art room"],
        "env_outdoor": ["school courtyard under cherry blossoms", "track field bleachers", "school gate", "school rooftop", "basketball court at sunset", "swimming pool for lessons"],
        "details_indoor": ["chalk dust in air", "posters on walls", "trophy cabinet", "bento lunch on desk", "scattered textbooks", "backpacks hanging on hooks", "sunlight filtering through classroom window"],
        "details_outdoor": ["paper airplane flying", "school bulletin board", "sound of a school bell", "students walking home"],
        "texture": ["scuffed linoleum", "polished gym floor", "worn wooden desks", "graffiti on locker doors"],
        "light": ["fluorescent classroom lighting", "sunlight through large windows", "late afternoon sun on the field"],
        "arch_indoor": ["corridor with lockers", "stairwell with afternoon light"],
        "arch_outdoor": ["brick facade", "school bell tower", "chain-link fence around sports field"],
        "props_indoor": ["school desk and chair", "blackboard and chalk", "anatomical model", "piano"],
        "props_outdoor": ["basketball hoop", "soccer goal", "bicycle parking area"],
    },
    "fantasy": {
        "env_indoor": ["wizard tower study", "crystal conservatory", "ancient library", "dragon's hoard cavern", "throne room of a castle", "alchemist's laboratory", "enchanted forest cottage", "elven hall", "dwarven forge"],
        "env_outdoor": ["floating islands in sky", "enchanted forest with glowing mushrooms", "crystal cavern", "moonlit meadow", "fairy ring in a forest", "ancient ruins on a misty hill", "dragon's peak with lava flow"],
        "details_indoor": ["magical runes glowing on walls", "floating motes of light", "arcane artifacts on shelves", "potion bottles bubbling"],
        "details_outdoor": ["magical glowing flora", "glowing crystals", "fairy dust in the air", "a distant dragon in the sky"],
        "texture": ["iridescent crystal", "mossy stone", "ancient runes on rock", "dragon scales", "mithril silver"],
        "light": ["ethereal moonlight", "bioluminescent glow", "arcane glow from a spell", "light from glowing crystals"],
        "arch_indoor": ["ancient stone archways", "spires of a wizard's tower", "crystal formations"],
        "arch_outdoor": ["ruined castle walls", "elven tree-houses", "bridge made of light"],
        "props_indoor": ["glowing orb", "spellbook on a pedestal", "magical scepter", "treasure chest"],
        "props_outdoor": ["ancient monolith", "glowing sword stuck in a stone"],
    },
    "gothic_horror": {
        "env_indoor": ["haunted mansion hallway", "dusty gothic library", "crypt interior", "abandoned chapel", "laboratory of a mad scientist"],
        "env_outdoor": ["misty graveyard at midnight", "crumbling abbey ruins", "dark forest with twisted trees", "lonely cliffside castle"],
        "details_indoor": ["flickering candelabras", "cobwebs in corners", "ornate silver mirror with no reflection", "bloodstains on the floor", "portraits with watching eyes"],
        "details_outdoor": ["bats flying against the full moon", "thick fog on the ground", "sound of a lone wolf howling", "lightning illuminating the scene"],
        "texture": ["aged stone", "tattered velvet", "cold iron bars", "rotting wood", "dusty surfaces"],
        "light": ["dim candlelight", "pale moonlight filtering through grimy windows", "lightning flashes", "single oil lamp"],
        "arch_indoor": ["pointed arches", "stone spiral staircase", "gargoyles looking down"],
        "arch_outdoor": ["flying buttresses", "cemetery gates", "crypt entrance"],
        "props_indoor": ["antique grandfather clock stopped at midnight", "skull on a book", "organ with dusty keys", "surgical tools on a tray"],
        "props_outdoor": ["weathered tombstones", "empty coffin", "crow perched on a branch"],
    },
}

# UIで使うテーマの選択肢リスト
THEME_CHOICES = ["none", "おまかせ"] + sorted(list(THEME_PACKS.keys()))

# ========================
# 排他的な語彙グループ (変更なし)
# ========================
EXCLUSIVE_TAG_GROUPS = {
    "light_type": [
        ["window daylight filtering through dust", "golden-hour light", "sunlight filtering through leaves (komorebi)", "high noon light", "blinding sunlight"],
        ["flickering candlelight ambience", "ethereal moonlit ambience", "cinematic film noir lighting", "glowing monitor light on a face", "neon-soaked street at night", "neon signage glow"],
        ["streetlamp pools of light", "powerful searchlight beams", "blurry headlights in the rain", "car headlights and taillights"],
    ],
    "weather_condition": [
        ["clear sky", "pollen breeze"],
        ["light drizzle", "heavy rain", "sun shower", "rain-soaked boulevard", "raindrops on a glass window", "wet pavement shine", "rain-soaked reflections"],
        ["gentle snowfall", "violent blizzard", "snowy sidewalk"],
        ["misty air", "thick morning fog", "hazy summer day"],
    ],
    "time_of_day": [
        ["sunrise", "morning light", "high noon light", "golden hour", "afternoon sun"],
        ["twilight", "blue hour", "deep midnight", "pre-dawn darkness", "late evening"],
    ],
    "environmental_effects": [
        ["volumetric light rays", "dusty light rays", "sunbeams filtering through trees", "light shafts"],
        ["light leaks", "lens flare", "strobe light effect", "glitching effect on a screen"],
    ]
}


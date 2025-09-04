# background_vocab.py
# 語彙を大幅に拡充し、テーマパックを屋内/屋外の構造に完全対応させた完成版
# New themes added: solapunk_art_nouveau, tropical_resort, cozy_academia

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
    "opulent opera house", "grand library with skylight", "wizard's tower study", "alchemist's laboratory", "throne room of a castle",
    # New additions
    "spaceship cockpit with a view of stars", "gleaming biodome interior", "stellar observatory dome", "engine room with glowing conduits",
    "hydroponics bay with alien plants", "sunlit conservatory", "spacious artist's loft", "abandoned subway station",
    "bustling indoor marketplace", "grand hotel lobby", "underground cavern temple", "scribe's scriptorium with scrolls",
    "ornate palace hall"
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
    "misty graveyard at midnight", "enchanted forest with glowing mushrooms", "floating islands in the sky", "castle courtyard",
    # New additions
    "majestic canyon overlook", "rim of a volcanic crater", "active geyser field", "shimmering salt flats",
    "ancient glacier field", "glowing crystal forest", "alien jungle with exotic flora", "derelict spaceship graveyard in a desert",
    "bustling city plaza with fountains", "picturesque canal city", "terraced rice paddies on a mountainside",
    "ancient amphitheater ruins", "sprawling vineyard on a hillside", "a lone lighthouse on a cliff"
]

# --- ディテール (DETAILS) ---
# --- ディテール (生成指示カテゴリ) ---
BG_DETAILS_INDOOR_GENERATIVE = [
    "a delicate detail **highlighted by a soft light**",
    "the **interplay of light and shadow** creating intricate patterns on surfaces",
    "a subtle imperfection that adds a touch of **realism and charm**",
    "**reflections on a polished surface** that add depth and complexity",
    "elegant signs of **aging and history**, like patina or worn velvet",
    "subtle hints of the atmosphere, like **rising steam or condensation**",
    "a single, **eye-catching detail** that serves as a focal point",
    "a subtle imperfection that adds realism"
]
BG_DETAILS_OUTDOOR_GENERATIVE = [
    "the way **sunlight filters through leaves or clouds**, creating dappled light",
    "the **texture of the ground** revealed by raking light (e.g., wet cobblestones, dry cracked earth)",
    "a small detail that hints at the history of this location",
    "subtle movements in nature, like **wind rustling through grass** or ripples on water",
    "man-made objects slowly being reclaimed by nature"
]

# --- 建築/構造 (ARCH) ---
BG_ARCH_INDOOR = [
    "arched doorway", "bay window with a cushioned seat", "spiral staircase", "exposed brick wall", "industrial pipes overhead",
    "open beam ceiling", "paper sliding doors (shoji)", "baroque columns", "stained glass window", "vaulted ceiling",
    "hidden passageway behind a bookshelf", "ornate fireplace", "library stacks stretching to the ceiling", "grand staircase",
    "sunken lounge area", "two-story atrium", "mezzanine level overlooking a hall", "grand gallery with portraits", "indoor balcony",
    "captain's quarters on a starship", "holographic control room", "observation deck with reinforced glass"
]
BG_ARCH_OUTDOOR = [
    "stone torii gate", "retro phone booth", "vintage signboard", "ramen shop counter open to the street", "concrete overpass",
    "rusted fire escape", "ornate iron fence", "abandoned train car on overgrown tracks", "gothic spires against the sky",
    "flying buttresses of a cathedral", "modern glass facade reflecting the sky", "sloping tiled roof (kawara)", "wrought-iron balcony",
    "ancient stone ruins", "ruined castle walls", "suspension bridge cables at night", "monumental arch", "old stone well", "wooden windmill",
    "drawbridge of a castle", "ornate bell tower", "ancient roman aqueduct", "colonnade pathway", "pergola covered in vines",
    "spaceship landing pad", "base of a space elevator", "floating platforms connected by bridges"
]

# --- 小道具 (PROPS) ---
BG_PROPS_INDOOR = [
    "an **aesthetically pleasing arrangement** of related items",
    "a **deliberate, minimalist placement** of a few beautiful objects",
    "an organic, **lived-in clutter** that feels natural and inviting",
    "functional items that also possess an **artistic or elegant design**",
    "a single, significant object that is the **center of the scene's narrative**",
    "objects that **harmoniously blend** with the surrounding environment's color and style",
    "props that **cast interesting shadows** or reflect the ambient light"
]
BG_PROPS_OUTDOOR = [
    "items that seem **intentionally placed for a specific purpose** or ritual",
    "a comfortable setup that **invites someone to rest** (e.g., a bench with a forgotten book, a picnic blanket)",
    "remnants of a celebration or gathering, suggesting a **recent happy memory**",
    "objects that create a **stark but beautiful contrast** with the natural environment",
    "a trail of small items that **guides the eye** through the scene",
    "seasonal decorations that **enhance the feeling of the time of year**"
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
    # Bright & Positive Weather
    "perfect sunny day", "clear sky", "bright daylight", "crisp morning air", "warm gentle breeze", "beautiful afterglow",
    "sunbeam breaking through clouds", "rainbow after a sun shower", "pollen breeze", "blinding sunlight", "hazy summer day",
    # Rain & Wet
    "light drizzle", "heavy rain", "sun shower", "wet pavement shine", "raindrops on window",
    # Snow
    "gentle snowfall", "heavy blizzard", "diamond dust (ice crystals in air)",
    # Mist & Fog
    "misty air", "thick morning fog", "bioluminescent fog",
    # Clouds & Sky
    "overcast sky", "dramatic storm clouds", "fluffy white clouds", "lenticular clouds", "vibrant sunset clouds",
    # Storm
    "thunderstorm with lightning", "calm before a storm",
    # Fantastic & Special
    "meteor shower", "aurora borealis", "solar eclipse", "floating particles of light", "comet in the night sky",
    # General Conditions
    "chilly winter air", "calm ocean with gentle waves"
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
    # --- NEW THEME PACKS START ---
    "solapunk_art_nouveau": {
        "env_indoor": ["sun-drenched atrium with lush greenery", "bio-luminescent library", "hydroponic garden room", "ornate conservatory with brass mechanics", "artist's workshop with stained-glass windows", "elegant tea room with floral motifs"],
        "env_outdoor": ["city with verdant skyscrapers", "floating botanical islands", "solar-sail shipyard at dawn", "market street with clockwork vendors", "sweeping organic-shaped bridges over a canal", "community rooftop garden"],
        "details_indoor": ["intricate brass clockwork mechanisms", "flowing silk banners with nature patterns", "holographic plant displays", "potted ferns and flowers", "sunlight filtering through patterned glass"],
        "details_outdoor": ["stained-glass solar panels", "flocks of ornithopters in the sky", "pollen-like energy particles drifting in the air", "vines coiling around lampposts", "glowing moss pathways"],
        "arch_indoor": ["art nouveau arches", "spiraling staircases around a giant tree", "geodesic dome skylights", "curving wooden beams", "filigree banisters"],
        "arch_outdoor": ["towers adorned with plant life", "brass and copper filigree on buildings", "graceful, curved bridges", "wind-powered spires", "glass-domed public squares"],
        "props_indoor": ["ornate astrolabe", "elegant fountain pen and inkwell", "wind-up automaton companion", "botanical illustration charts", "velvet chaise lounge"],
        "props_outdoor": ["elegant airship moored to a tower", "brass telescope on a balcony", "automated flower cart", "public kinetic sculptures"],
        "light": ["warm golden sunlight", "soft bioluminescent glow", "light filtering through stained glass", "dappled light through leaves"],
        "texture": ["polished wood", "tarnished brass", "woven fabrics", "smooth ivory", "embossed leather", "mother-of-pearl inlays"],
        "weather": ["gentle sun showers", "clear blue sky", "warm breeze with floating petals", "bright sunny day"],
        "time": ["dawn", "golden hour", "clear sunlit day", "late afternoon"],
        "fx": ["volumetric light shafts", "gentle lens flare", "floating sparkling motes", "soft bloom effect"]
    },
    "tropical_resort": {
        "env_indoor": ["luxurious hotel suite with ocean view", "overwater bungalow interior", "spa room with orchid decorations", "thatched-roof restaurant", "aquarium lobby", "breezy cabana interior"],
        "env_outdoor": ["white sand beach with turquoise water", "infinity pool overlooking the ocean", "palm tree-lined boardwalk", "secluded waterfall lagoon", "bustling beachside bar", "coral reef visible from a glass-bottom boat"],
        "details_indoor": ["bowl of tropical fruits", "sheer white curtains billowing in the sea breeze", "seashell decorations", "fresh hibiscus flowers on a table", "a glass of cocktail with a tiny umbrella"],
        "details_outdoor": ["hammock strung between two palm trees", "footprints in the wet sand", "gentle waves lapping the shore", "distant sailboats on the horizon", "colorful parrots in trees"],
        "arch_indoor": ["open-air living space", "bamboo partition walls", "high vaulted ceilings with fans", "natural stone shower"],
        "arch_outdoor": ["thatched roofing (palapa)", "wooden pier stretching into the sea", "outdoor tiki bar", "bungalows on stilts over the water"],
        "props_indoor": ["wicker furniture", "four-poster bed with mosquito net", "minibar stocked with tropical juices", "folded towels shaped like swans"],
        "props_outdoor": ["surfboard leaning against a hut", "lounge chairs and sun umbrella", "kayak pulled up on the beach", "tiki torches at dusk"],
        "light": ["bright tropical sunlight", "golden sunset over the water", "soft lantern light at night", "light reflecting off the water's surface"],
        "texture": ["fine white sand", "rough palm tree bark", "smooth wet stones", "woven rattan", "crisp linen sheets"],
        "weather": ["clear sunny sky", "light tropical rain shower", "warm sea breeze", "high humidity haze"],
        "time": ["sunrise over the ocean", "high noon on the beach", "sunset", "balmy evening"],
        "fx": ["sparkling water reflections", "lens flare from the sun", "underwater caustics", "beautiful bokeh from distant lights"]
    },
    "cozy_academia": {
        "env_indoor": ["grand library with endless bookshelves", "cozy professor's study with a fireplace", "potions classroom with bubbling cauldrons", "observatory with a large telescope", "natural history museum hall at night", "common room with plush armchairs"],
        "env_outdoor": ["university courtyard with ivy-covered walls", "ancient campus grounds in autumn", "botanical greenhouse for magical plants", "cobblestone alley leading to a hidden bookshop", "college quad at twilight"],
        "details_indoor": ["motes of dust dancing in a sunbeam", "floating, self-sorting books", "a cup of steaming tea on a stack of books", "handwritten notes with arcane diagrams", "quill pen in an inkpot"],
        "details_outdoor": ["autumn leaves swirling in the wind", "gargoyles on the rooftops that seem to watch you", "a cat sleeping on a sun-warmed stone wall", "gas lamps flickering to life at dusk"],
        "arch_indoor": ["towering vaulted ceilings", "secret passageway behind a bookshelf", "stained-glass windows depicting constellations", "rolling library ladders", "grand spiral staircase"],
        "arch_outdoor": ["gothic arches and spires", "ivy-clad stone walls", "clock tower on campus", "wrought-iron gates", "ancient stone cloisters"],
        "props_indoor": ["antique globe that slowly rotates", "bubbling beakers and alembics", "crystal ball showing misty images", "human skull on a desk (for study)", "celestial map (orrery)"],
        "props_outdoor": ["weathered stone bench under a large oak tree", "bronze statue of a founder", "old-fashioned bicycle rack", "notice board with parchment announcements"],
        "light": ["warm light from a fireplace", "sunlight filtering through large arched windows", "soft glow from a desk lamp", "mysterious glow from a magical object"],
        "texture": ["aged paper", "dusty book covers", "worn leather armchairs", "dark polished wood", "cold stone floors", "tweed fabric"],
        "weather": ["crisp autumn air", "gentle rain against the windowpane", "overcast sky", "first light snowfall on campus"],
        "time": ["late afternoon light", "cozy evening", "deep night, lit by candlelight", "early morning mist"],
        "fx": ["magical particles glittering in the air", "soft focus on background", "glowing runes", "subtle vignette effect"]
    },
        "wafu_serenity_nature": {
        "env_indoor": ["shoji screen room with soft light", "traditional tea room (chashitsu)", "ryokan room with a cypress bath", "samurai residence study room", "veranda with a moon-viewing platform"],
        "env_outdoor": ["dry landscape garden (karesansui)", "bamboo grove path with sunlight filtering through", "stone steps lined with cedar trees", "Japanese garden with a koi pond", "castle town at dusk"],
        "details_indoor": ["a hanging scroll and flower arrangement in an alcove", "steam quietly rising from an iron kettle", "beautiful maki-e lacquerware box", "soft light from a paper lantern"],
        "details_outdoor": ["water flowing from a stone basin", "wind chime tinkling in the breeze", "moss wet with rain", "scattering autumn leaves"],
        "arch_indoor": ["lattice doors", "transom window carvings (ranma)", "circular window", "staggered shelves"],
        "arch_outdoor": ["gently curved temple roof", "arched drum bridge", "stone lanterns", "white walls and stone base of a castle"],
        "props_indoor": ["Japanese umbrella (wagasa)", "folding fan (sensu)", "koto instrument", "Go board"],
        "props_outdoor": ["deer-scarer fountain (shishi-odoshi)", "bench with a large parasol", "ceremonial banners", "red lanterns of a food stall"],
        "light": ["soft light through shoji paper screens", "sunlight filtering through trees (komorebi)", "warm glow of paper lanterns"],
        "texture": ["tatami mat texture", "plastered wall", "polished wooden floor", "washi paper texture"],
        "weather": ["calm indian summer day", "clear may weather", "gentle spring rain", "light mist"],
        "time": ["dawn", "twilight (tasogare)", "moonlit night"],
        "fx": ["hazy landscape", "reflection on the water surface", "soft light diffusion"]
    },
    "space_opera": {
        "env_indoor": ["spaceship bridge with a panoramic viewport", "gleaming white space station corridor", "emperor's throne room on a capital planet", "bustling alien cantina", "holographic library"],
        "env_outdoor": ["alien futuristic city skyline", "spaceport with departing and arriving ships", "lunar surface with twin suns", "palace's zero-gravity garden", "crystalline asteroid belt"],
        "details_indoor": ["floating control panels", "energy lines flowing along walls", "stars streaking past the window", "sculpture made of unknown minerals"],
        "details_outdoor": ["aurora shimmering in the sky", "planetary rings", "distant nebula", "giant floating creatures"],
        "arch_indoor": ["transparent tube walkways", "anti-gravity staircases", "massive domed ceilings"],
        "arch_outdoor": ["elegant skyscrapers piercing the heavens", "space elevator connecting to orbit", "massive ring-shaped habitat"],
        "props_indoor": ["floating companion droid", "energy sword", "holo-projector displaying a star chart"],
        "props_outdoor": ["streamlined personal speeder", "colossal battleship", "energy shield generator"],
        "light": ["harsh light from a star", "blueish glow from engines", "colorful light from a nebula"],
        "texture": ["polished metal armor", "luminous glass panels", "smooth nano-materials"],
        "weather": ["storm with methane rain", "calm vacuum", "shimmer of solar wind"],
        "time": ["endless night of space", "planetrise"],
        "fx": ["light streaks from warp travel", "lens flare", "starfield"]
    },
    "desert_oasis_arabian_nights": {
        "env_indoor": ["palace hall adorned with mosaic tiles", "throne room with fragrant incense smoke", "library with countless scrolls", "interior of a luxurious tent with rich textiles", "alchemist's hidden workshop"],
        "env_outdoor": ["vast sun-drenched sand dunes", "vibrant marketplace (souk) with colorful goods", "palace courtyard with a fountain", "secret oasis with a waterfall", "ancient ruins half-buried in sand"],
        "details_indoor": ["geometric tilework (zellige) on walls", "Persian rugs and cushions on the floor", "light filtering through latticework lamps", "piles of gold and treasures"],
        "details_outdoor": ["awnings fluttering in the wind", "a caravan of camels", "piles of spices in the market", "a distant mirage"],
        "arch_indoor": ["pointed arches (ogive arches)", "intricate wooden lattice windows (mashrabiya)", "domed ceilings"],
        "arch_outdoor": ["soaring minarets", "fortified city walls (kasbah)", "white-domed palace"],
        "props_indoor": ["hookah pipe", "scimitar sword", "magic lamp", "parchment star chart"],
        "props_outdoor": ["magic carpet", "market stalls", "large earthenware jars", "hammock in the shade of a palm tree"],
        "light": ["strong desert sunlight", "deep blue night sky full of stars", "flickering light of lanterns"],
        "texture": ["fine sand", "glossy glazed tiles", "densely woven carpets", "hammered metalwork"],
        "weather": ["cloudless clear sky", "a distant sandstorm", "scorching air"],
        "time": ["high noon sun", "magic hour after sunset", "starry night"],
        "fx": ["shimmering heat haze", "glow from a magical object", "brilliant starlight"]
    }
    # --- NEW THEME PACKS END ---
}

# UIで使うテーマの選択肢リスト
THEME_CHOICES = ["none", "おまかせ"] + sorted(list(THEME_PACKS.keys()))

# ========================
# 排他的な語彙グループ (更新済み)
# ========================
EXCLUSIVE_TAG_GROUPS = {
    # 光源の種類 (自然光 / 人工光 / 幻想光)
    "light_source_type": [
        # --- 太陽光・自然光 ---
        ["window daylight filtering through dust", "golden-hour light", "sunlight filtering through leaves (komorebi)", "high noon light", "blinding sunlight", "sunbeam breaking through clouds", "perfect sunny day"],
        # --- 月光・夜の自然光 ---
        ["ethereal moonlit ambience", "aurora borealis", "meteor shower"],
        # --- 人工光 (現代・SF) ---
        ["glowing monitor light on a face", "neon-soaked street at night", "colorful neon accent lights", "holographic glow", "fluorescent strip light", "strobe light effect", "blurry headlights in the rain", "streetlamp pools of light"],
        # --- 炎・古典的な光 ---
        ["flickering candlelight ambience", "soft fireplace glow", "paper lantern glow", "warm glow of paper lanterns", "lantern-lit lane at dusk"],
        # --- 幻想的な光 ---
        ["bioluminescent glow", "arcane glow from a spell", "light from glowing crystals", "magical particles floating", "floating particles of light"]
    ],

    # 天候条件 (晴れ / 雨 / 雪 / 霧など)
    "weather_condition": [
        # --- 晴天系 ---
        ["clear sky", "pollen breeze", "perfect sunny day", "bright daylight", "warm gentle breeze", "beautiful afterglow", "sunbeam breaking through clouds"],
        # --- 雨天系 ---
        ["light drizzle", "heavy rain", "sun shower", "rain-soaked boulevard", "raindrops on window", "wet pavement shine", "rain-soaked reflections", "thunderstorm with lightning"],
        # --- 雪・氷結系 ---
        ["gentle snowfall", "heavy blizzard", "snowy sidewalk", "diamond dust (ice crystals in air)", "frozen lake", "ancient glacier field"],
        # --- 霧・霞系 ---
        ["misty air", "thick morning fog", "hazy summer day", "bioluminescent fog", "hazy landscape"],
        # --- 宇宙空間 (無天候) ---
        ["calm vacuum", "endless night of space"]
    ],

    # 時間帯 (昼 / 夜)
    "time_of_day": [
        # --- 昼間 ---
        ["sunrise", "morning light", "high noon light", "golden hour", "afternoon sun", "bright daylight"],
        # --- 夜間 ---
        ["twilight", "blue hour", "deep midnight", "pre-dawn darkness", "late evening", "moonlit night", "starry night"]
    ],

    # 特殊効果・光の表現
    "environmental_effects": [
        # --- 光線・光芒 ---
        ["volumetric light rays", "dusty light rays", "sunbeams filtering through trees", "light shafts"],
        # --- レンズ効果・人工的エフェクト ---
        ["light leaks", "lens flare", "strobe light effect", "glitching effect on a screen", "chromatic aberration"],
        # --- 粒子・浮遊物 ---
        ["floating dust motes in sunbeam", "magical particles floating", "glowing motes of dust", "fire sparks and embers", "snow flurry in the air", "pollen breeze", "dandelion seeds drifting in the air"]
    ],

    # 場所の基本的な状態 (屋内 / 屋外)
    # ※これはシステム上フィルタリングされますが、念のため定義
    "location_base": [
        # --- 屋内系環境 ---
        BG_ENV_INDOOR,
        # --- 屋外系環境 ---
        BG_ENV_OUTDOOR
    ]
}





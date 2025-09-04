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
# background_vocab.py に記述する THEME_PACKS の全体を置き換えてください

THEME_PACKS = {
    "cyberpunk_futuristic": {
        "env_indoor": ["sleek starship interior", "space station viewport", "holographic command room", "cybernetic clinic", "hi-tech laboratory", "glowing data center", "grimy noodle bar", "back-alley cybernetics clinic"],
        "env_outdoor": ["futuristic metropolis", "cyberpunk street scene", "floating city in the clouds", "maglev transit hub", "off-world colony", "dystopian cityscape", "acid rain-slicked streets", "mega-corporation ziggurat"],
        "texture": ["brushed alloy", "carbon fiber", "glass panels", "iridescent materials", "chrome plating", "glowing circuit patterns", "wet asphalt"],
        "light": ["neon rim light", "holographic glow", "fluorescent strip light", "lens flare from flying vehicle"],
        "arch_indoor": ["transparent skybridge", "sleek modular buildings"],
        "arch_outdoor": ["luminescent pylons", "data spine towers", "floating platforms", "endless skyscrapers"],
        # ★★★ details/props を抽象的な指示に更新 ★★★
        "details_indoor": [
            "the **constant, restless flow of holographic data** streams",
            "**glitching and distorted light** from aging electronics",
            "the **sleek, reflective surfaces** of advanced cybernetics",
            "a **network of cables and conduits** integrated into the architecture"
        ],
        "details_outdoor": [
            "the **atmospheric haze** catching and diffusing the city's countless lights",
            "**reflections of the neon-drenched city** in puddles of acid rain",
            "the **overwhelming sense of scale** from towering mega-structures",
            "**digital graffiti and advertisements** projected onto building facades"
        ],
        "props_indoor": [
            "**utilitarian, function-over-form technology** common on the streets",
            "**discarded or broken cybernetic parts** hinting at a recent conflict",
            "**sleek, corporate-branded technology** that looks pristine and intimidating",
            "a **makeshift setup** of cobbled-together electronics"
        ],
        "props_outdoor": [
            "**automated drones** performing mundane tasks like delivery or surveillance",
            "**objects that suggest a stark divide** between the rich and the poor",
            "**public terminals and interfaces** integrated into the urban landscape",
            "**heavily armored vehicles** that signify a corporate or state presence"
        ],
    },
    "school": {
        "env_indoor": ["classroom with wooden desks", "sunlit library aisles", "science lab benches", "school gymnasium", "school cafeteria", "empty hallway with lockers", "music room", "art room"],
        "env_outdoor": ["school courtyard under cherry blossoms", "track field bleachers", "school gate", "school rooftop", "basketball court at sunset", "swimming pool for lessons"],
        "texture": ["scuffed linoleum", "polished gym floor", "worn wooden desks", "graffiti on locker doors"],
        "light": ["fluorescent classroom lighting", "sunlight through large windows", "late afternoon sun on the field"],
        "arch_indoor": ["corridor with lockers", "stairwell with afternoon light"],
        "arch_outdoor": ["brick facade", "school bell tower", "chain-link fence around sports field"],
        # ★★★ details/props を抽象的な指示に更新 ★★★
        "details_indoor": [
            "**sunlight streaming through large windows**, illuminating floating dust motes",
            "**personal touches and doodles** left behind on desks and lockers",
            "the **organized chaos** of a classroom in active use",
            "a sense of **quiet nostalgia and memories** lingering in the empty spaces"
        ],
        "details_outdoor": [
            "the **play of shadows** on the ground in the late afternoon",
            "**evidence of the changing seasons** on the school grounds",
            "the **faded lines and worn surfaces** of a well-used sports court",
            "a **gentle breeze** carrying the sounds of distant activity"
        ],
        "props_indoor": [
            "**materials for learning and creativity**, arranged on desks",
            "**evidence of extracurricular activities** and student passions",
            "**items that show the passage of a long school day**",
            "**trophies and awards** that speak to the school's history and pride"
        ],
        "props_outdoor": [
            "**sports equipment** left out as if a game just ended",
            "**items forgotten by students**, telling a small story",
            "**bicycles neatly parked**, suggesting the daily commute of students",
            "**seasonal decorations** for a school event or festival"
        ],
    },
    "fantasy": {
        "env_indoor": ["wizard tower study", "crystal conservatory", "ancient library", "dragon's hoard cavern", "throne room of a castle", "alchemist's laboratory", "enchanted forest cottage", "elven hall", "dwarven forge"],
        "env_outdoor": ["floating islands in sky", "enchanted forest with glowing mushrooms", "crystal cavern", "moonlit meadow", "fairy ring in a forest", "ancient ruins on a misty hill", "dragon's peak with lava flow"],
        "texture": ["iridescent crystal", "mossy stone", "ancient runes on rock", "dragon scales", "mithril silver"],
        "light": ["ethereal moonlight", "bioluminescent glow", "arcane glow from a spell", "light from glowing crystals"],
        "arch_indoor": ["ancient stone archways", "spires of a wizard's tower", "crystal formations"],
        "arch_outdoor": ["ruined castle walls", "elven tree-houses", "bridge made of light"],
        # ★★★ details/props を抽象的な指示に更新 ★★★
        "details_indoor": [
            "an **ambient, magical glow** emanating from an unseen source",
            "the air **shimmering with raw magical energy**",
            "**ancient, intricate carvings** that tell a forgotten story",
            "**fantastical flora** integrated into the architecture"
        ],
        "details_outdoor": [
            "**particles of light or magic** drifting gently in the air",
            "the **colossal scale of ancient ruins** or natural formations",
            "an **otherworldly quality to the natural light**",
            "**impossible geography** that defies the laws of physics"
        ],
        "props_indoor": [
            "**artifacts of immense power or ancient knowledge**",
            "**ingredients and tools for alchemy or spellcrafting**",
            "**objects of regal or divine significance**",
            "a **legendary weapon or item**, presented with reverence"
        ],
        "props_outdoor": [
            "**objects that serve as a source of immense magical power**",
            "**remains of a great battle** from a bygone era",
            "**offerings left for ancient gods or spirits**",
            "**a path marked by mystical stones or lights**"
        ],
    },
    "gothic_horror": {
        "env_indoor": ["haunted mansion hallway", "dusty gothic library", "crypt interior", "abandoned chapel", "laboratory of a mad scientist"],
        "env_outdoor": ["misty graveyard at midnight", "crumbling abbey ruins", "dark forest with twisted trees", "lonely cliffside castle"],
        "texture": ["aged stone", "tattered velvet", "cold iron bars", "rotting wood", "dusty surfaces"],
        "light": ["dim candlelight", "pale moonlight filtering through grimy windows", "lightning flashes", "single oil lamp"],
        "arch_indoor": ["pointed arches", "stone spiral staircase", "gargoyles looking down"],
        "arch_outdoor": ["flying buttresses", "cemetery gates", "crypt entrance"],
        # ★★★ details/props を抽象的な指示に更新 ★★★
        "details_indoor": [
            "**deep, imposing shadows** that seem to hide something",
            "a **thick layer of dust** covering everything, disturbed in one spot",
            "the feeling of being **watched by portraits** on the wall",
            "a **chilling draft** from an unseen source"
        ],
        "details_outdoor": [
            "**twisted, skeletal trees** silhouetted against a pale moon",
            "a **dense, rolling fog** that obscures the ground",
            "the **ominous shapes of crumbling ruins** in the darkness",
            "an **unnatural silence** in the air"
        ],
        "props_indoor": [
            "**objects suggesting a dark and disturbing history**",
            "**items that have been left in a hurry**, as if fleeing",
            "**scientific or occult instruments** for a sinister purpose",
            "a **single object that is unnervingly out of place**"
        ],
        "props_outdoor": [
            "**weathered tombstones, some overturned or broken**",
            "**tools for digging**, left abandoned",
            "a **solitary, flickering lantern** suggesting a lone presence",
            "**personal belongings lost or discarded** in the mud"
        ],
    },
    "solapunk_art_nouveau": {
        "env_indoor": ["sun-drenched atrium with lush greenery", "bio-luminescent library", "hydroponic garden room", "ornate conservatory with brass mechanics", "artist's workshop with stained-glass windows", "elegant tea room with floral motifs"],
        "env_outdoor": ["city with verdant skyscrapers", "floating botanical islands", "solar-sail shipyard at dawn", "market street with clockwork vendors", "sweeping organic-shaped bridges over a canal", "community rooftop garden"],
        "light": ["warm golden sunlight", "soft bioluminescent glow", "light filtering through stained glass", "dappled light through leaves"],
        "texture": ["polished wood", "tarnished brass", "woven fabrics", "smooth ivory", "embossed leather", "mother-of-pearl inlays"],
        # ★★★ details/props を抽象的な指示に更新 ★★★
        "details_indoor": [
            "**intricate, flowing lines** inspired by nature in the architecture",
            "the **harmonious integration of plant life** and living space",
            "the **gentle, rhythmic movement** of clockwork mechanisms",
            "**sunlight creating beautiful patterns** as it passes through stained glass"
        ],
        "details_outdoor": [
            "the **elegant fusion of technology and nature**",
            "a **sense of community and sustainable living**",
            "the **play of light on brass and copper** architectural details",
            "**graceful, flowing forms** in bridges, buildings, and vehicles"
        ],
        "props_indoor": [
            "**beautifully crafted objects that are both artistic and functional**",
            "**items related to botany, art, or astronomy**",
            "**elegant furniture with organic, curved lines**",
            "**automatons designed with artistic flair**, performing helpful tasks"
        ],
        "props_outdoor": [
            "**ornate, beautifully designed public transportation**, like airships or trams",
            "**community gardens and shared spaces** for public enjoyment",
            "**kinetic sculptures powered by wind or solar energy**",
            "**market stalls selling handcrafted goods and organic produce**"
        ],
    },
    "tropical_resort": {
        "env_indoor": ["luxurious hotel suite with ocean view", "overwater bungalow interior", "spa room with orchid decorations", "thatched-roof restaurant", "aquarium lobby", "breezy cabana interior"],
        "env_outdoor": ["white sand beach with turquoise water", "infinity pool overlooking the ocean", "palm tree-lined boardwalk", "secluded waterfall lagoon", "bustling beachside bar", "coral reef visible from a glass-bottom boat"],
        "light": ["bright tropical sunlight", "golden sunset over the water", "soft lantern light at night", "light reflecting off the water's surface"],
        "texture": ["fine white sand", "rough palm tree bark", "smooth wet stones", "woven rattan", "crisp linen sheets"],
        # ★★★ details/props を抽象的な指示に更新 ★★★
        "details_indoor": [
            "a **gentle sea breeze** causing sheer curtains to billow",
            "the **clean, refreshing scent** of tropical flowers and salt air",
            "the **seamless transition** between indoor and outdoor space",
            "**details made from natural materials** like wood, stone, and shell"
        ],
        "details_outdoor": [
            "the **crystal-clear quality of the turquoise water**",
            "the **soft, warm texture of the white sand**",
            "the **sound of gentle waves** lapping the shore",
            "the **vibrant colors of tropical flora** against the blue sky"
        ],
        "props_indoor": [
            "**items that invite relaxation and comfort**",
            "**luxurious amenities** for a perfect vacation",
            "a **refreshing tropical drink or fresh fruit**, beautifully presented",
            "**furniture made from light, natural materials** like wicker or bamboo"
        ],
        "props_outdoor": [
            "**equipment for enjoying the water**, like surfboards or kayaks",
            "a **perfectly placed spot to relax and enjoy the view**",
            "**tiki torches or lanterns that create a romantic mood** at dusk",
            "**objects that suggest leisure and carefree living**"
        ],
    },
    "cozy_academia": {
        "env_indoor": ["grand library with endless bookshelves", "cozy professor's study with a fireplace", "potions classroom with bubbling cauldrons", "observatory with a large telescope", "natural history museum hall at night", "common room with plush armchairs"],
        "env_outdoor": ["university courtyard with ivy-covered walls", "ancient campus grounds in autumn", "botanical greenhouse for magical plants", "cobblestone alley leading to a hidden bookshop", "college quad at twilight"],
        "light": ["warm light from a fireplace", "sunlight filtering through large arched windows", "soft glow from a desk lamp", "mysterious glow from a magical object"],
        "texture": ["aged paper", "dusty book covers", "worn leather armchairs", "dark polished wood", "cold stone floors", "tweed fabric"],
        # ★★★ details/props を抽象的な指示に更新 ★★★
        "details_indoor": [
            "the **smell of old books, woodsmoke, and brewing tea**",
            "the **comforting silence of a library**, broken only by turning pages",
            "**motes of dust dancing in a sunbeam** filtering through a tall window",
            "a **sense of deep history and accumulated knowledge**"
        ],
        "details_outdoor": [
            "the **crisp feeling of autumn air**",
            "**ivy clinging to ancient stone walls**",
            "the **sound of distant bells or a choir**",
            "the **warm, inviting glow** from windows at twilight"
        ],
        "props_indoor": [
            "**piles and shelves of books**, suggesting a love of reading and research",
            "**objects related to scholarly pursuits** like astronomy, history, or botany",
            "a **comfortable place to sit and read** for hours",
            "**items that suggest a touch of magic or mystery** hidden within the academic setting"
        ],
        "props_outdoor": [
            "**architectural features that inspire a sense of wonder and history**",
            "a **quiet, secluded bench** perfect for contemplation",
            "**items that hint at the traditions and ceremonies** of the institution",
            "**seasonal elements**, like fallen leaves or a light dusting of snow"
        ],
    },
    "wafu_serenity_nature": {
        "env_indoor": ["shoji screen room with soft light", "traditional tea room (chashitsu)", "ryokan room with a cypress bath", "samurai residence study room", "veranda with a moon-viewing platform"],
        "env_outdoor": ["dry landscape garden (karesansui)", "bamboo grove path with sunlight filtering through", "stone steps lined with cedar trees", "Japanese garden with a koi pond", "castle town at dusk"],
        "light": ["soft light through shoji paper screens", "sunlight filtering through trees (komorebi)", "warm glow of paper lanterns"],
        "texture": ["tatami mat texture", "plastered wall", "polished wooden floor", "washi paper texture"],
        # ★★★ details/props を抽象的な指示に更新 ★★★
        "details_indoor": [
            "the **play of light and shadow** through a lattice screen",
            "a **perfectly framed view of the garden** from inside",
            "an atmosphere of **tranquility, simplicity, and wabi-sabi**",
            "the **scent of tatami, hinoki wood, and green tea**"
        ],
        "details_outdoor": [
            "the **sound of a shishi-odoshi** (deer-scarer) or a gentle stream",
            "the **feeling of moss underfoot** on ancient stones",
            "the **dance of light and shadow** in a bamboo grove",
            "a **sense of deep peace and harmony with nature**"
        ],
        "props_indoor": [
            "a **single, beautiful object, perfectly placed** in an alcove (tokonoma)",
            "**items for a traditional art or ceremony**, like tea ceremony or calligraphy",
            "**minimalist furniture** that emphasizes the beauty of the space",
            "**objects that reflect a deep appreciation for nature and craftsmanship**"
        ],
        "props_outdoor": [
            "**stones and sand raked into patterns** that evoke water and mountains",
            "**elements designed to blend seamlessly with the natural landscape**",
            "a **place for quiet contemplation and meditation**",
            "**objects that change beautifully with the seasons**"
        ],
    },
    "space_opera": {
        "env_indoor": ["spaceship bridge with a panoramic viewport", "gleaming white space station corridor", "emperor's throne room on a capital planet", "bustling alien cantina", "holographic library"],
        "env_outdoor": ["alien futuristic city skyline", "spaceport with departing and arriving ships", "lunar surface with twin suns", "palace's zero-gravity garden", "crystalline asteroid belt"],
        "light": ["harsh light from a star", "blueish glow from engines", "colorful light from a nebula"],
        "texture": ["polished metal armor", "luminous glass panels", "smooth nano-materials"],
        # ★★★ details/props を抽象的な指示に更新 ★★★
        "details_indoor": [
            "a **panoramic view of stars, planets, or nebulae** through a large window",
            "the **low, constant hum of a starship's engine** or life support",
            "the **clean, sterile look of advanced technology**",
            "**holographic displays and interfaces** integrated everywhere"
        ],
        "details_outdoor": [
            "the **breathtaking scale of alien megastructures** or celestial phenomena",
            "the **sight of multiple moons or suns** in the sky",
            "the **vibrant, chaotic energy** of a multicultural spaceport",
            "an **awe-inspiring view of a fleet of starships**"
        ],
        "props_indoor": [
            "**advanced technology for command, control, and communication**",
            "**items that show the diversity of alien species** present",
            "**personal belongings that hint at a life spent traveling the stars**",
            "**symbols of power and authority** within a galactic empire or federation"
        ],
        "props_outdoor": [
            "**a variety of starships, from sleek fighters to massive cruisers**",
            "**technology for terraforming or resource extraction on an alien world**",
            "**monuments or statues commemorating a great historical event**",
            "**defensive installations**, like energy shields or weapon platforms"
        ],
    },
    "desert_oasis_arabian_nights": {
        "env_indoor": ["palace hall adorned with mosaic tiles", "throne room with fragrant incense smoke", "library with countless scrolls", "interior of a luxurious tent with rich textiles", "alchemist's hidden workshop"],
        "env_outdoor": ["vast sun-drenched sand dunes", "vibrant marketplace (souk) with colorful goods", "palace courtyard with a fountain", "secret oasis with a waterfall", "ancient ruins half-buried in sand"],
        "light": ["strong desert sunlight", "deep blue night sky full of stars", "flickering light of lanterns"],
        "texture": ["fine sand", "glossy glazed tiles", "densely woven carpets", "hammered metalwork"],
        # ★★★ details/props を抽象的な指示に更新 ★★★
        "details_indoor": [
            "**intricate geometric patterns** (zellige) that create a mesmerizing effect",
            "**cool air and the gentle sound of water**, a stark contrast to the outside heat",
            "the **rich aroma of spices, incense, and perfumes**",
            "**ornate archways and latticework** that create beautiful, complex shadows"
        ],
        "details_outdoor": [
            "the **shimmering heat haze** rising from the endless sand dunes",
            "the **vibrant, chaotic energy of a bustling marketplace** (souk)",
            "the **brilliant, dazzling display of stars** in a clear desert night sky",
            "a **sense of ancient history and forgotten magic** among the ruins"
        ],
        "props_indoor": [
            "**luxurious textiles, like silk cushions and elaborate carpets**, for comfort and beauty",
            "**items that suggest wealth, trade, and a long history of storytelling**",
            "**objects related to magic, alchemy, or astronomy**",
            "a **source of cool, clean water**, the most valuable treasure in the desert"
        ],
        "props_outdoor": [
            "**elements that provide shade and relief from the intense sun**",
            "**goods from all corners of the world**, hinting at a crossroads of trade",
            "**evidence of a hidden, magical world** just beneath the surface",
            "**items needed for a long journey across the vast desert**"
        ],
    }
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






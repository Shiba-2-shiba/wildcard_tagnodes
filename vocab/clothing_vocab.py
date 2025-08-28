# clothing_vocab.py (v4 - 状態・新テーマ対応版)
# - 「服装の状態」カテゴリを追加
# - テーマパックをより具体的・多様なシチュエーションベースに刷新

# ========================
# 1. コア語彙 (色、素材、柄)
# ========================
COLORS = [
    "black", "white", "gray", "charcoal", "ivory", "cream", "beige", "khaki", "off-white", "jet black", "snow white",
    "red", "crimson", "scarlet", "wine", "burgundy", "maroon", "pink", "hot pink", "fuchsia", "rose", "coral", "blush pink", "magenta",
    "blue", "navy blue", "royal blue", "sky blue", "cobalt", "cyan", "teal", "turquoise", "midnight blue", "baby blue", "periwinkle",
    "green", "emerald", "olive", "forest green", "lime green", "mint green", "sage green", "jade", "seafoam green",
    "yellow", "mustard", "gold", "orange", "apricot", "peach", "tangerine", "citrine",
    "purple", "violet", "lavender", "mauve", "plum", "indigo", "lilac", "amethyst",
    "brown", "chocolate", "tan", "caramel", "bronze", "coffee", "taupe",
    "silver", "gunmetal", "metallic", "rose gold", "platinum", "iridescent", "holographic", "transparent", "clear"
]
MATERIALS = [
    "cotton", "denim", "linen", "silk", "wool", "cashmere", "velvet", "leather", "suede", "corduroy", "hemp", "bamboo fabric",
    "polyester", "nylon", "spandex", "lycra", "rayon", "acrylic", "latex", "PVC", "vinyl", "faux leather", "neoprene",
    "lace", "chantilly lace", "chiffon", "organza", "tulle", "mesh", "fishnet", "georgette", "see-through fabric", "gossamer",
    "knit", "ribbed knit", "cable knit", "fleece", "jersey", "chenille", "boucle",
    "satin", "charmeuse", "brocade", "tweed", "sequin fabric", "faux fur", "terrycloth", "lamé", "jacquard", "crepe"
]
PATTERNS = [
    "solid", "striped", "vertical stripes", "horizontal stripes", "pinstripe", "polka-dot", "checked", "gingham", "tartan", "plaid", "checkered",
    "argyle", "chevron", "herringbone", "houndstooth", "grid", "geometric-pattern", "diamond-pattern", "cubist-pattern",
    "floral", "botanical", "paisley", "leaf-print", "tropical-print", "rose-print", "cherry-blossom-print",
    "animal-print", "leopard-print", "zebra-print", "snake-print", "tiger-print", "cheetah-print", "crocodile-print",
    "abstract", "camouflage", "tie-dye", "gradient", "ombre", "star-pattern", "heart-pattern", "fair isle", "damask", "baroque", "cosmic-print", "ikat"
]

# ========================
# 2. 服の基本アイテム
# ========================
TOPS = ["t-shirt", "graphic tee", "blouse", "crop top", "hoodie", "turtleneck sweater", "off-the-shoulder top", "polo shirt", "henley shirt", "camisole", "tank top", "button-down shirt", "flannel shirt", "cashmere knit", "v-neck sweater", "cardigan", "sweatshirt", "tube top", "halter top", "peasant blouse", "tunic", "bustier top", "corset top", "bodysuit", "bandeau top", "smocked top", "wrap top"]
BOTTOMS = ["jeans", "skinny jeans", "straight-leg jeans", "bootcut jeans", "ripped jeans", "flared jeans", "cargo pants", "pleated skirt", "mini skirt", "maxi skirt", "pencil skirt", "A-line skirt", "leggings", "biker shorts", "tailored trousers", "culottes", "denim shorts", "wide-leg pants", "corduroy pants", "yoga pants", "capri pants", "hotpants", "skort", "hip-huggers", "palazzo pants"]
OUTERWEAR = ["denim jacket", "leather jacket", "biker jacket", "bomber jacket", "trench coat", "wool coat", "blazer", "parka", "puffer jacket", "windbreaker", "vest", "bolero", "duffle coat", "pea coat", "overcoat", "hooded jacket", "fleece jacket", "cape", "moto jacket", "longline cardigan", "kimono jacket", "anorak"]
DRESSES_SETS = ["sundress", "A-line dress", "wrap dress", "pleated dress", "tailored blazer set", "jumpsuit", "romper", "maxi dress", "shirt dress", "sweater dress", "sheath dress", "blazer dress", "slip dress", "bodycon dress", "fit and flare dress", "babydoll dress", "little black dress", "cocktail dress", "evening gown", "skirt and blouse set", "two-piece set", "cutout dress", "qipao", "cheongsam", "kaftan"]
LINGERIE = ["lace bra", "lace panties", "corset", "pvc corset", "leather corset", "waspie", "satin bustier", "lace bodysuit", "fishnet bodysuit", "silk chemise", "garter belt", "suspender belt", "latex mini dress", "fishnet stockings", "thigh-high stockings", "satin blindfold", "nipple tassels", "pasties", "open-cup bra", "shelf bra", "cupless bra", "strappy cage bra", "micro bikini", "crotchless panty", "open-back thong", "lace teddy", "sheer bodysuit", "satin corset", "longline bralette", "underwire bra and thong set", "babydoll", "g-string", "sheer kimono robe", "lace-trim yukata lingerie", "merry widow", "negligee"]

# ========================
# 3. 装飾・スタイル
# ========================
STYLES = ["V-neck", "crew-neck", "scoop-neck", "boat-neck", "turtleneck", "high-neck", "halter", "sweetheart neckline", "plunge neckline", "cowl neck", "sleeveless", "short-sleeve", "long-sleeve", "cap-sleeve", "puffed-sleeve", "bell-sleeve", "raglan-sleeve", "kimono-sleeve", "bishop sleeve", "slim-fit", "loose-fit", "oversized", "A-line", "bodycon", "wrap-front", "peplum", "cropped", "high-waist", "low-rise", "empire waist", "draped", "ruched", "asymmetric hem", "high-low hem", "scalloped hem", "side-slit", "thigh-high slit", "front slit", "double slit", "open-back", "low-back", "lace-up back", "criss-cross back", "backless", "T-back", "strapless", "one-shoulder", "off-the-shoulder", "cold-shoulder", "button-front", "zip-front", "underboob cutout", "cleavage cutout", "hip cutout"]
EMBELLISH = ["lace trim", "ruffles", "frills", "fringe", "piping", "contrast trim", "scalloped edges", "feathers", "fur trim", "bows", "ribbons", "sequins", "pearls", "crystals", "rhinestones", "studs", "grommets", "beads", "metal hardware", "embroidery", "pleats", "pintucks", "smocking", "ruching", "quilting", "cutouts", "sheer panels", "mesh inserts", "lace panels", "slashed details", "decorative buttons", "buckles", "zippers", "lace-up details", "hook-and-eye", "snap closure", "clasps", "appliques", "patches", "tassels", "chain details", "body chains", "contrast stitching", "epaulettes"]

# ========================
# 4. 露出表現・セクシー系アクセント
# ========================
ACCENTS_EROTIC = ["with garter straps", "with detachable garters", "with attached stockings", "with sheer gloves", "with a delicate choker", "with matching thong", "with lace-up back", "with open-crotch design", "with open-cup features", "with peekaboo panels", "with keyhole opening", "with O-ring details", "with metal rings", "with chain accents", "with delicate body chains", "with harness straps", "with bondage-style straps", "with lace-up sides", "with cutout hips", "with a plunging back", "held together by thin straps", "with strategic cutouts", "accented with pearls"]
REVEAL_MILD = ["subtle sheer panels", "keyhole cutout", "low back", "shoulder cutouts", "back keyhole", "sheer sleeves", "a hint of sideboob", "modest cleavage", "slit on the leg", "off-shoulder revealing collarbones"]
REVEAL_BOLD = ["see-through panels", "micro cutouts", "high-leg cut", "thong back", "deep plunge neckline", "cleavage window", "sideboob cutout", "underboob cutout", "hip cutouts", "backless design", "extremely short hemline", "navel cutout", "daringly high slit"]
REVEAL_EXPLICIT = ["open sides", "sideboob cutouts", "barely-there straps", "ultra high-leg", "backless micro dress", "fully transparent", "cupless design", "crotchless design", "held by a single thread", "wardrobe malfunction", "nipple cutout", "completely sheer", "strategically placed rips", "unzipped front"]

# ========================
# 5. [新設] 服装の状態
# ========================
STATES = [
    "wet", "soaking wet", "damp", "rain-soaked", "water-splashed", "dripping wet",
    "dirty", "mud-stained", "torn", "ripped", "shredded", "worn-out", "tattered", "blood-stained",
    "messy", "disheveled", "wrinkled", "askew", "loosened", "unbuttoned", "partially unzipped", "falling off shoulder",
    "glowing", "shimmering", "wind-blown", "sun-bleached", "frozen", "covered in snow"
]

# ========================
# 6. 排他グループ
# ========================
EXCLUSIVE_GROUPS = {
    "season": {"summer": ["sundress", "linen", "bikini", "romper", "denim shorts", "tank top"], "winter": ["wool coat", "turtleneck sweater", "puffer jacket", "fleece", "cashmere knit", "corduroy"]},
    "garment_slot": {"full_body": DRESSES_SETS, "tops": TOPS, "bottoms": BOTTOMS}
}

# ========================
# 7. [改修] テーマパック
# ========================
THEMES = {
    "office_lady": {"tops": ["blouse", "button-down shirt", "knit top"], "bottoms": ["pencil skirt", "tailored trousers"], "outerwear": ["blazer"], "dresses_sets": ["sheath dress"], "patterns": ["solid", "pinstripe"]},
    "beach_resort": {"dresses_sets": ["sundress", "maxi dress", "romper"], "tops": ["camisole", "off-the-shoulder top", "bandeau top"], "bottoms": ["denim shorts", "wrap skirt"], "materials": ["linen", "cotton", "chiffon"], "patterns": ["tropical-print", "floral"]},
    "rainy_day": {"outerwear": ["trench coat", "raincoat", "windbreaker"], "bottoms": ["jeans"], "states": ["wet", "rain-soaked", "damp"], "patterns": ["solid"]},
    "fantasy_battle": {"tops": ["corset top", "leather bustier"], "bottoms": ["leather pants", "armored skirt"], "outerwear": ["cape", "armored vest"], "materials": ["leather", "metal", "chainmail"], "embellish": ["studs", "buckles", "engraved patterns"]},
    "cyberpunk_night": {"tops": ["techwear crop top", "holographic tank top"], "outerwear": ["bomber jacket with LED", "transparent vinyl jacket"], "bottoms": ["cargo pants with straps"], "materials": ["PVC", "nylon", "holographic"], "embellish": ["glowing piping", "buckles"]},
    "traditional_japanese": {"dresses_sets": ["kimono", "yukata", "hakama skirt set"], "lingerie": ["sheer kimono robe"], "materials": ["silk", "satin", "cotton"], "patterns": ["sakura", "asanoha", "seigaiha"]},
    "school_uniform": {"tops": ["sailor blouse", "button-down shirt"], "bottoms": ["pleated skirt"], "outerwear": ["blazer", "cardigan"], "patterns": ["plaid", "solid"]},
    "gothic_lolita": {"dresses_sets": ["babydoll dress", "victorian goth dress"], "tops": ["lace blouse"], "bottoms": ["tiered skirt"], "materials": ["velvet", "lace", "cotton"], "embellish": ["ruffles", "bows", "lace trim"]},
    "rock_concert": {"tops": ["graphic tee", "band t-shirt", "mesh top"], "bottoms": ["ripped jeans", "leather pants", "mini skirt"], "outerwear": ["biker jacket", "denim jacket"], "materials": ["denim", "leather", "mesh"]},
    "winter_date": {"outerwear": ["wool coat", "duffle coat", "puffer jacket"], "tops": ["turtleneck sweater", "cashmere knit"], "bottoms": ["pleated skirt", "wool trousers"], "states": ["covered in snow"]},
    "secret_agent": {"dresses_sets": ["bodycon dress", "evening gown"], "styles": ["thigh-high slit", "backless"], "materials": ["satin", "velvet"], "accents_erotic": ["with garter straps"]},
    "gym_workout": {"tops": ["sports bra", "tank top"], "bottoms": ["leggings", "yoga pants", "biker shorts"], "materials": ["spandex", "nylon", "jersey"]}
}

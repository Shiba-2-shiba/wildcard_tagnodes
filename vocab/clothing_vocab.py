# clothing_vocab.py (v3 - 大幅拡張版)
# カテゴリを細分化し、語彙を大幅に拡張したバージョン。
# clothing_tag.pyの生成ロジックをこれに合わせて変更する必要があります。

# ========================
# 1. コア語彙 (色、素材、柄)
# ========================
COLORS = [
    # Basic
    "black", "white", "gray", "charcoal", "ivory", "cream", "beige", "khaki", "off-white", "jet black", "snow white",
    # Red/Pink
    "red", "crimson", "scarlet", "wine", "burgundy", "maroon", "pink", "hot pink", "fuchsia", "rose", "coral", "blush pink", "magenta",
    # Blue
    "blue", "navy blue", "royal blue", "sky blue", "cobalt", "cyan", "teal", "turquoise", "midnight blue", "baby blue", "periwinkle",
    # Green
    "green", "emerald", "olive", "forest green", "lime green", "mint green", "sage green", "jade", "seafoam green",
    # Yellow/Orange
    "yellow", "mustard", "gold", "orange", "apricot", "peach", "tangerine", "citrine",
    # Purple
    "purple", "violet", "lavender", "mauve", "plum", "indigo", "lilac", "amethyst",
    # Brown
    "brown", "chocolate", "tan", "caramel", "bronze", "coffee", "taupe",
    # Metallic & Other
    "silver", "gunmetal", "metallic", "rose gold", "platinum", "iridescent", "holographic", "transparent", "clear"
]

MATERIALS = [
    # Natural Fibers
    "cotton", "denim", "linen", "silk", "wool", "cashmere", "velvet", "leather", "suede", "corduroy", "hemp", "bamboo fabric",
    # Synthetic Fibers
    "polyester", "nylon", "spandex", "lycra", "rayon", "acrylic", "latex", "PVC", "vinyl", "faux leather", "neoprene",
    # Sheer & Lace
    "lace", "chantilly lace", "chiffon", "organza", "tulle", "mesh", "fishnet", "georgette", "see-through fabric", "gossamer",
    # Knits
    "knit", "ribbed knit", "cable knit", "fleece", "jersey", "chenille", "boucle",
    # Others
    "satin", "charmeuse", "brocade", "tweed", "sequin fabric", "faux fur", "terrycloth", "lamé", "jacquard", "crepe"
]

PATTERNS = [
    # Classic
    "solid", "striped", "vertical stripes", "horizontal stripes", "pinstripe", "polka-dot", "checked", "gingham", "tartan", "plaid", "checkered",
    # Geometric
    "argyle", "chevron", "herringbone", "houndstooth", "grid", "geometric-pattern", "diamond-pattern", "cubist-pattern",
    # Floral & Nature
    "floral", "botanical", "paisley", "leaf-print", "tropical-print", "rose-print", "cherry-blossom-print",
    # Animal
    "animal-print", "leopard-print", "zebra-print", "snake-print", "tiger-print", "cheetah-print", "crocodile-print",
    # Abstract & Others
    "abstract", "camouflage", "tie-dye", "gradient", "ombre", "star-pattern", "heart-pattern", "fair isle", "damask", "baroque", "cosmic-print", "ikat"
]

# ========================
# 2. 服の基本アイテム
# ========================
TOPS = [
    "t-shirt", "graphic tee", "blouse", "crop top", "hoodie", "turtleneck sweater",
    "off-the-shoulder top", "polo shirt", "henley shirt", "camisole", "tank top",
    "button-down shirt", "flannel shirt", "cashmere knit", "v-neck sweater", "cardigan",
    "sweatshirt", "tube top", "halter top", "peasant blouse", "tunic", "bustier top",
    "corset top", "bodysuit", "bandeau top", "smocked top", "wrap top"
]

BOTTOMS = [
    "jeans", "skinny jeans", "straight-leg jeans", "bootcut jeans", "ripped jeans", "flared jeans",
    "cargo pants", "pleated skirt", "mini skirt", "maxi skirt", "pencil skirt", "A-line skirt",
    "leggings", "biker shorts", "tailored trousers", "culottes", "denim shorts", "wide-leg pants",
    "corduroy pants", "yoga pants", "capri pants", "hotpants", "skort", "hip-huggers", "palazzo pants"
]

OUTERWEAR = [
    "denim jacket", "leather jacket", "biker jacket", "bomber jacket", "trench coat",
    "wool coat", "blazer", "parka", "puffer jacket", "windbreaker", "vest", "bolero",
    "duffle coat", "pea coat", "overcoat", "hooded jacket", "fleece jacket", "cape",
    "moto jacket", "longline cardigan", "kimono jacket", "anorak"
]

DRESSES_SETS = [
    "sundress", "A-line dress", "wrap dress", "pleated dress", "tailored blazer set",
    "jumpsuit", "romper", "maxi dress", "shirt dress", "sweater dress", "sheath dress",
    "blazer dress", "slip dress", "bodycon dress", "fit and flare dress", "babydoll dress",
    "little black dress", "cocktail dress", "evening gown", "skirt and blouse set",
    "two-piece set", "cutout dress", "qipao", "cheongsam", "kaftan"
]

LINGERIE = [
    "lace bra", "lace panties", "corset", "pvc corset", "leather corset", "waspie",
    "satin bustier", "lace bodysuit", "fishnet bodysuit", "silk chemise", "garter belt", "suspender belt",
    "latex mini dress", "fishnet stockings", "thigh-high stockings", "satin blindfold", "nipple tassels", "pasties",
    "open-cup bra", "shelf bra", "cupless bra", "strappy cage bra", "micro bikini", "crotchless panty", "open-back thong",
    "lace teddy", "sheer bodysuit", "satin corset", "longline bralette", "underwire bra and thong set",
    "babydoll", "g-string", "sheer kimono robe", "lace-trim yukata lingerie", "merry widow", "negligee"
]

# ========================
# 3. 装飾・スタイル
# ========================
STYLES = [
    # Necklines
    "V-neck", "crew-neck", "scoop-neck", "boat-neck", "turtleneck", "high-neck", "halter", "sweetheart neckline", "plunge neckline", "cowl neck",
    # Sleeves
    "sleeveless", "short-sleeve", "long-sleeve", "cap-sleeve", "puffed-sleeve", "bell-sleeve", "raglan-sleeve", "kimono-sleeve", "bishop sleeve",
    # Fit & Cut
    "slim-fit", "loose-fit", "oversized", "A-line", "bodycon", "wrap-front", "peplum", "cropped", "high-waist", "low-rise", "empire waist", "draped", "ruched",
    # Hems & Slits
    "asymmetric hem", "high-low hem", "scalloped hem", "side-slit", "thigh-high slit", "front slit", "double slit",
    # Backs
    "open-back", "low-back", "lace-up back", "criss-cross back", "backless", "T-back",
    # Others
    "strapless", "one-shoulder", "off-the-shoulder", "cold-shoulder", "button-front", "zip-front", "underboob cutout", "cleavage cutout", "hip cutout"
]

EMBELLISH = [
    # Trims & Edges
    "lace trim", "ruffles", "frills", "fringe", "piping", "contrast trim", "scalloped edges", "feathers", "fur trim",
    # Add-ons
    "bows", "ribbons", "sequins", "pearls", "crystals", "rhinestones", "studs", "grommets", "beads", "metal hardware",
    # Fabric Manipulation
    "embroidery", "pleats", "pintucks", "smocking", "ruching", "quilting",
    # Cutouts & Panels
    "cutouts", "sheer panels", "mesh inserts", "lace panels", "slashed details",
    # Fastenings (can be decorative)
    "decorative buttons", "buckles", "zippers", "lace-up details", "hook-and-eye", "snap closure", "clasps",
    # Others
    "appliques", "patches", "tassels", "chain details", "body chains", "contrast stitching", "epaulettes"
]

# ========================
# 4. 露出表現・セクシー系アクセント
# ========================
ACCENTS_EROTIC = [
    "with garter straps", "with detachable garters", "with attached stockings",
    "with sheer gloves", "with a delicate choker", "with matching thong", "with lace-up back",
    "with open-crotch design", "with open-cup features", "with peekaboo panels", "with keyhole opening",
    "with O-ring details", "with metal rings", "with chain accents", "with delicate body chains",
    "with harness straps", "with bondage-style straps", "with lace-up sides", "with cutout hips", "with a plunging back",
    "held together by thin straps", "with strategic cutouts", "accented with pearls"
]

REVEAL_MILD = [
    "subtle sheer panels", "keyhole cutout", "low back", "shoulder cutouts", "back keyhole",
    "sheer sleeves", "a hint of sideboob", "modest cleavage", "slit on the leg", "off-shoulder revealing collarbones"
]
REVEAL_BOLD = [
    "see-through panels", "micro cutouts", "high-leg cut", "thong back", "deep plunge neckline",
    "cleavage window", "sideboob cutout", "underboob cutout", "hip cutouts", "backless design",
    "extremely short hemline", "navel cutout", "daringly high slit"
]
REVEAL_EXPLICIT = [
    "open sides", "sideboob cutouts", "barely-there straps", "ultra high-leg", "backless micro dress",
    "fully transparent", "cupless design", "crotchless design", "held by a single thread", "wardrobe malfunction",
    "nipple cutout", "completely sheer", "strategically placed rips", "unzipped front"
]

# ========================
# 5. 排他グループ
# ========================
EXCLUSIVE_GROUPS = {
    "season": {
        "summer": ["sundress", "linen", "bikini", "romper", "denim shorts", "tank top"],
        "winter": ["wool coat", "turtleneck sweater", "puffer jacket", "fleece", "cashmere knit", "corduroy"]
    },
    "garment_slot": {
        "full_body": DRESSES_SETS,
        "tops": TOPS,
        "bottoms": BOTTOMS
    }
}

# ========================
# 6. テーマパック (新しいカテゴリ構造に合わせて更新)
# ========================
THEMES = {
    "street": {
        "tops": ["oversized hoodie", "graphic tee", "crop top"],
        "outerwear": ["bomber jacket", "denim jacket", "windbreaker"],
        "bottoms": ["cargo pants", "biker shorts", "ripped jeans"],
        "materials": ["denim", "mesh", "fleece"],
        "styles": ["low-rise", "cropped", "oversized"],
    },
    "business": {
        "tops": ["silk blouse", "button-down shirt"],
        "outerwear": ["tailored blazer", "trench coat"],
        "bottoms": ["pencil skirt", "high-waist trousers"],
        "dresses_sets": ["pinstripe suit set", "blazer dress"],
        "patterns": ["pinstripe", "herringbone"],
        "materials": ["wool", "silk"],
        "styles": ["wrap-front", "slim-fit"],
    },
    "gothic": {
        "tops": ["lace blouse", "corset top", "velvet top"],
        "outerwear": ["velvet coat", "victorian style jacket"],
        "bottoms": ["long tiered skirt", "leather pants"],
        "dresses_sets": ["victorian goth dress", "velvet corset dress"],
        "materials": ["velvet", "lace", "leather", "brocade"],
        "patterns": ["damask", "cross motifs"],
        "styles": ["high-neck", "bell-sleeves", "lace-up details"],
    },
    "wasou": {
        "dresses_sets": ["yukata", "kimono", "hakama skirt set", "haori over camisole"],
        "lingerie": ["sheer kimono robe", "lace-trim yukata lingerie"],
        "materials": ["silk", "satin", "cotton"],
        "patterns": ["sakura", "asanoha", "seigaiha", "kikko", "floral"],
        "styles": ["kimono-sleeve", "wrap-front"],
    },
    "fantasy": {
        "dresses_sets": ["elven-inspired gown", "sorceress robe", "steampunk corset with skirt", "fairy dress"],
        "embellish": ["embroidered runes", "feathered cape", "jeweled details", "glowing patterns"],
        "materials": ["velvet", "brocade", "metallic fabric", "gossamer"],
        "patterns": ["celestial", "scale-like"],
    },
    "cyberpunk": {
        "tops": ["techwear crop top", "holographic tank top"],
        "outerwear": ["bomber jacket with LED", "transparent vinyl jacket"],
        "bottoms": ["cargo pants with straps", "techwear shorts"],
        "materials": ["PVC", "nylon", "holographic", "neoprene"],
        "embellish": ["buckles", "straps", "glowing piping", "cybernetic patterns"],
    },
    "swimsuits": {
        "lingerie": ["triangle string bikini", "high-cut monokini", "plunging one-piece", "lace-up two-piece", "bandeau bikini", "underwire bikini"],
        "dresses_sets": ["sporty zip-front rash guard set", "retro high-waist bikini"],
        "embellish": ["sheer mesh inserts", "cut-out sides", "O-ring details"],
        "materials": ["ribbed knit", "mesh", "spandex", "neoprene"],
    }
}

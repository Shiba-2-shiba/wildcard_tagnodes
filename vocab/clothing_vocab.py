"""Vocabulary definitions for clothing concept packs.

This module restructures the clothing vocabulary into themed concept packs so that
prompt generation can select cohesive outfits without creating contradictory
combinations (for example mixing a full dress with unrelated tops).
"""

from typing import Dict, List

# ---------------------------------------------------------------------------
# Shared pools
# ---------------------------------------------------------------------------
PALETTE_DEFAULT_PROBABILITIES: Dict[str, float] = {
    "colors": 0.9,
    "materials": 0.85,
    "patterns": 0.45,
    "styles": 0.7,
    "embellishments": 0.55,
}

OPTIONAL_DETAIL_PROBABILITY: float = 0.45
STATE_DETAIL_PROBABILITY: float = 0.3
OUTERWEAR_SELECTION_PROBABILITY: float = 0.25

STATE_TAGS: List[str] = [
    "wet",
    "rain-soaked",
    "damp",
    "water-splashed",
    "dripping wet",
    "wind-blown",
    "sun-bleached",
    "frozen",
    "covered in snow",
    "glowing",
    "shimmering",
]

EROTIC_ACCENTS: List[str] = [
    "with garter straps",
    "with detachable garters",
    "with attached stockings",
    "with sheer gloves",
    "with a delicate choker",
    "with matching thong",
    "with lace-up back",
    "with open-crotch design",
    "with peekaboo panels",
    "with keyhole opening",
    "with O-ring details",
    "with metal rings",
    "with chain accents",
    "with delicate body chains",
    "with harness straps",
    "with bondage-style straps",
    "with lace-up sides",
    "with cutout hips",
    "with a plunging back",
    "accented with pearls",
]

EXPOSURE_TAGS: Dict[str, List[str]] = {
    "mild": [
        "subtle sheer panels",
        "keyhole cutout",
        "low back",
        "shoulder cutouts",
        "back keyhole",
        "sheer sleeves",
        "a hint of sideboob",
        "modest cleavage",
        "slit on the leg",
        "off-shoulder revealing collarbones",
    ],
    "bold": [
        "see-through panels",
        "micro cutouts",
        "high-leg cut",
        "thong back",
        "deep plunge neckline",
        "cleavage window",
        "sideboob cutout",
        "underboob cutout",
        "hip cutouts",
        "backless design",
        "daringly high slit",
    ],
    "explicit": [
        "open sides",
        "barely-there straps",
        "ultra high-leg",
        "backless micro dress",
        "fully transparent",
        "cupless design",
        "crotchless design",
        "held by a single thread",
        "nipple cutout",
        "completely sheer",
        "strategically placed rips",
        "unzipped front",
    ],
}

# ---------------------------------------------------------------------------
# Concept packs
# ---------------------------------------------------------------------------
CONCEPT_PACKS: Dict[str, Dict[str, Dict[str, object]]] = {
    "dresses": {
        "romantic_garden_party": {
            "core": ["floral-print", "fit and flare dress"],
            "choices": {
                "dresses": ["sundress", "A-line dress"],
            },
            "palette": {
                "colors": ["soft pink", "white", "sky blue"],
                "materials": ["cotton", "chiffon", "linen"],
                "patterns": ["floral", "botanical"],
                "styles": ["sleeveless", "knee-length", "flowy silhouette"],
                "embellishments": ["lace trim", "ruffles", "belted waist"],
            },
            "optional_details": ["delicate waist ribbon", "matching sun hat"],
            "states": [],
        },
        "executive_pencil_dress": {
            "core": ["tailored fit", "sleek silhouette"],
            "choices": {
                "dresses": ["sheath dress", "bodycon dress"],
            },
            "palette": {
                "colors": ["navy blue", "charcoal", "wine"],
                "materials": ["wool", "stretch cotton", "silk blend"],
                "patterns": ["solid", "pinstripe"],
                "styles": ["knee-length", "cap-sleeve", "high-neck"],
                "embellishments": ["waist belt", "covered buttons"],
            },
            "optional_details": ["minimalist jewelry accent", "structured peplum"],
        },
        "boho_maxi_dress": {
            "core": ["bohemian", "flowing layers"],
            "choices": {
                "dresses": ["maxi dress", "wrap dress"],
            },
            "palette": {
                "colors": ["earthy brown", "sage green", "sunset orange"],
                "materials": ["cotton", "gauze", "silk"],
                "patterns": ["paisley", "floral", "tie-dye"],
                "styles": ["long-sleeve", "wrap-front", "tiered hem"],
                "embellishments": ["fringe", "tassels", "embroidery"],
            },
            "optional_details": ["layered necklaces", "wide waist sash"],
        },
        "sleek_evening_gown": {
            "core": ["elegant evening", "floor-length"],
            "choices": {
                "dresses": ["evening gown", "little black dress"],
            },
            "palette": {
                "colors": ["black", "deep crimson", "emerald"],
                "materials": ["silk", "velvet", "satin"],
                "patterns": ["solid", "ombre"],
                "styles": ["backless", "thigh-high slit", "mermaid silhouette"],
                "embellishments": ["sequins", "crystals", "beaded straps"],
            },
            "optional_details": ["opera gloves", "draped shawl"],
            "exposure_bias": "bold",
        },
        "cyberpunk_bodycon_dress": {
            "core": ["futuristic", "techwear accents"],
            "choices": {
                "dresses": ["bodycon dress", "techwear mini dress"],
            },
            "palette": {
                "colors": ["black", "electric blue", "neon magenta"],
                "materials": ["PVC", "latex", "neoprene"],
                "patterns": ["geometric-pattern", "circuit motif"],
                "styles": ["high-neck", "cutout panels", "asymmetric hem"],
                "embellishments": ["glowing piping", "buckles", "metal hardware"],
            },
            "optional_details": ["holographic visor", "fingerless gloves"],
            "exposure_bias": "bold",
        },
        "victorian_gothic_dress": {
            "core": ["victorian goth", "layered lace"],
            "choices": {
                "dresses": ["babydoll dress", "gothic lolita dress"],
            },
            "palette": {
                "colors": ["jet black", "wine", "ivory"],
                "materials": ["velvet", "lace", "cotton"],
                "patterns": ["baroque", "damask"],
                "styles": ["long-sleeve", "high-neck", "tiered skirt"],
                "embellishments": ["lace trim", "bows", "ruffles"],
            },
            "optional_details": ["lace gloves", "mini top hat"],
        },
        "winter_knit_dress": {
            "core": ["cozy knit", "winter date"],
            "choices": {
                "dresses": ["sweater dress", "turtleneck sweater dress"],
            },
            "palette": {
                "colors": ["cream", "dusty rose", "soft gray"],
                "materials": ["wool", "cashmere", "fleece"],
                "patterns": ["fair isle", "solid"],
                "styles": ["long-sleeve", "fitted silhouette", "knee-length"],
                "embellishments": ["cable knit texture", "knit belt"],
            },
            "optional_details": ["cozy scarf", "fuzzy leg warmers"],
            "states": ["covered in snow"],
        },
        "traditional_kimono_dress": {
            "core": ["kimono", "obi sash"],
            "choices": {
                "dresses": ["kimono", "yukata", "furisode"],
            },
            "palette": {
                "colors": ["crimson", "indigo", "soft gold"],
                "materials": ["silk", "satin", "cotton"],
                "patterns": ["cherry-blossom-print", "asanoha", "seigaiha"],
                "styles": ["long-sleeve", "floor-length", "layered"],
                "embellishments": ["embroidery", "obijime cord", "kanzashi adornment"],
            },
            "optional_details": ["floral hair ornament", "tabi socks"],
        },
        "athletic_bodysuit": {
            "core": ["performance wear", "streamlined"],
            "choices": {
                "dresses": ["bodysuit", "unitard"],
            },
            "palette": {
                "colors": ["slate gray", "cerulean", "white"],
                "materials": ["spandex", "nylon", "lycra"],
                "patterns": ["color-block", "gradient"],
                "styles": ["zip-front", "thumb holes", "panelled"],
                "embellishments": ["reflective piping", "mesh inserts"],
            },
            "optional_details": ["supportive sports belt", "performance gloves"],
            "exposure_bias": "mild",
        },
        "arcane_battle_dress": {
            "core": ["fantasy battle", "armored bodice"],
            "choices": {
                "dresses": ["armored gown", "battle mage robe"],
            },
            "palette": {
                "colors": ["midnight blue", "gunmetal", "amethyst"],
                "materials": ["leather", "metal", "brocade"],
                "patterns": ["arcane sigils", "geometric-pattern"],
                "styles": ["structured skirt", "high slit", "layered plates"],
                "embellishments": ["studs", "engraved plates", "chainmail trim"],
            },
            "optional_details": ["spell scroll belt", "pauldron accents"],
        },
    },
    "separates": {
        "modern_office_attire": {
            "core": ["professional ensemble"],
            "choices": {
                "tops": [["silk blouse", "long-sleeve"], ["button-down shirt", "tucked in"], ["knit top", "fitted"]],
                "bottoms": [["pencil skirt", "high-waist"], ["tailored trousers", "pressed creases"]],
            },
            "palette": {
                "colors": ["ivory", "charcoal", "navy blue"],
                "materials": ["silk", "cotton", "wool"],
                "patterns": ["solid", "pinstripe"],
                "styles": ["waist-cinched", "knee-length", "structured"],
                "embellishments": ["waist belt", "minimalist buttons"],
            },
            "optional_details": ["delicate neck scarf", "minimal jewelry"],
        },
        "street_denim_layer": {
            "core": ["street fashion", "layered casual"],
            "choices": {
                "tops": [["graphic tee", "oversized"], ["cropped hoodie", "drawstring"], ["tank top", "layered under jacket"]],
                "bottoms": [["ripped jeans"], ["denim shorts", "distressed hem"], ["cargo pants", "strap details"]],
            },
            "palette": {
                "colors": ["black", "ash gray", "electric blue"],
                "materials": ["denim", "cotton", "mesh"],
                "patterns": ["graphic print", "striped"],
                "styles": ["relaxed fit", "high-waist", "cropped"],
                "embellishments": ["zippers", "buckles", "contrast stitching"],
            },
            "optional_details": ["layered chains", "fingerless gloves"],
        },
        "preppy_school_uniform": {
            "core": ["school uniform", "neat pleats"],
            "choices": {
                "tops": [["sailor blouse", "ribbon tie"], ["button-down shirt", "cardigan overlay"]],
                "bottoms": [["pleated skirt"], ["plaid skirt"]],
            },
            "palette": {
                "colors": ["navy", "white", "burgundy"],
                "materials": ["cotton", "wool blend"],
                "patterns": ["plaid", "solid"],
                "styles": ["long-sleeve", "pleated", "collared"],
                "embellishments": ["ribbons", "decorative buttons", "badge emblem"],
            },
            "optional_details": ["knee-high socks", "school satchel"],
        },
        "athleisure_training_set": {
            "core": ["training set", "sporty"],
            "choices": {
                "tops": [["sports bra", "supportive straps"], ["tank top", "breathable mesh"]],
                "bottoms": [["leggings", "high-waist"], ["biker shorts", "compression fit"], ["yoga pants", "panelled"]],
            },
            "palette": {
                "colors": ["black", "teal", "coral"],
                "materials": ["spandex", "nylon", "jersey"],
                "patterns": ["color-block", "ombre"],
                "styles": ["bodycon", "crop length", "supportive waistband"],
                "embellishments": ["mesh inserts", "reflective piping"],
            },
            "optional_details": ["sweatband", "sports smartwatch"],
            "exposure_bias": "mild",
        },
        "punk_rock_stagewear": {
            "core": ["stage ready", "edgy"],
            "choices": {
                "tops": [["mesh top", "strappy"], ["band t-shirt", "cropped"], ["corset top", "lace-up front"]],
                "bottoms": [["leather pants", "skin-tight"], ["mini skirt", "studded belt"]],
            },
            "palette": {
                "colors": ["black", "scarlet", "metallic"],
                "materials": ["leather", "PVC", "mesh"],
                "patterns": ["solid", "grunge print"],
                "styles": ["bodycon", "high-waist", "asymmetric hem"],
                "embellishments": ["studs", "chains", "zippers"],
            },
            "optional_details": ["fishnet stockings", "choker necklace"],
            "exposure_bias": "bold",
        },
        "gothic_lolita_coord": {
            "core": ["layered lolita", "sweet goth"],
            "choices": {
                "tops": [["lace blouse", "puffed-sleeve"], ["high-neck blouse", "ruffled collar"]],
                "bottoms": [["tiered skirt", "petticoat"]],
            },
            "palette": {
                "colors": ["black", "wine", "cream"],
                "materials": ["lace", "velvet", "cotton"],
                "patterns": ["baroque", "floral"] ,
                "styles": ["long-sleeve", "corseted waist", "layered"],
                "embellishments": ["bows", "lace trim", "frills"],
            },
            "optional_details": ["bonnet headpiece", "lace parasol"],
        },
        "beach_resort_coord": {
            "core": ["resort wear", "breezy layers"],
            "choices": {
                "tops": [["off-the-shoulder top", "ruffled"], ["bandeau top", "twist front"], ["light camisole", "flowy"]],
                "bottoms": [["wrap skirt", "side slit"], ["linen shorts", "tie waist"]],
            },
            "palette": {
                "colors": ["turquoise", "white", "sunny yellow"],
                "materials": ["linen", "cotton", "chiffon"],
                "patterns": ["tropical-print", "floral", "gradient"],
                "styles": ["lightweight", "high-low hem", "off-the-shoulder"],
                "embellishments": ["shell accents", "beaded tassels"],
            },
            "optional_details": ["wide-brim hat", "ankle bracelet"],
            "states": ["sun-kissed glow"],
        },
        "winter_layered_knit": {
            "core": ["layered knitwear", "cozy"],
            "choices": {
                "tops": [["turtleneck sweater", "chunky knit"], ["cashmere knit", "long-sleeve"]],
                "bottoms": [["wool trousers", "pleated front"], ["thermal leggings", "lined"]],
            },
            "palette": {
                "colors": ["cream", "dusty mauve", "forest green"],
                "materials": ["wool", "cashmere", "fleece"],
                "patterns": ["solid", "fair isle"],
                "styles": ["relaxed fit", "layered", "tucked"],
                "embellishments": ["cable knit texture", "faux fur trim"],
            },
            "optional_details": ["knit mittens", "wool beret"],
            "states": ["covered in snow"],
        },
        "fantasy_battle_armor": {
            "core": ["armored elegance", "battle ready"],
            "choices": {
                "tops": [["corset top", "reinforced plates"], ["leather bustier", "strapped"]],
                "bottoms": [["armored skirt", "layered plates"], ["leather pants", "buckled"]],
            },
            "palette": {
                "colors": ["steel", "midnight blue", "crimson"],
                "materials": ["leather", "metal", "brocade"],
                "patterns": ["geometric-pattern", "engraved runes"],
                "styles": ["cinched waist", "high slit", "structured panels"],
                "embellishments": ["studs", "buckles", "chainmail trim"],
            },
            "optional_details": ["armored gauntlets", "battle cloak"],
        },
        "secret_agent_suit": {
            "core": ["sleek agent", "stealthy"],
            "choices": {
                "tops": [["tailored bodysuit", "zip-front"], ["silk blouse", "hidden placket"]],
                "bottoms": [["tailored trousers", "ankle-slit"], ["sleek pencil skirt", "side slit"]],
            },
            "palette": {
                "colors": ["black", "graphite", "deep navy"],
                "materials": ["stretch twill", "silk", "neoprene"],
                "patterns": ["solid", "subtle herringbone"],
                "styles": ["bodycon", "high slit", "structured"],
                "embellishments": ["concealed holster harness", "minimalist belt"],
            },
            "optional_details": ["glossy gloves", "earpiece"],
            "exposure_bias": "bold",
        },
        "rainy_day_layers": {
            "core": ["weather ready", "layered"],
            "choices": {
                "tops": [["turtleneck sweater", "cozy"], ["long-sleeve tee", "layered"], ["lightweight sweater", "ribbed"]],
                "bottoms": [["jeans", "ankle crop"], ["tailored trousers", "water resistant"]],
            },
            "palette": {
                "colors": ["charcoal", "navy", "olive"],
                "materials": ["cotton", "wool blend", "technical fabric"],
                "patterns": ["solid", "pinstripe"],
                "styles": ["layered", "ankle-length", "high-waist"],
                "embellishments": ["storm flap", "sealed seams"],
            },
            "optional_details": ["cozy scarf", "weatherproof boots"],
            "states": ["rain-soaked"],
            "outerwear_hint": "rainproof_trench",
        },
        "solarpunk_breeze": {
            "core": ["solarpunk", "organic silhouettes"],
            "choices": {
                "tops": [["sleeveless tunic", "draped"], ["wrap top", "asymmetric hem"]],
                "bottoms": [["pleated skirt", "lightweight"], ["wide-leg pants", "flowing panels"]],
            },
            "palette": {
                "colors": ["mint green", "sunlit gold", "off-white"],
                "materials": ["bamboo fabric", "cotton", "silk"],
                "patterns": ["botanical", "geometric-pattern"],
                "styles": ["flowy", "high-waist", "layered"],
                "embellishments": ["embroidery", "beads", "leafy appliques"],
            },
            "optional_details": ["bioluminescent accents", "seed pod jewelry"],
        },
    },
    "outerwear": {
        "tailored_blazer": {
            "core": ["structured blazer"],
            "choices": {
                "outerwear": ["blazer", "longline blazer"],
            },
            "palette": {
                "colors": ["charcoal", "camel", "navy"],
                "materials": ["wool", "tweed", "cotton blend"],
                "styles": ["waist-cinched", "double-breasted", "sleek lapels"],
                "embellishments": ["padded shoulders", "polished buttons"],
            },
            "optional_details": ["pocket square", "skinny belt"],
        },
        "cozy_wool_coat": {
            "core": ["warm outerwear"],
            "choices": {
                "outerwear": ["wool coat", "duffle coat", "puffer jacket"],
            },
            "palette": {
                "colors": ["cream", "burgundy", "forest green"],
                "materials": ["wool", "cashmere", "faux fur"],
                "styles": ["longline", "hooded", "wrap-front"],
                "embellishments": ["toggle closures", "faux fur trim"]
            },
            "optional_details": ["knit scarf", "cozy earmuffs"],
        },
        "edgy_biker_jacket": {
            "core": ["biker jacket", "edgy layer"],
            "choices": {
                "outerwear": ["leather jacket", "biker jacket", "moto jacket"],
            },
            "palette": {
                "colors": ["black", "charcoal", "oxblood"],
                "materials": ["leather", "faux leather", "suede"],
                "styles": ["cropped", "asymmetric zipper", "fitted"],
                "embellishments": ["studs", "zip hardware", "buckled straps"],
            },
            "optional_details": ["shoulder spikes", "chain epaulettes"],
        },
        "techwear_translucent_parka": {
            "core": ["techwear parka", "futuristic"],
            "choices": {
                "outerwear": ["transparent vinyl jacket", "bomber jacket with LED", "anorak"],
            },
            "palette": {
                "colors": ["transparent", "holographic", "electric blue"],
                "materials": ["PVC", "nylon", "neoprene"],
                "styles": ["hooded", "oversized", "modular"],
                "embellishments": ["glowing piping", "utility straps", "zippered pockets"],
            },
            "optional_details": ["tech visor", "cybernetic armband"],
        },
        "romantic_lace_shawl": {
            "core": ["delicate cover-up"],
            "choices": {
                "outerwear": ["lace shawl", "sheer cape", "bolero"],
            },
            "palette": {
                "colors": ["ivory", "blush", "lavender"],
                "materials": ["lace", "tulle", "chiffon"],
                "styles": ["shoulder drape", "open-front", "short-sleeve"],
                "embellishments": ["lace trim", "scalloped edges", "pearls"],
            },
            "optional_details": ["delicate brooch", "floral corsage"],
        },
        "sporty_track_jacket": {
            "core": ["athletic layer"],
            "choices": {
                "outerwear": ["track jacket", "windbreaker"],
            },
            "palette": {
                "colors": ["white", "teal", "coral"],
                "materials": ["nylon", "polyester", "spandex"],
                "styles": ["zip-front", "stand collar", "cropped"],
                "embellishments": ["reflective stripes", "contrast piping"],
            },
            "optional_details": ["thumb hole cuffs", "hood hidden in collar"],
        },
        "armored_cloak": {
            "core": ["battle cloak"],
            "choices": {
                "outerwear": ["cape", "armored vest", "hooded cloak"],
            },
            "palette": {
                "colors": ["black", "midnight blue", "bronze"],
                "materials": ["leather", "brocade", "metal"],
                "styles": ["floor-length", "hooded", "shoulder plating"],
                "embellishments": ["engraved clasps", "chainmail edging"],
            },
            "optional_details": ["sigil brooch", "fur-lined collar"],
        },
        "rainproof_trench": {
            "core": ["raincoat", "weather shield"],
            "choices": {
                "outerwear": ["trench coat", "raincoat"],
            },
            "palette": {
                "colors": ["charcoal", "navy", "olive"],
                "materials": ["waterproof fabric", "coated cotton"],
                "styles": ["belted", "storm flap", "hooded"],
                "embellishments": ["sealed seams", "epaulettes"],
            },
            "optional_details": ["transparent umbrella", "waterproof bag"],
        },
        "kimono_haori": {
            "core": ["haori jacket"],
            "choices": {
                "outerwear": ["haori", "kimono jacket"],
            },
            "palette": {
                "colors": ["indigo", "vermillion", "cream"],
                "materials": ["silk", "cotton", "brocade"],
                "styles": ["three-quarter sleeve", "open-front", "patterned lining"],
                "embellishments": ["embroidered crest", "woven sash"],
            },
            "optional_details": ["sensu fan", "obi-inspired belt"],
        },
    },
}

# ---------------------------------------------------------------------------
# Theme mapping (UI compatibility)
# ---------------------------------------------------------------------------
THEME_TO_PACKS: Dict[str, Dict[str, List[str]]] = {
    "office_lady": {
        "dresses": ["executive_pencil_dress"],
        "separates": ["modern_office_attire"],
        "outerwear": ["tailored_blazer"],
    },
    "beach_resort": {
        "dresses": ["romantic_garden_party", "boho_maxi_dress"],
        "separates": ["beach_resort_coord"],
        "outerwear": ["romantic_lace_shawl"],
    },
    "rainy_day": {
        "dresses": ["winter_knit_dress"],
        "separates": ["rainy_day_layers"],
        "outerwear": ["rainproof_trench", "cozy_wool_coat"],
    },
    "fantasy_battle": {
        "dresses": ["arcane_battle_dress"],
        "separates": ["fantasy_battle_armor"],
        "outerwear": ["armored_cloak"],
    },
    "cyberpunk_night": {
        "dresses": ["cyberpunk_bodycon_dress"],
        "separates": ["street_denim_layer"],
        "outerwear": ["techwear_translucent_parka"],
    },
    "traditional_japanese": {
        "dresses": ["traditional_kimono_dress"],
        "separates": ["solarpunk_breeze"],
        "outerwear": ["kimono_haori"],
    },
    "school_uniform": {
        "dresses": ["romantic_garden_party"],
        "separates": ["preppy_school_uniform"],
        "outerwear": ["tailored_blazer"],
    },
    "gothic_lolita": {
        "dresses": ["victorian_gothic_dress"],
        "separates": ["gothic_lolita_coord"],
        "outerwear": ["romantic_lace_shawl"],
    },
    "rock_concert": {
        "dresses": ["sleek_evening_gown", "cyberpunk_bodycon_dress"],
        "separates": ["punk_rock_stagewear"],
        "outerwear": ["edgy_biker_jacket"],
    },
    "winter_date": {
        "dresses": ["winter_knit_dress"],
        "separates": ["winter_layered_knit"],
        "outerwear": ["cozy_wool_coat"],
    },
    "secret_agent": {
        "dresses": ["sleek_evening_gown", "athletic_bodysuit"],
        "separates": ["secret_agent_suit"],
        "outerwear": ["tailored_blazer", "rainproof_trench"],
    },
    "gym_workout": {
        "dresses": ["athletic_bodysuit"],
        "separates": ["athleisure_training_set"],
        "outerwear": ["sporty_track_jacket"],
    },
}

THEME_CHOICES: List[str] = ["none"] + sorted(list(THEME_TO_PACKS.keys()))

__all__ = [
    "CONCEPT_PACKS",
    "THEME_TO_PACKS",
    "THEME_CHOICES",
    "EXPOSURE_TAGS",
    "EROTIC_ACCENTS",
    "STATE_TAGS",
    "PALETTE_DEFAULT_PROBABILITIES",
    "OPTIONAL_DETAIL_PROBABILITY",
    "STATE_DETAIL_PROBABILITY",
    "OUTERWEAR_SELECTION_PROBABILITY",
]

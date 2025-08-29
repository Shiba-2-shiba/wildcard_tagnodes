# accessory_vocab.py (改善版)
# 語彙リスト: アクセサリータグ生成ノード用

# 1. 各カテゴリの語彙を大幅に拡充
HEADWEAR = [
    "wide-brim hat", "beanie", "beret", "headband", "tiara", "hood", "baseball cap", 
    "flower crown", "fedora", "top hat", "sun visor", "sailor hat", "witch hat", 
    "pirate hat", "nurse cap", "headscarf", "bandana", "ushanka", "deerstalker cap",
    "garrison cap", "crown", "helmet", "circlet", "hairpin", "hair ribbon", "veil"
]

EYEWEAR = [
    "glasses", "sunglasses", "monocle", "eye patch", "goggles", "reading glasses",
    "aviator sunglasses", "heart-shaped sunglasses", "cyberpunk goggles", "steampunk goggles",
    "3d glasses", "blindfold"
]

EARRINGS = [
    "earrings", "stud earrings", "hoop earrings", "dangle earrings", "ear cuff", 
    "tassel earrings", "pearl earrings", "diamond earrings"
]

NECKLACES = [
    "necklace", "choker", "pendant", "locket", "chain", "beaded necklace", 
    "pearl necklace", "amulet", "dog tag", "bolo tie"
]

# 腕や手のアクセサリーカテゴリを追加
HAND_ACCESSORIES = [
    "bracelet", "ring", "anklet", "bangle", "cuff bracelet", "watch", 
    "fingerless gloves", "gloves", "armlet", "gauntlet"
]

# その他のアクセサリーカテゴリを追加
OTHER_ACCESSORIES = [
    "brooch", "scarf", "tie", "bowtie", "belt", "sash", "shoulder armor", "cape",
    "backpack", "crossbody bag", "tote bag", "pouch", "wings"
]

HANDHELD = [
    "hand fan", "parasol", "book", "smartphone", "coffee cup", "sword", "staff", 
    "umbrella", "wand", "lantern", "camera", "briefcase", "guitar", "bouquet",
    "crystal ball", "revolver", "dagger", "shield", "flag"
]

# 2. テーマパックを導入
# 特定のスタイルやテーマに沿ったタグの組み合わせを定義
THEME_PACKS = {
    "casual": ["baseball cap", "sunglasses", "backpack", "smartphone", "watch"],
    "fantasy": ["tiara", "amulet", "staff", "cape", "gauntlet", "wings", "sword"],
    "formal": ["top hat", "monocle", "pearl necklace", "gloves", "briefcase", "bowtie"],
    "steampunk": ["steampunk goggles", "top hat", "pocket watch", "gears", "leather belt"],
    "gothic": ["choker", "veil", "dark jewelry", "black roses", "silver cross"],
}

# 3. 排他的なタググループを導入
# 同時に出現させたくないタグをグループ化
# 例: "glasses"が選ばれたら、同じグループの"sunglasses"や"blindfold"は選ばれなくなる
EXCLUSIVE_TAG_GROUPS = {
    "eyewear_type": ["glasses", "sunglasses", "monocle", "goggles", "blindfold"],
    "hat_type": ["wide-brim hat", "beanie", "beret", "baseball cap", "fedora", "top hat"],
    "weapon_type": ["sword", "dagger", "revolver", "staff", "wand"],
}

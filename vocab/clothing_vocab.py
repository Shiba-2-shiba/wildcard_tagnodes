# vocab.py
# clothing_tagノードで使用する語彙リスト

# ========================
# コア語彙（共通）
# ========================
COLORS = [
    "black","white","ivory","cream","silver","gold","champagne",
    "red","crimson","scarlet","wine","burgundy",
    "pink","blush","rose","magenta",
    "purple","lavender","violet","plum",
    "blue","navy","cobalt","turquoise","teal",
    "green","emerald","olive","mint",
    "brown","chocolate","tan","beige",
    "gray","charcoal","graphite","transparent","clear"
]
MATERIALS = [
    "lace","satin","silk","velvet","latex","PVC","mesh","tulle",
    "chiffon","fishnet","leather","patent leather","faux leather",
    "organza","ribbed knit","micro-mesh","crepe","linen","denim","wool blend","brocade"
]
PATTERNS = [
    "floral","paisley","polka-dot","striped","zebra-print",
    "leopard-print","snake-print","grid","herringbone",
    "chevron","heart-pattern","checked","argyle","gingham","pinstripe","tartan"
]
STYLES = [
    "halter","strapless","off-shoulder","one-shoulder",
    "plunge neckline","sweetheart neckline","high-neck",
    "open back","low-back","side-slit","thigh-slit",
    "high-waist","low-rise","micro-length","wrap-front",
    "lace-up front","lace-up sides","zip-back","buttoned front","asymmetric hem"
]
CLOSURES = [
    "front lace-up","back lace-up","side zipper","back zipper",
    "buckle straps","hook-and-eye","tie-back","snap closure"
]
EMBELLISH = [
    "embroidery","sequins","pearls","crystals","studs","gems",
    "bows","fringe","ribbons","ruffles","lace trim",
    "scalloped edges","sheer panels","cutouts","piping","contrast piping"
]
BASES_EROTIC = [
    "lace bra","lace panties","corset dress","corset top","pvc corset","leather corset",
    "satin bustier","lace bodysuit","fishnet bodysuit","silk chemise","garter belt",
    "latex mini dress","fishnet stockings","satin blindfold","nipple tassels","pasties",
    "open-cup bra","strappy cage bra","micro bikini","crotchless panty","open-back thong",
]
ACCENTS_EROTIC = [
    "with garter straps","with detachable garters","with attached stockings",
    "with sheer gloves","with choker","with matching thong",
    "with open-crotch","with open-cup","with peekaboo panels",
    "with O-ring details","with metal rings","with chain accents",
    "with harness straps","with lace-up sides","with cutout hips"
]
BASES_NONEROTIC = [
    "A-line sundress","wrap dress","pleated skirt with blouse","tailored blazer set",
    "silk camisole and cardigan","turtleneck knit and skirt","denim jacket and tee",
    "linen jumpsuit","maxi dress with slit","shirt dress with belt",
    "sweater and pleated midi","blazer and tailored trousers","crop top and high-waist jeans",
]
ACCENTS_NONEROTIC = [
    "with waist belt","with matching cardigan","with scarf","with layered necklace",
    "with tote bag","with ankle boots","with mary janes","with knee-high socks",
]
REVEAL_MILD = ["subtle sheer panels","keyhole cutout","low back"]
REVEAL_BOLD = ["see-through panels","micro cutouts","high-leg cut","thong back","deep plunge"]
REVEAL_EXPLICIT = ["open sides","sideboob cutouts","barely-there straps","ultra high-leg","backless micro"]

# ========================
# テーマパック
# ========================
THEMES = {
    "lingerie": {"bases_erotic": ["lace teddy","sheer bodysuit","satin corset","longline bralette","underwire bra and thong set","babydoll set","g-string set",],"accents_erotic": ["with garter belt","with lace thigh-highs","with silk robe"],"materials": ["mesh","silk","satin","lace","tulle"],},
    "erotic_boost": {"bases_erotic": ["latex corset","pasties and thong","open-cup corset","strappy bondage set"],"accents_erotic": ["with collar and leash","with handcuffs","with harness"],"materials": ["latex","PVC","leather"],},
    "dresses": {"bases_non": ["little black dress","wrap-front midi dress","fit and flare dress","slip dress with lace trim","shirt dress","pleated A-line dress","one-shoulder bodycon dress",],"patterns": ["polka-dot","floral","geometric"],"styles": ["off-shoulder","halter","sweetheart neckline"],},
    "swimsuits": {"bases_erotic": ["triangle string bikini","high-cut monokini","plunging one-piece","lace-up two-piece"],"bases_non": ["sporty zip-front rash guard set","retro high-waist bikini"],"accents_erotic": ["with sheer mesh inserts","with cut-out sides"],"materials": ["ribbed knit","mesh"],},
    "sets": {"bases_non": ["pleated skirt and blouse set","paperbag pants with ribbed knit top","peplum blazer and pencil skirt","cargo pants and tank top","jumpsuit set",]},
    "tops": {"bases_non": ["corset top with high-waist trousers","halter neck top with maxi skirt","wrap-front blouse with culottes","kimono top with jeans",],"styles": ["lace-up front","off-shoulder","asymmetrical hem","wrap-front"],},
    "fantasy": {"bases_non": ["elven-inspired gown","sorceress robe","steampunk corset with skirt"],"accents_non": ["with embroidered runes","with feathered cape","with jeweled tiara"],"materials": ["velvet","brocade","metallic fabric"],"patterns": ["celestial","scale-like"],},
    "christmas": {"bases_non": ["red sweater and plaid skirt","velvet green dress","fair isle sweater dress"],"accents_non": ["with faux fur trim","with santa hat","with reindeer motif"],"patterns": ["plaid","candy-cane stripe","snowflake"],"materials": ["velvet","knit"],},
    "wasou": {"bases_non": ["yukata with obi sash","kimono-style wrap dress","hakama skirt set","haori over camisole"],"bases_erotic": ["sheer kimono robe","lace-trim yukata lingerie","obi belt with satin chemise"],"accents_non": ["with obi-jime cord","with sensu fan","with tabi socks"],"accents_erotic": ["with silk obi loosely tied","with sheer juban layer"],"materials": ["silk","satin","washi-like weave"],"patterns": ["sakura","asanoha","seigaiha","kikkō"],"styles": ["kimono sleeves","overlapping front"],},
    "uniform": {"bases_non": ["sailor blouse and pleated skirt","blazer uniform set","shirt and tie with skirt"],"bases_erotic": ["cropped sailor top and micro skirt","tight shirt with ultra mini skirt"],"accents_non": ["with ribbon tie","with knee-high socks","with loafers"],"accents_erotic": ["with unbuttoned top","with loosened tie"],"patterns": ["pinstripe","plaid"],"materials": ["poly-blend","knit"],},
    "street": {"bases_non": ["oversized hoodie with biker shorts","crop hoodie and cargo pants","denim jacket and graphic tee","bomber jacket and mini skirt","tracksuit set"],"bases_erotic": ["mesh crop top and micro shorts","strap bralette and low-rise cargo"],"accents_non": ["with baseball cap","with chunky sneakers","with crossbody bag"],"materials": ["denim","mesh","ribbed knit"],"styles": ["low-rise","cropped","asymmetric hem"],},
    "business": {"bases_non": ["tailored blazer with pencil skirt","pinstripe suit set","silk blouse with high-waist trousers"],"bases_erotic": ["deep-plunge blazer dress","sheer blouse with bra top"],"accents_non": ["with leather tote","with pumps","with thin belt"],"patterns": ["pinstripe","herringbone"],"materials": ["wool blend","silk"],"styles": ["wrap-front","structured shoulders"],},
    "gothic": {"bases_non": ["velvet corset with long skirt","lace blouse and tiered skirt","victorian goth dress"],"bases_erotic": ["sheer lace gothic bodysuit","latex corset with mesh skirt"],"accents_non": ["with choker","with lace gloves","with fishnet tights"],"materials": ["velvet","lace","leather"],"patterns": ["brocade","cross motifs"],"styles": ["high-neck","bell sleeves"],},
    "lolita": {"bases_non": ["sweet lolita dress","classic lolita set","gothic lolita OP"],"bases_erotic": ["mini puff-sleeve babydoll","sheer apron lolita"],"accents_non": ["with petticoat","with headdress","with ribbon bows"],"materials": ["cotton","lace","organza"],"patterns": ["polka-dot","rose bouquet","gingham"],"styles": ["peter pan collar","ruffled hem"],},
}

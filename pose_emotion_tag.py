# pose_emotion_tag.py (統合・修正版)
# 元の詳細なUI・確率調整機能と、新しい3段階NSFWモード・フィルタリング機能を統合

from typing import Dict, List, Set
import re
from .util import rng_from_seed, maybe, pick, join_clean, limit_len, normalize, merge_unique
from .vocab.pose_emotion_vocab import (
    POSE_MODES, EXPRESSION_MODES,
    HAND_PLACEMENT, LEG_POSITION, SPINE_SHOULDER, CAMERA_FRAMING, INTERACTION,
    LID_STATE, EYE_GAZE, MOUTH_ACTION, BLUSH, SWEAT, TEAR, MICRO_EXP,
    THEME_PACKS,
    NSFW_SUGGESTIVE_HAND, NSFW_SUGGESTIVE_LEG, NSFW_SUGGESTIVE_SPINE,
    NSFW_SUGGESTIVE_CAMERA, NSFW_SUGGESTIVE_INTER,
    NSFW_SUGGESTIVE_MOUTH, NSFW_SUGGESTIVE_EYES, NSFW_SUGGESTIVE_MOOD,
    NSFW_SUGGESTIVE_BLUSH, NSFW_SUGGESTIVE_SWEAT, NSFW_SUGGESTIVE_MICRO,
    EXTRA_NSFW_POSE, EXTRA_NSFW_EXPR,
    EXPLICIT_BLOCKLIST,
)

# ===== 日本語UIマップ =====
POSE_MODE_JP = {"日常":"daily","アクション":"action","ファッション":"fashion","グラビア":"gravure"}
EXPR_MODE_JP = {"日常":"daily","魅惑":"allure","キュート":"cute","クール":"cool"}
COMPLEXITY_JP = {"とても単純":"very_simple","単純":"simple","標準":"normal","複雑":"elaborate","とても複雑":"complex"}
INTENSITY_JP = {"とても控えめ":"very_subtle","控えめ":"subtle","普通":"normal","豊か":"rich","過剰":"over"}
# explicitモードを追加
NSFW_JP = {"オフ":"off","アダルト寄り(非露骨)":"suggestive","アダルト(露骨フィルタ)":"explicit"}

# ===== 確率プロファイル関数 =====
def _complexity_profile(level:str)->Dict[str,float]:
    base = dict(view=.8, motion=.6, props=.5, hand=.6, leg=.6, spine=.6, camera=.7, inter=.5)
    if level=="very_simple": base.update(view=.4,motion=.15,props=.1,hand=.15,leg=.15,spine=.25,camera=.4,inter=.1)
    elif level=="simple":    base.update(view=.55,motion=.3, props=.2,hand=.3, leg=.3, spine=.4, camera=.55,inter=.2)
    elif level=="elaborate": base.update(view=.9, motion=.8, props=.75,hand=.8, leg=.8, spine=.85,camera=.9, inter=.7)
    elif level=="complex":   base.update(view=.95,motion=.9, props=.85,hand=.9, leg=.9, spine=.95,camera=.95,inter=.85)
    return base

def _intensity_profile(level:str)->Dict[str,float]:
    base = dict(mouth=1.0, eyes=1.0, brow=.6, mood=.7, lid=.7, gaze=.7, micro=.5, blush=.5, sweat=.3, tear=.3)
    if level=="very_subtle": base.update(brow=.25,mood=.3,lid=.3,gaze=.3,micro=.2,blush=.2,sweat=.1,tear=.1)
    elif level=="subtle":    base.update(brow=.4, mood=.45,lid=.5,gaze=.5,micro=.35,blush=.35,sweat=.2,tear=.2)
    elif level=="rich":      base.update(brow=.8, mood=.95,lid=.85,gaze=.85,micro=.7, blush=.7, sweat=.45,tear=.45)
    elif level=="over":      base.update(brow=.9, mood=1.0,lid=.95,gaze=.95,micro=.85,blush=.85,sweat=.6, tear=.6)
    return base

# ===== 語彙プール準備関数 =====
def _prepare_pose_lists(mode:str)->Dict[str,List[str]]:
    M = POSE_MODES.get(mode, POSE_MODES["daily"])
    return dict(body=M["body"], view=M["view"], motion=M["motion"], props=M["props"])

def _prepare_expr_lists(mode:str)->Dict[str,List[str]]:
    M = EXPRESSION_MODES.get(mode, EXPRESSION_MODES["daily"])
    return dict(mouth=M["mouth"], eyes=M["eyes"], mood=M["mood"], brow=M["brow"])

def _face_safe_camera(camera_list:List[str])->List[str]:
    prefer = [c for c in camera_list if any(k in c for k in ["bust","waist-up","close-up"])]
    return prefer or camera_list

def _apply_nsfw_pools(Lp, Le, mode:str):
    if mode == "off":
        return Lp, Le

    # suggestive と explicit 共通のベース拡張
    Lp2 = dict(
        body=Lp["body"], view=Lp["view"], motion=Lp["motion"], props=Lp["props"],
        hand=merge_unique(HAND_PLACEMENT, NSFW_SUGGESTIVE_HAND),
        leg=merge_unique(LEG_POSITION, NSFW_SUGGESTIVE_LEG),
        spine=merge_unique(SPINE_SHOULDER, NSFW_SUGGESTIVE_SPINE),
        camera=merge_unique(CAMERA_FRAMING, NSFW_SUGGESTIVE_CAMERA),
        inter=merge_unique(INTERACTION, NSFW_SUGGESTIVE_INTER),
    )
    Le2 = dict(
        mouth=merge_unique(Le["mouth"], NSFW_SUGGESTIVE_MOUTH),
        eyes =merge_unique(Le["eyes"],  NSFW_SUGGESTIVE_EYES),
        mood =merge_unique(Le["mood"],  NSFW_SUGGESTIVE_MOOD),
        brow =Le["brow"], lid=LID_STATE, gaze=EYE_GAZE,
        micro=merge_unique(MICRO_EXP, NSFW_SUGGESTIVE_MICRO),
        blush=merge_unique(BLUSH, NSFW_SUGGESTIVE_BLUSH),
        sweat=merge_unique(SWEAT, NSFW_SUGGESTIVE_SWEAT),
        tear =TEAR,
    )

    if mode == "explicit":
        # explicitモードでは、さらに露骨な単語も候補に加える
        Lp2["hand"] = merge_unique(Lp2["hand"], EXTRA_NSFW_POSE)
        Lp2["leg"] = merge_unique(Lp2["leg"], EXTRA_NSFW_POSE)
        Lp2["spine"] = merge_unique(Lp2["spine"], EXTRA_NSFW_POSE)
        Le2["mood"] = merge_unique(Le2["mood"], EXTRA_NSFW_EXPR)
        Le2["blush"] = merge_unique(Le2["blush"], EXTRA_NSFW_EXPR)

    return Lp2, Le2

# ===== 高性能サニタイズ関数 (新規) =====
_BLOCK_PATTERNS = None
def _compile_block_patterns():
    global _BLOCK_PATTERNS
    if _BLOCK_PATTERNS is None:
        if not EXPLICIT_BLOCKLIST:
            _BLOCK_PATTERNS = False # ブロックリストが空なら何もしない
            return _BLOCK_PATTERNS
        terms = sorted(EXPLICIT_BLOCKLIST, key=lambda s: (-len(s), s))
        pat = r"|".join(re.escape(t) for t in terms if t)
        _BLOCK_PATTERNS = re.compile(pat, re.IGNORECASE) if pat else False
    return _BLOCK_PATTERNS

def _sanitize(seq:List[str])->List[str]:
    pat = _compile_block_patterns()
    if not pat: # パターンがなければそのまま返す
        return [s.strip() for s in seq if s and s.strip()]

    out=[]
    for t in seq:
        if not t: continue
        s = t.strip()
        if not s: continue
        if pat.search(s): # 露骨/不適切語を含むタグは破棄
            continue
        out.append(s)
    return out

# ===== タグ生成コア関数 =====
def _compose(rng, Pp:Dict[str,float], Pe:Dict[str,float],
             Lp:Dict[str,List[str]], Le:Dict[str,List[str]],
             face_safe:bool, gaze_target:str, focus_part:str,
             theme:str|None)->str:

    body = pick(rng, Lp["body"]) or "standing straight"
    view = pick(rng, Lp["view"]) if maybe(rng, Pp["view"]) else None
    motion = pick(rng, Lp["motion"]) if maybe(rng, Pp["motion"]) else None
    props = pick(rng, Lp["props"]) if maybe(rng, Pp["props"]) else None
    hand = pick(rng, Lp.get("hand", HAND_PLACEMENT)) if maybe(rng, Pp["hand"]) else None
    leg = pick(rng, Lp.get("leg", LEG_POSITION)) if maybe(rng, Pp["leg"]) else None
    spine = pick(rng, Lp.get("spine", SPINE_SHOULDER)) if maybe(rng, Pp["spine"]) else None
    camera_pool = _face_safe_camera(Lp.get("camera", CAMERA_FRAMING)) if face_safe else Lp.get("camera", CAMERA_FRAMING)
    camera = pick(rng, camera_pool) if maybe(rng, Pp["camera"]) else None
    inter = pick(rng, Lp.get("inter", INTERACTION)) if maybe(rng, Pp["inter"]) else None
    mouth = pick(rng, Le["mouth"]) or "soft smile"
    eyes  = pick(rng, Le["eyes"])  or "gentle gaze"
    brow  = pick(rng, Le["brow"]) if maybe(rng, Pe["brow"]) else None
    mood  = pick(rng, Le["mood"]) if maybe(rng, Pe["mood"]) else None
    lid   = pick(rng, Le.get("lid", LID_STATE)) if maybe(rng, Pe["lid"]) else None
    gaze  = gaze_target if gaze_target!="自動" else (pick(rng, Le.get("gaze", EYE_GAZE)) if maybe(rng, Pe["gaze"]) else None)
    micro = pick(rng, Le.get("micro", MICRO_EXP)) if maybe(rng, Pe["micro"]) else None
    blush = pick(rng, Le.get("blush", BLUSH)) if maybe(rng, Pe["blush"]) else None
    sweat = pick(rng, Le.get("sweat", SWEAT)) if maybe(rng, Pe["sweat"]) else None
    tear  = pick(rng, Le.get("tear", TEAR))  if maybe(rng, Pe["tear"])  else None

    pose_seq = [body, view, motion, props, hand, leg, spine, camera, inter]
    expr_seq = [mouth, eyes, lid, gaze, brow, micro, blush, sweat, tear, mood]

    # サニタイズは結合直前に行う
    pose_tag = join_clean(_sanitize(pose_seq), sep=", ")
    expr_tag = join_clean(_sanitize(expr_seq), sep=", ")
    return join_clean([pose_tag, expr_tag], sep=", ")

# ===== ComfyUIノードクラス =====
class PoseEmotionTagNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"seed": ("INT", {"default": 42, "min": 0, "max": 2**31-1})},
            "optional": {
                "ポーズモード": (list(POSE_MODE_JP.keys()), {"default":"日常"}),
                "表情モード": (list(EXPR_MODE_JP.keys()), {"default":"日常"}),
                "構図の複雑さ": (list(COMPLEXITY_JP.keys()), {"default":"標準"}),
                "感情の強さ": (list(INTENSITY_JP.keys()), {"default":"普通"}),
                "アダルト表現": (list(NSFW_JP.keys()), {"default":"オフ"}),
                "テーマ": (["なし","runway","pinup"], {"default":"なし"}),
                "顔切れ防止": ("BOOL", {"default": True}),
                "見せたい部位": (["自動","顔","胸","ウエスト","ヒップ","脚","背中"], {"default":"自動"}),
                "視線ターゲット": (["自動","looking at viewer","downcast gaze","side glance","upward glance","closed"], {"default":"自動"}),
                "確率: 視点": ("FLOAT", {"default":1.0, "min":0.0,"max":1.0,"step":0.01}),
                "確率: 動き": ("FLOAT", {"default":1.0, "min":0.0,"max":1.0,"step":0.01}),
                "確率: 小道具": ("FLOAT", {"default":1.0, "min":0.0,"max":1.0,"step":0.01}),
                "確率: 手配置": ("FLOAT", {"default":0.9, "min":0.0,"max":1.0,"step":0.01}),
                "確率: 脚配置": ("FLOAT", {"default":0.9, "min":0.0,"max":1.0,"step":0.01}),
                "確率: 体幹/肩線": ("FLOAT", {"default":0.9, "min":0.0,"max":1.0,"step":0.01}),
                "確率: フレーミング": ("FLOAT", {"default":1.0, "min":0.0,"max":1.0,"step":0.01}),
                "確率: インタラクション": ("FLOAT", {"default":0.8, "min":0.0,"max":1.0,"step":0.01}),
                "確率: 眉": ("FLOAT", {"default":1.0, "min":0.0,"max":1.0,"step":0.01}),
                "確率: ムード": ("FLOAT", {"default":1.0, "min":0.0,"max":1.0,"step":0.01}),
                "確率: まぶた": ("FLOAT", {"default":0.9, "min":0.0,"max":1.0,"step":0.01}),
                "確率: 視線": ("FLOAT", {"default":0.9, "min":0.0,"max":1.0,"step":0.01}),
                "確率: マイクロ表情": ("FLOAT", {"default":0.7, "min":0.0,"max":1.0,"step":0.01}),
                "確率: 赤面": ("FLOAT", {"default":0.7, "min":0.0,"max":1.0,"step":0.01}),
                "確率: 汗": ("FLOAT", {"default":0.5, "min":0.0,"max":1.0,"step":0.01}),
                "確率: 涙": ("FLOAT", {"default":0.4, "min":0.0,"max":1.0,"step":0.01}),
                "最大文字数": ("INT", {"default":160,"min":0,"max":4096}),
                "小文字化": ("BOOL", {"default": True}),
            }
        }
    RETURN_TYPES=("STRING",)
    FUNCTION="generate"
    CATEGORY="tagging" # カテゴリ名を変更したい場合はここを修正

    def generate(self, seed, **kwargs):
        rng = rng_from_seed(seed)
        pose_mode = POSE_MODE_JP.get(kwargs.get("ポーズモード","日常"), "daily")
        expr_mode = EXPR_MODE_JP.get(kwargs.get("表情モード","日常"), "daily")
        complexity = COMPLEXITY_JP.get(kwargs.get("構図の複雑さ","標準"), "normal")
        intensity  = INTENSITY_JP.get(kwargs.get("感情の強さ","普通"), "normal")
        nsfw_level = NSFW_JP.get(kwargs.get("アダルト表現","オフ"), "off")
        theme = None if kwargs.get("テーマ","なし")=="なし" else kwargs.get("テーマ")
        face_safe = bool(kwargs.get("顔切れ防止", True))
        gaze_target = kwargs.get("視線ターゲット","自動")
        max_len = int(kwargs.get("最大文字数",160))
        lowercase = bool(kwargs.get("小文字化", True))
        Cp = _complexity_profile(complexity)
        Ce = _intensity_profile(intensity)
        def f(name, default): return float(kwargs.get(name, default))
        Pp = {
            "view":f("確率: 視点",1.0)*Cp["view"], "motion":f("確率: 動き",1.0)*Cp["motion"],
            "props":f("確率: 小道具",1.0)*Cp["props"], "hand":f("確率: 手配置",0.9)*Cp["hand"],
            "leg":f("確率: 脚配置",0.9)*Cp["leg"], "spine":f("確率: 体幹/肩線",0.9)*Cp["spine"],
            "camera":f("確率: フレーミング",1.0)*Cp["camera"], "inter":f("確率: インタラクション",0.8)*Cp["inter"],
        }
        Pe = {
            "brow":f("確率: 眉",1.0)*Ce["brow"], "mood":f("確率: ムード",1.0)*Ce["mood"],
            "lid":f("確率: まぶた",0.9)*Ce["lid"], "gaze":f("確率: 視線",0.9)*Ce["gaze"],
            "micro":f("確率: マイクロ表情",0.7)*Ce["micro"], "blush":f("確率: 赤面",0.7)*Ce["blush"],
            "sweat":f("確率: 汗",0.5)*Ce["sweat"], "tear":f("確率: 涙",0.4)*Ce["tear"],
            "mouth":Ce["mouth"], "eyes":Ce["eyes"],
        }

        Lp = _prepare_pose_lists(pose_mode)
        Le = _prepare_expr_lists(expr_mode)

        if nsfw_level != "off":
            Lp, Le = _apply_nsfw_pools(Lp, Le, nsfw_level)
            Pp.update({k: min(1.0, v*1.1) for k,v in Pp.items()})
            Pe.update({
                "blush": min(1.0, Pe["blush"]*1.2), "sweat": min(1.0, Pe["sweat"]*1.2),
                "micro": min(1.0, Pe["micro"]*1.1), "gaze":  min(1.0, Pe["gaze"]*1.1),
                "lid":   min(1.0, Pe["lid"]*1.05),
            })

        tag = _compose(rng, Pp, Pe, Lp, Le, face_safe, gaze_target, kwargs.get("見せたい部位","自動"), theme)
        tag = normalize(tag, lowercase)
        tag = limit_len(tag, max_len)
        return (tag,)
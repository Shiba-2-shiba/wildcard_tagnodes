#
# camera_lighting_tag_v3.py
# ComfyUI V3 Custom Node
#
# This script is a V3 refactoring of the original camera_lighting_tag.py.
# It generates tags related to camera angles and lighting for creative prompts.
#

# Third-party imports for ComfyUI V3 schema
from comfy_api.latest import io

# Local imports from the original script
# Assume these utility and vocabulary files are in the correct relative path
from .util import rng_from_seed, maybe, pick, join_clean, limit_len, normalize
from .vocab.camera_lighting_vocab import (
    COMMON_ANGLES, PORTRAIT_SHOTS, LANDSCAPE_SHOTS,
    LIGHT_STYLES_SAFE, LIGHT_DIRECTIONS_SAFE, LIGHT_TIMES, LIGHT_COLORS,
    PORTRAIT_EROTIC_TONE,
    PORTRAIT_EROTIC_TONE_TIER1, PORTRAIT_EROTIC_TONE_TIER2, PORTRAIT_EROTIC_TONE_TIER3,
    LANDSCAPE_GRANDEUR_TONE,
    BAN_REPLACE
)

# Constants from the V1 script
MODE_MAP_JP = {"女性": "portrait", "風景": "landscape"}
EROTIC_LEVEL_CHOICES = ["控えめ (Tier1)", "強め (Tier2)", "濃厚 (Tier3)"]

class CameraLightingTagNodeV3(io.ComfyNode):
    """
    A node that generates integrated tags for camera angles and lighting.
    It probabilistically combines composition, light style, direction, time of day, etc.,
    based on a selected theme ('portrait' or 'landscape').
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        """
        Defines the schema for the node, including inputs and outputs.
        This method replaces the V1 INPUT_TYPES class method.
        """
        return io.Schema(
            node_id="CameraLightingTagNodeV3",
            display_name="Camera & Lighting Tag (V3)",
            category="Text/Wildcards",
            description="Generates integrated tags for camera angles and lighting.",
            # Define inputs based on V1's INPUT_TYPES
            inputs=[
                io.Int.Input(id="seed", default=42, min=0, max=2**31 - 1, tooltip="Random seed for tag generation"),
                io.Combo.Input(id="subject", display_name="主役 (Subject)", options=list(MODE_MAP_JP.keys()), default="女性", tooltip="Choose the main subject theme"),
                io.Int.Input(id="max_length", display_name="最大文字数 (Max Length)", default=120, min=0, max=4096, tooltip="Maximum length of the generated tag string"),
                io.Boolean.Input(id="lowercase", display_name="小文字化 (Lowercase)", default=True, tooltip="Convert the output to lowercase"),
                io.Float.Input(id="prob_angle", display_name="確率: 角度 (Prob: Angle)", default=0.75, min=0.0, max=1.0, step=0.01, tooltip="Probability of including a camera angle tag"),
                io.Float.Input(id="prob_shot", display_name="確率: ショット (Prob: Shot)", default=0.95, min=0.0, max=1.0, step=0.01, tooltip="Probability of including a shot type tag (e.g., close-up)"),
                io.Float.Input(id="prob_light_direction", display_name="確率: ライト方向 (Prob: Light Direction)", default=0.65, min=0.0, max=1.0, step=0.01, tooltip="Probability of including a light direction tag"),
                io.Float.Input(id="prob_time", display_name="確率: 時間帯 (Prob: Time of Day)", default=0.55, min=0.0, max=1.0, step=0.01, tooltip="Probability of including a time of day tag"),
                io.Float.Input(id="prob_color", display_name="確率: 色味 (Prob: Color)", default=0.45, min=0.0, max=1.0, step=0.01, tooltip="Probability of including a lighting color tag"),
                io.Float.Input(id="prob_tone_boost", display_name="確率: 雰囲気補強 (Prob: Tone Boost)", default=0.75, min=0.0, max=1.0, step=0.01, tooltip="Probability of adding an atmospheric tone tag"),
                io.Combo.Input(id="erotic_level_female", display_name="官能レベル(女性) (Erotic Level - Portrait)", options=EROTIC_LEVEL_CHOICES, default="強め (Tier2)", tooltip="Sensual level for the 'portrait' mode"),
                io.Float.Input(id="prob_erotic_tag_female", display_name="確率: 官能タグ(女性) (Prob: Erotic Tag - Portrait)", default=0.85, min=0.0, max=1.0, step=0.01, tooltip="Probability of using a sensual tag in 'portrait' mode"),
                io.Float.Input(id="grandeur_boost_landscape", display_name="雄大さ強調(風景) (Grandeur Boost - Landscape)", default=0.85, min=0.0, max=1.0, step=0.05, tooltip="Boost for majestic atmosphere in 'landscape' mode"),
            ],
            # Define outputs based on V1's RETURN_TYPES
            outputs=[
                io.String.Output(id="text", display_name="STRING", tooltip="The generated camera and lighting tags"),
            ]
        )

    # Helper methods ported from the V1 class
    def _sanitize(self, text: str) -> str:
        """Sanitizes the text by replacing banned words."""
        if not text:
            return text
        t = text
        low = t.lower()
        for bad, rep in BAN_REPLACE.items():
            if bad in low:
                t = t.replace(bad, rep).replace(bad.title(), rep).replace(bad.upper(), rep)
                low = t.lower()
        return t

    def _pick_shot_by_mode(self, rng, mode: str, p_shot: float):
        """Picks a shot type based on the subject mode."""
        if mode == "portrait":
            return pick(rng, PORTRAIT_SHOTS) if maybe(rng, p_shot) else None
        else:
            return pick(rng, LANDSCAPE_SHOTS) if maybe(rng, p_shot) else None

    def _pick_erotic_tone(self, rng, level: str):
        """Picks a sensual tone based on the selected tier."""
        if "Tier3" in level:
            pool = PORTRAIT_EROTIC_TONE_TIER3 + PORTRAIT_EROTIC_TONE_TIER2
        elif "Tier2" in level:
            pool = PORTRAIT_EROTIC_TONE_TIER2 + PORTRAIT_EROTIC_TONE_TIER1
        else:
            pool = PORTRAIT_EROTIC_TONE_TIER1
        pool = pool + PORTRAIT_EROTIC_TONE
        return pick(rng, pool)

    def _tone_by_mode(self, rng, mode: str, p_tone: float,
                      erotic_level: str, p_erotic: float,
                      grandeur_boost: float):
        """Selects an atmospheric tone based on the subject mode."""
        if mode == "portrait":
            if maybe(rng, min(1.0, p_erotic)):
                return self._pick_erotic_tone(rng, erotic_level)
            return pick(rng, PORTRAIT_EROTIC_TONE) if maybe(rng, p_tone * 0.5) else None
        else:
            prob = min(1.0, p_tone * (0.6 + 0.4 * max(0.0, min(1.0, grandeur_boost))))
            return pick(rng, LANDSCAPE_GRANDEUR_TONE) if maybe(rng, prob) else None

    @classmethod
    def execute(cls, seed: int, subject: str, max_length: int, lowercase: bool,
                prob_angle: float, prob_shot: float, prob_light_direction: float,
                prob_time: float, prob_color: float, prob_tone_boost: float,
                erotic_level_female: str, prob_erotic_tag_female: float,
                grandeur_boost_landscape: float, **kwargs) -> io.NodeOutput:
        """
        This is the main execution method of the node.
        It replaces the V1 `generate` method.
        """
        node_instance = cls()
        rng = rng_from_seed(seed)
        mode = MODE_MAP_JP.get(subject, "portrait")

        # Core tag components
        angle = pick(rng, COMMON_ANGLES) if maybe(rng, prob_angle) else None
        shot = node_instance._pick_shot_by_mode(rng, mode, prob_shot)
        style = pick(rng, LIGHT_STYLES_SAFE)
        direction = pick(rng, LIGHT_DIRECTIONS_SAFE) if maybe(rng, prob_light_direction) else None
        time = pick(rng, LIGHT_TIMES) if maybe(rng, prob_time) else None
        color = pick(rng, LIGHT_COLORS) if maybe(rng, prob_color) else None

        # Mode-dependent tone
        tone = node_instance._tone_by_mode(
            rng, mode, prob_tone_boost,
            erotic_level=erotic_level_female, p_erotic=prob_erotic_tag_female,
            grandeur_boost=grandeur_boost_landscape
        )

        # Assemble and process the final tag string
        parts = [time, color, style, direction, angle, shot, tone]
        tag = join_clean(parts)

        tag = node_instance._sanitize(tag)
        tag = normalize(tag, lowercase)
        tag = limit_len(tag, max_length)

        # Return the result wrapped in io.NodeOutput
        return io.NodeOutput(text=tag)

# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "CameraLightingTagNodeV3": CameraLightingTagNodeV3
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CameraLightingTagNodeV3": "Camera & Lighting Tag (V3)"
}

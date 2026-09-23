from typing import Any
import bpy

def is_LUT_image(img: bpy.types.Image) -> bool:
    if not img.is_float:
        return False

    # TODO: More LUT types like Pattern LUT and such
    if img.size[0] != 23:
        return False

    return True

def safe_hash(obj: Any) -> int:
    return hash(obj) % 0x7ffffffe
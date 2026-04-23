import bpy
from typing import Tuple
from bpy.types import ShaderNodeTexImage, Image

IDMaskSockets = Tuple[bpy.types.NodeSocketColor, bpy.types.NodeSocketFloat, bpy.types.NodeSocketColor, bpy.types.NodeSocketFloat]
IDMaskImageNodes = Tuple[ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage, ShaderNodeTexImage]
IDMaskImages = Tuple[Image, Image, Image, Image, Image, Image, Image, Image]
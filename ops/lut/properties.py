from __future__ import annotations
from typing import Callable, Dict, Literal, Self, Tuple

import bpy
from bpy.types import Context

from .enums import LUTColumn1A, BumpMap
from ...utils import LUT
from ...utils.LUT import LUT as LUTType, Float4
from ..utils.images import lut_from_blender_image, populate_blender_lut
from .util import safe_hash

LUT_MAP: Dict[int, BPYLUTBridge] = {}

Float3 = Tuple[float, float, float]
class LUTPixelProperty(bpy.types.PropertyGroup):
    def get_pixel(self) -> Float4:
        bridge = LUT_MAP[self.map_hash]
        return bridge.lut.get_pixel(self.index)

    def set_pixel(self, new_pixel: Float4):
        if self.map_hash == 0:
            return
        bridge = LUT_MAP[self.map_hash]
        bridge.modify_lut(lambda lut: lut.set_pixel(self.index, new_pixel))

    def get_color(self) -> Float3:
        color = tuple(self.get_pixel()[:-1])
        assert len(color) == 3
        return color

    def set_color(self, new: Float3):
        pixel = list(self.get_pixel())
        pixel[:-1] = list(new)
        pixel = tuple(pixel)
        assert len(pixel) == 4
        self.set_pixel(pixel)

    color: bpy.props.FloatVectorProperty(
        name="LUT Pixel Data",
        subtype="COLOR",
        size=3,
        default=(0.0,0.0,0.0),
        set=set_color, # type: ignore
        get=get_color
    ) # type: ignore

    def set_pix_index(self, new_val: float, index: int):
        pix = list(self.get_pixel())
        pix[index] = new_val
        pix = tuple(pix)
        assert len(pix) == 4
        self.set_pixel(pix)

    def get_pix_index(self, index: int) -> float:
        return self.get_pixel()[index]
    
    r: bpy.props.FloatProperty(
        name="LUT Pixel Data R",
        default=0.0,
        set=lambda self,v: self.set_pix_index(v, 0), # type: ignore
        get=lambda self: self.get_pix_index(0) # type: ignore
    ) # type: ignore

    g: bpy.props.FloatProperty(
            name="LUT Pixel Data G",
            default=0.0,
            set=lambda self,v: self.set_pix_index(v, 1), # type: ignore
            get=lambda self: self.get_pix_index(1) # type: ignore
        ) # type: ignore

    b: bpy.props.FloatProperty(
            name="LUT Pixel Data B",
            default=0.0,
            set=lambda self,v: self.set_pix_index(v, 2), # type: ignore
            get=lambda self: self.get_pix_index(2) # type: ignore
        ) # type: ignore

    a: bpy.props.FloatProperty(
            name="LUT Pixel Data A",
            default=0.0,
            set=lambda self,v: self.set_pix_index(v, 3), # type: ignore
            get=lambda self: self.get_pix_index(3) # type: ignore
        ) # type: ignore


    def set_col1a(self, index: int):
        self.set_pix_index(LUTColumn1A(index).to_float(), 3)
    def get_col1a(self) -> int:
        return LUTColumn1A.from_float(self.get_pix_index(3)).value
    col1_a: bpy.props.EnumProperty(
        name="Special Material Mode",
        items=LUTColumn1A.values(),
        set=set_col1a,
        get=get_col1a
    ) # type: ignore

    def set_bmi(self, index: int):
        self.set_pix_index(float(index), 0)
    def get_bmi(self) -> int:
        return int(self.get_pix_index(0))
    bump_map_index_int: bpy.props.IntProperty(
        name= "Bump Map Index",
        min=0,
        max=25,
        set=set_bmi,
        get=get_bmi
    ) # type: ignore

    bump_map_index_enum: bpy.props.EnumProperty(
        name="Bump Map",
        items=BumpMap.values(),
        set=set_bmi,
        get=get_bmi
    ) # type: ignore

    def set_camo_type(self, index: int):
        self.set_pix_index(max(-1, index), 3)
        pass
    def get_camo_type(self) -> int:
        camo = int(self.get_pix_index(3))
        camo = max(-1, camo)
        return camo
    camo_type: bpy.props.IntProperty(
        name="Camo Type",
        set=set_camo_type,
        get=get_camo_type,
        min=-1,
        max=10
    ) # type: ignore


    index: bpy.props.IntVectorProperty(
        name="LUT Pixel Index",
        size=2,
        default=(0,0)
    ) # type: ignore

    map_hash: bpy.props.IntProperty(
        name="Map Hash"
    ) # type: ignore

LUT_PROPERTY_NAME = "hd2_idmask_lut_property"
class LUTProperty(bpy.types.PropertyGroup):
    lut: bpy.props.CollectionProperty(
        type=LUTPixelProperty, # type: ignore
        name="pixels",
    ) # type: ignore

    def clamped_set(self, v):
        self["selected_row"] = max(1, min(v, LUT_MAP[self.map_hash].lut.dim()[1]))
    def get_selected_row(self) -> int:
        return self.get("selected_row", 1) #type: ignore
    selected_row: bpy.props.IntProperty(
        name="LUT Row",
        default=1,
        set=clamped_set,
        get=get_selected_row,
        min=1
    ) # type: ignore

    map_hash: bpy.props.IntProperty(
        name="Map Hash"
    ) # type: ignore

    @classmethod
    def from_wm(cls, wm: bpy.types.WindowManager) -> Self:
        return wm.hd2_idmask_lut_property # type: ignore

class BPYLUTBridge:
    lut: LUTType
    image: bpy.types.Image
    lut_property: LUTProperty

    def __init__(self, image: bpy.types.Image, lut_prop: LUTProperty, lut: LUTType | None = None):
        self.image = image
        if lut is None:
            self.lut = lut_from_blender_image(image)
        else:
            self.lut = lut

        self.lut_property = lut_prop
        LUT_MAP[safe_hash(self.image)] = self
        self.populate_lut_property()

        #bpy.msgbus.subscribe_rna(
        #    key=image,
        #    owner=self,
        #    args=(),
        #    notify=lambda: self.populate_lut_property()
        #)

    def modify_lut(self, lamb: Callable[[LUTType], None]):
        lamb(self.lut)
        populate_blender_lut(self.lut, self.image)
        for scene in bpy.data.scenes:
            scene.update_render_engine()

    def __delete__(self):
        h = self.get_hash()
        if h in LUT_MAP:
            del LUT_MAP[h]

        # bpy.msgbus.clear_by_owner(self)

    def populate_lut_property(self):
        #print("populating LUT properties")
        prop = self.lut_property
        image = self.image
        prop.lut.clear()
        prop.map_hash = self.get_hash()

        x_dim,y_dim = self.lut.dim()
        for y in range(y_dim):
            for x in range(x_dim):
                new_pixel: LUTPixelProperty = prop.lut.add()
                new_pixel.index = (x,y)
                new_pixel.map_hash = self.get_hash()

    def get_hash(self) -> int:
        return safe_hash(self.image)

    @classmethod
    def get_from_windowmanager(cls, window_manager: bpy.types.WindowManager, image: bpy.types.Image) -> Self:
        h = safe_hash(image)
        lut_prop = window_manager.hd2_idmask_lut_property # type: ignore
        LUT_MAP[h] = BPYLUTBridge(image, lut_prop)
        #if h != window_manager.hd2_idmask_lut_property.map_hash:
            
            
        return LUT_MAP[h] # type: ignore
from typing import Literal

import bpy
from bpy.types import Context
from .properties import BPYLUTBridge, LUTProperty, LUTPixelProperty
from .ui import draw_lut_pixel
from .util import is_LUT_image
from ..utils import accurate_shader

def panel_draw(layout: bpy.types.UILayout, bridge: BPYLUTBridge):
    col = layout.column(align=True)
    col.prop(bridge.lut_property, "selected_row")

    def draw_lut_row(col: bpy.types.UILayout, row_index: int):
        x_dim,y = bridge.lut.dim()
        for x in range(x_dim):
            pixel_index = x_dim*row_index+x
            pixel = bridge.lut_property.lut[pixel_index]
            
            draw_lut_pixel(col, pixel, x+1)
            #draw_lut_color_with_alpha_slider(col, pixel)

    draw_lut_row(col, bridge.lut_property.selected_row-1)

class LUTEditPanelIMEditor(bpy.types.Panel):
    """Creates a Panel in the Image Editor"""
    bl_label = "LUT Editor"
    bl_idname = "UI_PT_LUTEditPanelImageEditor"
    bl_category = "LUT Editor"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context: Context) -> None:
        space = context.space_data
        assert space is not None
        assert space.type == "IMAGE_EDITOR"
        assert isinstance(space, bpy.types.SpaceImageEditor)
        assert space.image is not None
        assert context.window_manager is not None
        
        layout = self.layout
        assert layout is not None
        bridge = BPYLUTBridge.get_from_windowmanager(context.window_manager, space.image)
        panel_draw(layout, bridge)
        
    @classmethod
    def poll(cls, context: Context) -> bool:
        space = context.space_data
        if (
            space is None 
            or space.type != "IMAGE_EDITOR" 
            or not isinstance(space, bpy.types.SpaceImageEditor)
            or space.image is None
            or context.window_manager is None
            ):
            return False

        if not is_LUT_image(space.image):
            return False

        return True

class LUTEditPanel3D(bpy.types.Panel):
    """Creates a Panel in the View3D space"""
    bl_label = "LUT Editor"
    bl_idname = "UI_PT_LUTEditPanelView3D"
    bl_category = "LUT Editor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context: Context) -> None:
        assert context.window_manager is not None
        ao = context.active_object
        assert ao is not None
        mg = accurate_shader.find_main_group(ao)
        assert mg is not None
        lut_node = mg.get_primary_lut_texture_node()
        assert lut_node is not None
        lut_image = lut_node.image
        assert lut_image is not None
        
        layout = self.layout
        assert layout is not None
        bridge = BPYLUTBridge.get_from_windowmanager(context.window_manager, lut_image)
        panel_draw(layout, bridge)
        
    @classmethod
    def poll(cls, context: Context) -> bool:
        if (
            context.window_manager is None
            or context.active_object is None
            or (mg := accurate_shader.find_main_group(context.active_object)) is None
            or (tn := mg.get_primary_lut_texture_node()) is None
            or tn.image is None
            ):
            return False

        if not is_LUT_image(tn.image):
            return False

        return True

class ExportLUTOperator(bpy.types.Operator):
    bl_idname = "hd2visual.export_lut_dds"
    bl_label = "Export LUT as DDS"
    bl_options = {'REGISTER'}

    filepath: bpy.props.StringProperty(name="LUT Path", subtype="FILE_PATH", default="lut.dds") #type: ignore
        
    filter_glob: bpy.props.StringProperty(
        default="*.dds",
        options={'HIDDEN'},
    ) #type: ignore

    def draw(self, context):
        layout = self.layout
        assert layout is not None

        layout.label(text="Export to a .dds file.", icon='INFO')

    def invoke(self, context: Context, event: bpy.types.Event) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        ao = context.active_object
        assert ao is not None
        mg = accurate_shader.find_main_group(ao)
        assert mg is not None
        lut_node = mg.get_primary_lut_texture_node()
        assert lut_node is not None
        lut_image = lut_node.image
        assert lut_image is not None

        if ".blend" in self.filepath:
            raise ValueError("Refusing to overwrite blend file!")

        bridge = BPYLUTBridge.get_from_windowmanager(context.window_manager, lut_image)
        with open(self.filepath, 'wb') as f:
            f.write(bridge.lut.to_dds().getbuffer())

        return {"FINISHED"}

    @classmethod
    def poll(cls, context: Context) -> bool:
        if (
            context.window_manager is None
            or context.active_object is None
            or (mg := accurate_shader.find_main_group(context.active_object)) is None
            or (tn := mg.get_primary_lut_texture_node()) is None
            or tn.image is None
            ):
            cls.poll_message_set("No accurate material found, or it was broken")
            return False

        if not is_LUT_image(tn.image):
            cls.poll_message_set("image does not seem like a LUT")
            return False

        return True


CLASSES = [LUTPixelProperty, LUTProperty, LUTEditPanelIMEditor, LUTEditPanel3D, ExportLUTOperator]
def register():
    for c in CLASSES:
        bpy.utils.register_class(c)

    bpy.types.WindowManager.hd2_idmask_lut_property = bpy.props.PointerProperty(type=LUTProperty) #type: ignore

def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)

    del bpy.types.WindowManager.hd2_idmask_lut_property #type: ignore
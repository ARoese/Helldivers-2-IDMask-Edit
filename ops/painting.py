from pathlib import Path
from typing import Literal, Tuple
import bpy
from bpy.types import Context, Event

from .utils.custom_types import IDMaskImageNodes

from .utils import accurate_shader
from .utils.idmask_debug_material import create_idmask_debug_material
from .utils.images import IDMaskImages, make_id_mask_images, id_mask_array_from_images
from ..utils import IDMask

from .utils.idmask_debug_material import IDMaskDebugMaterial
class PaintMaterial(bpy.types.Operator):
    bl_idname = "hd2visual.paint_material"
    bl_label = "Material N"
    bl_options = {'REGISTER'}

    material_index: bpy.props.IntProperty(name="Material Index", default=1, min=1, max=8) #type: ignore
    set_pattern_mask: bpy.props.BoolProperty(name="Paint Pattern Mask", default=False) #type: ignore

    @classmethod
    def set_brush_settings(cls, context: Context):
        if context.tool_settings is None or context.tool_settings.image_paint is None or context.tool_settings.image_paint.brush is None:
            return
        brush = context.tool_settings.image_paint.brush
        
        BLACK = (0.0, 0.0, 0.0)
        WHITE = (1.0, 1.0, 1.0)
        primary = brush.color
        secondary = brush.secondary_color
        def color_eq(color1, color2: Tuple[float, float, float]) -> bool:
            return color1.r == color2[0] and color1.g == color2[1] and color1.b == color1[2]
        
        def assign_color(target_color, to_assign: Tuple[float, float, float]):
            target_color.r = to_assign[0]
            target_color.g = to_assign[1]
            target_color.b = to_assign[2]
        
        if color_eq(primary, WHITE) or color_eq(secondary, BLACK):
            assign_color(primary, WHITE)
            assign_color(secondary, BLACK)
        elif color_eq(primary, BLACK) or color_eq(secondary, WHITE):
            assign_color(secondary, WHITE)
            assign_color(primary, BLACK)
        else:
            assign_color(primary, WHITE)
            assign_color(secondary, BLACK)

    def execute_debug_material(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        ao = context.active_object
        assert ao is not None
        am = ao.active_material
        assert am is not None

        def find_paint_slot_index(ref_name: str) -> int:
            ind = -1
            for i,slot in enumerate(am.texture_paint_slots):
                if slot.name == ref_name:
                    ind = i
            assert ind != -1
            return ind
        
        debug_material = IDMaskDebugMaterial(am)
        textures = debug_material.get_layer_images()
        assert textures is not None
        textures, pattern_mask_texture = textures

        if self.set_pattern_mask:
            am.paint_active_slot = find_paint_slot_index(pattern_mask_texture.name)
        else:
            image_names = [image.name for image in textures]
            target_image_name = image_names[self.material_index-1]

            am.paint_active_slot = find_paint_slot_index(target_image_name)

        return {'FINISHED'}

    def execute_accurate_shader(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        ao = context.active_object
        assert ao is not None
        am = ao.active_material
        assert am is not None
        main_group = accurate_shader.from_material(am)
        assert main_group is not None
        texture_nodes = main_group.get_idmask_channel_texture_nodes()
        assert texture_nodes is not None
        

        def find_paint_slot_index(ref_name: str) -> int:
            ind = -1
            for i,slot in enumerate(am.texture_paint_slots):
                if slot.name == ref_name:
                    ind = i
            assert ind != -1
            return ind
            
        # set image being edited
        if self.set_pattern_mask:
            pattern_mask_node = main_group.find_pattern_mask_node()
            assert pattern_mask_node is not None and pattern_mask_node.image is not None

            am.paint_active_slot = find_paint_slot_index(pattern_mask_node.image.name)
        else:
            image_names = [node.image.name for node in texture_nodes if node.image is not None]
            target_image_name = image_names[self.material_index-1]

            am.paint_active_slot = find_paint_slot_index(target_image_name)
            
        return {'FINISHED'}

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        ao = context.active_object
        assert ao is not None
        assert ao.active_material is not None
        
        self.set_brush_settings(context)

        if IDMaskDebugMaterial.is_debug_material(ao.active_material):
            return self.execute_debug_material(context)
        else:
            return self.execute_accurate_shader(context)
    
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        ao = context.active_object
        if ao is None or ao.active_material is None:
            cls.poll_message_set("Make sure an editable material is active")
            return False
        
        if IDMaskDebugMaterial.is_debug_material(ao.active_material):
            return True
        
        if (main_group := accurate_shader.from_material(ao.active_material)) is None:
            cls.poll_message_set("Could not find editable material")
            return False
        
        if not main_group.is_patched():
            cls.poll_message_set("Shader group must be patched")
            return False
        
        texture_nodes = main_group.get_idmask_channel_texture_nodes()
        if texture_nodes is None:
            cls.poll_message_set("Could not find IDMask channel input nodes")
            return False
        
        mask_node = main_group.find_pattern_mask_node()
        if mask_node is None or mask_node.image is None:
            cls.poll_message_set("Could not find pattern mask channel input node")
            return False
        
        return True
    

class MaterialSwitcherPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "LUT Materials"
    bl_idname = "UI_PT_MaterialSwitcherPanel"
    bl_category = "LUT Materials"
    bl_space_type = 'VIEW_3D'
    bl_context = "imagepaint"
    bl_region_type = 'UI'

    def draw(self, context: Context) -> None:
        layout = self.layout
        assert layout is not None
        
        col = layout.column(align=True)
        col.label(text="IDMask Array")
        for i in range(1,9):
            op = col.operator(PaintMaterial.bl_idname, text=f"Material {i}")
            op.material_index = i
            op.set_pattern_mask = False

        col.label(text="Pattern Mask")
        col.operator(PaintMaterial.bl_idname, text=f"Pattern Mask").set_pattern_mask = True
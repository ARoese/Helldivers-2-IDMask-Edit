from typing import Literal, Tuple
import bpy
from bpy.types import Context
from .import_export import is_main_node_group, is_group_patched, get_idmask_channel_texture_nodes, trace_to_textures

def _find_shader_graph_node(obj: bpy.types.Object) -> bpy.types.ShaderNodeGroup | None:
    for ms in obj.material_slots:
        if ms.material is None:
            continue

        if not ms.material.use_nodes:
            continue
        
        if ms.material.node_tree is None:
            continue
        
        for node in ms.material.node_tree.nodes:
            if node is None:
                continue
            if isinstance(node, bpy.types.ShaderNodeGroup) and is_main_node_group(node):
                return node
            
def _find_pattern_mask_node(main_group: bpy.types.ShaderNodeGroup) -> bpy.types.ShaderNodeTexImage | None:
    tl = trace_to_textures(main_group.inputs["Pattern Mask Array"])
    if len(tl) == 0:
        return None

    return tl[0]


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

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.active_object is not None
        main_group = _find_shader_graph_node(context.active_object)
        assert main_group is not None
        texture_nodes = get_idmask_channel_texture_nodes(main_group)
        assert texture_nodes is not None
        am = context.active_object.active_material
        assert am is not None

        # set brush colors
        self.set_brush_settings(context)


        def find_paint_slot_index(ref_name: str) -> int:
            ind = -1
            for i,slot in enumerate(am.texture_paint_slots):
                if slot.name == ref_name:
                    ind = i
            assert ind != -1
            return ind
            
        # set image being edited
        if self.set_pattern_mask:
            pattern_mask_node = _find_pattern_mask_node(main_group)
            assert pattern_mask_node is not None and pattern_mask_node.image is not None

            am.paint_active_slot = find_paint_slot_index(pattern_mask_node.image.name)
        else:
            image_names = [node.image.name for node in texture_nodes if node.image is not None]
            target_image_name = image_names[self.material_index-1]

            am.paint_active_slot = find_paint_slot_index(target_image_name)
            
        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        ao = context.active_object
        if ao is None or ao.active_material is None or (main_group := _find_shader_graph_node(ao)) is None:
            cls.poll_message_set("Could not find editable material")
            return False
        
        if not is_group_patched(main_group):
            cls.poll_message_set("Shader group must be patched")
            return False
        
        texture_nodes = get_idmask_channel_texture_nodes(main_group)
        if texture_nodes is None:
            cls.poll_message_set("Could not find IDMask channel input nodes")
            return False
        
        mask_node = _find_pattern_mask_node(main_group)
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
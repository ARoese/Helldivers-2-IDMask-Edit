from typing import List, Literal

import bpy
from bpy_extras import view3d_utils
import mathutils
from ...utils import LUT
from ...utils.LUT import LUT as LUTType
from ...utils.IDMask import PackedChannels
from ..utils import accurate_shader

from .lut_panel import BPYLUTBridge
from ..utils import images as image_util


def get_debug_LUT() -> LUTType:
    DEBUG_LUT_JSON = "[[[1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, -1.0], [1.0, 0.0, 0.0, 1.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.90625, 0.90625, 0.90625, 2.0], [0.63671875, 0.63671875, 0.63671875, -1.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.25, 0.25, 0.5498046875], [0.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.99609375, 0.0, 0.0, 0.0], [0.0, 0.0, 0.1199951171875, 0.4599609375], [0.0, -0.25, 0.199951171875, 0.0], [0.0, 0.0, 0.0, 0.5], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, -1.0], [0.0, 0.0, 0.0, 0.5]]]"
    return LUT.from_json(DEBUG_LUT_JSON)

class LUTSelectionModalOperator(bpy.types.Operator):
    """Select a LUT row using the mouse"""
    bl_idname = "hd2visual.lut_select_eyedropper"
    bl_label = "Visually Select LUT Row"
    
    original_LUT: LUTType
    color_phase: float

    target_object: bpy.types.Object
    target_lut: bpy.types.Image
    target_idmask: PackedChannels
    target_material: accurate_shader.AccurateShaderMainGroup
    bridge: BPYLUTBridge

    # TODO: Works in ortho and simple views, does not in other views. Fix it
    def do_raycast(self, context: bpy.types.Context, event: bpy.types.Event) -> mathutils.Vector | None:
        if (context.region is None 
            or context.space_data is None 
            or context.space_data.region_3d is None): # type: ignore
            return None

        view3d_utils.region_2d_to_origin_3d
        origin_vector = view3d_utils.region_2d_to_origin_3d(
            context.region, 
            context.space_data.region_3d, # type: ignore
            (event.mouse_region_x, event.mouse_region_y))
        
        direction_vector = view3d_utils.region_2d_to_vector_3d(
            context.region, 
            context.space_data.region_3d, # type: ignore
            (event.mouse_region_x, event.mouse_region_y))

        depsgraph = context.evaluated_depsgraph_get()
        obj_eval = self.target_object.evaluated_get(depsgraph)
        hit, location, normal, face_index = self.target_object.ray_cast(
            self.target_object.matrix_world.inverted() @ origin_vector,
            self.target_object.matrix_world.inverted().to_3x3() @ direction_vector
        ) # type: ignore # This does not return None

        assert isinstance(hit, bool) and isinstance(face_index, int) and isinstance(location, mathutils.Vector)

        if not hit or face_index == -1:
            return None

        assert isinstance(obj_eval.data, bpy.types.Mesh) 
        mesh = obj_eval.data
        poly = mesh.polygons[face_index]
        poly.normal

        # Get the vertices and UV layer data
        uv_layer = mesh.uv_layers.active
        if not uv_layer:
            return None
        
        uv_data = uv_layer.data
        
        # Gather vertex positions and UVs for the hit face
        face_verts = [mesh.vertices[vi].co for vi in poly.vertices]
        face_uvs: List[mathutils.Vector] = [uv_data[li].uv for li in poly.loop_indices]

        # Convert hit location back to local space of the object
        local_hit = self.target_object.matrix_world.inverted() @ location # NOTE: This might be incorrect

        # Generalized barycentric coordinates of the hit point with respect to the hit face verts
        weights = mathutils.interpolate.poly_3d_calc([vec.to_3d().to_tuple() for vec in face_verts], location)
        # Convert barycentric coordinate to UV-space coordinate
        hit_uv = mathutils.Vector((0,0))
        for weight, uv in zip(weights, face_uvs):
            hit_uv += uv * weight

        return hit_uv

    def lut_index_for_uv(self, uv: mathutils.Vector) -> int:
        uv_coords = uv.to_tuple()
        assert len(uv_coords) == 2
        uv_coords = (uv_coords[0] % 1.0, uv_coords[1] % 1.0) # udims
        return self.target_idmask.top_layer_at(uv_coords)

    def get_hovered_index(self, context: bpy.types.Context, event: bpy.types.Event) -> int | None:
        hit_uv = self.do_raycast(context, event)
        #print(hit_uv)
        if hit_uv is not None:
            return self.lut_index_for_uv(hit_uv)

    def handle_mouse_move(self, context: bpy.types.Context, event: bpy.types.Event):
        hovered_index = self.get_hovered_index(context, event)
        if hovered_index is not None:
            #print(f"top layer: {hovered_index}")
            debug_lut = get_debug_LUT().clone()
            # TODO: Make this debug lut spin through the rainbow over time 
            # using self.color_phase to ensure it is clearly visible no matter what.
            highlight_lut = self.original_LUT.clone()
            highlight_lut.set_row(hovered_index, debug_lut.get_row(0))
            image_util.populate_blender_lut(highlight_lut, self.target_lut)
        else:
            self.reset_lut()

    def reset_lut(self):
        image_util.populate_blender_lut(self.original_LUT, self.target_lut)

    def modal(self, context: bpy.types.Context, event: bpy.types.Event) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        w = context.window_manager.windows[0]
        try:
            w.cursor_modal_set("EYEDROPPER")
            # 1. Handle continuous event execution (Mouse Move)
            if event.type == 'MOUSEMOVE':
                self.handle_mouse_move(context, event)
                    
            # 2. Handle confirmation event (Left Mouse Click)
            elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                
                hovered_index = self.get_hovered_index(context, event)
                if hovered_index is not None:
                    self.report({'INFO'}, f"Selected LUT row {hovered_index+1}")
                    self.bridge.lut_property.selected_row = hovered_index+1 # 0-index to 1-index
                self.reset_lut()
                
                if context.area is not None:
                    context.area.tag_redraw() # ensure the panel(s) update
                    w.cursor_modal_restore()
                return {'FINISHED'}
                
            # 3. Handle cancellation event (Escape Key)
            elif event.type in {'ESC', 'RIGHTMOUSE'}:
                self.report({'INFO'}, "LUT selection cancelled")
                self.reset_lut()
                w.cursor_modal_restore()
                return {'CANCELLED'}

            # Keep running the modal loop if no termination conditions are met
            return {'PASS_THROUGH'}
        except:
            self.reset_lut() # make sure that we don't destroy LUTs no matter what
            raise

    def invoke(self, context, event)-> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        ao = context.active_object
        assert ao is not None
        mg = accurate_shader.find_main_group(ao)
        assert mg is not None
        lut_node = mg.get_primary_lut_texture_node()
        assert lut_node is not None
        lut_image = lut_node.image
        assert lut_image is not None

        self.bridge = BPYLUTBridge.get_from_windowmanager(context.window_manager, lut_image)
        self.color_phase = 0.0
        self.target_object = ao
        self.target_lut = lut_image
        self.original_LUT = image_util.lut_from_blender_image(lut_image)
        self.target_material = mg
        idmask = mg.get_idmask()
        assert idmask is not None
        self.target_idmask = idmask

        # Tell the Window Manager to start tracking events for this modal
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
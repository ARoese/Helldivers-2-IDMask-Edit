from pathlib import Path
from typing import List, Literal, Tuple, Self

import bpy
from bpy.types import Context
from .utils import accurate_shader
from .utils import images as image_util
from .utils.custom_types import *
from ..utils import sdf_mask

class PatchAccurate(bpy.types.Operator):
    bl_idname = "hd2visual.patch_accurate_shader"
    bl_label = "Patch Accurate Shader"
    bl_options = {'REGISTER', 'UNDO'}

    as_sdf: bpy.props.BoolProperty(default=False, name="is SDF", description="Upscale the SDF to a higher resolution") #type: ignore
    sdf_upscale_target: bpy.props.IntProperty(name="new resolution", default=1024, min=32, description="The new SDF resolution.") #type: ignore
    
    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        ao = context.active_object
        so = context.selected_objects

        assert ao is not None and so
        assert isinstance(ao.data, bpy.types.Mesh)

        objects = [*so]
        objects.remove(ao)
        objects = [ao, *objects]

        for object in objects:
            mg = accurate_shader.find_main_group(object)
            assert mg is not None

            id_mask = mg.get_idmask()
            assert id_mask is not None

            if self.as_sdf:
                id_mask = id_mask.upscale_at((self.sdf_upscale_target, self.sdf_upscale_target))

            # make the id mask images from the array
            id_mask_channels = image_util.make_id_mask_images(id_mask, object.name)
            mg.set_idmask_images(id_mask_channels)

            # upscale the pattern mask if necessary
            if self.as_sdf:
                pattern_mask_node = mg.find_pattern_mask_node()
                assert pattern_mask_node is not None
                assert pattern_mask_node.image is not None
                pattern_mask = image_util.pillow_image_from_blender_image(pattern_mask_node.image)
                pattern_mask = sdf_mask.sdf_channel_to_straight(pattern_mask, (self.sdf_upscale_target, self.sdf_upscale_target))
                pattern_mask_node.image = image_util.blender_image_from_pillow_image(pattern_mask, f"{object.name}-pm")
            

        return {'FINISHED'}

    @classmethod
    def poll(cls, context: Context) -> bool:
        ao = context.active_object
        so = context.selected_objects

        if ao is None:
            cls.poll_message_set("An object must be selected")
            return False

        if any(o.type != "MESH" for o in [ao, *so]):
            cls.poll_message_set("All selected objects need meshes")
            return False

        objects = [*so]
        objects.remove(ao)
        objects = [ao, *objects]
        for object in objects:
            mg = accurate_shader.find_main_group(object)
            if mg is None:
                cls.poll_message_set(f"Failed to find main group for object {object.name}")
                return False

            id_mask = mg.get_idmask()
            if id_mask is None:
                cls.poll_message_set(f"Failed to get IDMask for object {object.name}")
                return False

            pattern_mask_node = mg.find_pattern_mask_node()
            if pattern_mask_node is None:
                cls.poll_message_set(f"Failed to get pattern mask node for object {object.name}")
                return False

            if pattern_mask_node is None:
                cls.poll_message_set(f"Failed to get pattern mask image for object {object.name}")
                return False
        
        return True
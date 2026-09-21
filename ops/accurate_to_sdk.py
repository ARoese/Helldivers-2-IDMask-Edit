from pathlib import Path
from typing import List, Literal, Tuple, Self

import bpy
from bpy.types import Context, Event
from PIL import Image as PILImage
from PIL.Image import Image as PILImageType
from .utils import atlas_pieces
from .utils.custom_types import *
from .utils.sdk_material_interface import poll_create_sdk_lut_material

class AccurateToSDK(bpy.types.Operator):
    bl_idname = "hd2visual.accurate_to_sdk"
    bl_label = "Accurate to SDK"
    bl_options = {'REGISTER', 'UNDO'}

    # Properties to store the selection
    directory: bpy.props.StringProperty(
        name="Output Folder",
        subtype='DIR_PATH'
    ) #type: ignore
    
    # Filter to show only folders in the file browser
    filter_folder: bpy.props.BoolProperty(
        default=True,
        options={'HIDDEN'}
    ) #type: ignore

    to_sdf: bpy.props.BoolProperty(default=False, name="as SDF", description="Export to a SDF at a lower resolution. See the README to understand what this means.") #type: ignore
    sdf_downscale_target: bpy.props.IntProperty(name="SDF resolution", default=256, min=32, description="The resolution of the exported SDF.") #type: ignore

    def draw(self, context):
        layout = self.layout
        assert layout is not None

        layout.label(text="Select a directory to export the assets to", icon='INFO')
        
        layout.prop(self, "to_sdf")
        if self.to_sdf:
            layout.prop(self, "sdf_downscale_target")

    def invoke(self, context: Context, event: Event) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        ao = context.active_object
        so = context.selected_objects

        assert ao is not None and so
        assert isinstance(ao.data, bpy.types.Mesh)

        objects = [*so]
        objects.remove(ao)
        objects = [ao, *objects]

        # largest_pattern_mask_dim = max(piece[2].size[0] for piece in pieces)
        sdf_downscale_target = self.sdf_downscale_target if self.to_sdf else None
        pieces = [atlas_pieces.from_bpy_obj(obj, sdf_downscale_target) for obj in objects]
        assert len(pieces) == len(objects)

        output_dir = Path(self.directory)

        for piece in pieces:
            primary_lut_path = output_dir / f"{ao.name}-primary-lut.dds"
            with open(primary_lut_path, 'wb') as out_file:
                out_file.write(piece.primary_lut.to_dds().getbuffer())
            
            shared_primary_lut = bpy.data.images.load(primary_lut_path.as_posix(), check_existing=False)
            piece.apply_sdk_material(shared_primary_lut, output_dir)

        # Let the user do this themselves. That way, they can decide what needs to be part of what unit
        #bpy.ops.object.join()
        return {'FINISHED'}

    @classmethod
    def poll(cls, context: Context) -> bool:
        ao = context.active_object
        so = context.selected_objects

        if any(o.type != "MESH" for o in [ao, *so]):
            cls.poll_message_set("All selected objects need meshes")
            return False
        
        if (reason := poll_create_sdk_lut_material()) is not None:
            cls.poll_message_set(reason)
            return False
        
        return True
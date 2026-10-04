from pathlib import Path
from typing import List, Literal, Tuple, Self

import bpy
from bpy.types import Context, Event
from .utils import atlas_pieces
from .utils.custom_types import *
from .utils import sdk_material_interface
from ..utils import customization_armor_sets

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
    add_lut_to_patch: bpy.props.BoolProperty(
        name="Add LUT to patch",
        default=True, 
        description="Attempt to identify the object(s) being merged via HD2 custom properties, and automatically replace the correct LUT with the generated atlas"
    ) #type: ignore

    def draw(self, context):
        layout = self.layout
        assert layout is not None

        layout.label(text="Select a directory to export the assets to", icon='INFO')
        layout.prop(self, "add_lut_to_patch")
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

        sdf_downscale_target = self.sdf_downscale_target if self.to_sdf else None
        pieces = [atlas_pieces.from_bpy_obj(obj, sdf_downscale_target) for obj in objects]
        assert len(pieces) == len(objects)

        output_dir = Path(self.directory)

        for piece in pieces:
            primary_lut_path = output_dir / f"{ao.name}-primary-lut.dds"
            with open(primary_lut_path, 'wb') as out_file:
                out_file.write(piece.primary_lut.to_dds().getbuffer())
            
            shared_primary_lut = bpy.data.images.load(primary_lut_path.as_posix(), check_existing=False)
            if self.add_lut_to_patch:
                object_id = sdk_material_interface.get_hd2_object_id(piece.obj)
                if object_id is None:
                    raise Exception(f"Could not find object ID for '{piece.obj.name}'. Copy helldivers 2 custom properties to one of your objects or uncheck the 'Add LUT to patch' checkbox.")
                lut_id = customization_armor_sets.find_lut_for_obj(object_id)
                if lut_id is None:
                    raise Exception(f"Could not find material LUT for object ID 0x{object_id:x} ({object_id})")
                archive_id, lut_id = lut_id

                # attempt to automatically add the shared LUT to the patch
                print(f"LUT for object 0x{object_id:x} ({object_id}) is 0x{lut_id:x} ({lut_id}) in archive 0x{archive_id:x}")
                print(f"loading archive 0x{archive_id:x}")
                sdk_material_interface.load_archive(archive_id)
                print(f"Adding LUT atlas to patch as 0x{lut_id:x}")
                sdk_material_interface.add_dds_to_patch(lut_id, primary_lut_path)
                
            piece.unpack()
            piece.apply_sdk_material(shared_primary_lut, output_dir)

        return {'FINISHED'}

    @classmethod
    def poll(cls, context: Context) -> bool:
        ao = context.active_object
        so = context.selected_objects

        if any(o.type != "MESH" for o in [ao, *so]):
            cls.poll_message_set("All selected objects need meshes")
            return False
        
        if (reason := sdk_material_interface.poll_create_sdk_lut_material()) is not None:
            cls.poll_message_set(reason)
            return False
        
        return True
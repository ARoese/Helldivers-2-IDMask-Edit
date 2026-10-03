from pathlib import Path
from typing import List, Literal, Tuple, Self

import bpy
from bpy.types import Context, Event
from PIL import Image as PILImage
from PIL.Image import Image as PILImageType
from .utils import atlas_pieces
from .utils.custom_types import *
from .utils import sdk_material_interface
from ..utils import customization_armor_sets

# TODO: This is creating images (normals, etc) with broken empty paths. The issue does not become apparent until the SECOND time a merge is performed.
# TODO: It is probably related to the ensure_not_unpacked_exr code, but not sure
class ComplexMerge(bpy.types.Operator):
    bl_idname = "hd2visual.complex_merge"
    bl_label = "Complex Merge"
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

        layout.label(text="Select a directory to export the merge assets to", icon='INFO')

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

        # collect these early to fail fast
        object_ids = set([obj_id for obj in objects if (obj_id := sdk_material_interface.get_hd2_object_id(obj)) is not None])
        object_luts: dict[int, Tuple[int, int]] = dict()
        for object_id in object_ids:
            lut_id = customization_armor_sets.find_lut_for_obj(object_id)
            if lut_id is not None:
                object_luts[object_id] = lut_id
            elif self.add_lut_to_patch:
                raise Exception(f"Could not find material LUT for object ID 0x{object_id:x} ({object_id})")
        if len(object_luts) == 0 and self.add_lut_to_patch:
            raise Exception("Could not find any material LUTs to replace. Copy helldivers 2 custom properties to one of your objects or uncheck the 'Add LUT to patch' checkbox.")
            
        sdf_downscale_target = self.sdf_downscale_target if self.to_sdf else None
        pieces = [atlas_pieces.from_bpy_obj(obj, sdf_downscale_target) for obj in objects]
        assert len(pieces) == len(objects)

        output_dir = Path(self.directory)
        for piece in pieces:
            piece.unpack()
        shared_primary_lut = atlas_pieces.atlas_luts(pieces)

        shared_primary_lut_path = output_dir / f"{ao.name}-primary-lut-atlas.dds"
        with open(shared_primary_lut_path, 'wb') as out_file:
            out_file.write(shared_primary_lut.to_dds().getbuffer())
        
        shared_primary_lut = bpy.data.images.load(shared_primary_lut_path.as_posix(), check_existing=False)

        for piece in pieces:
            piece.apply_sdk_material(shared_primary_lut, output_dir)

        # attempt to automatically add the shared LUT to the patch
        if self.add_lut_to_patch:
            loaded_archives: set[int] = set()
            for obj_id, (archive_id, lut_id) in object_luts.items():
                print(f"LUT for object 0x{obj_id:x} ({obj_id}) is 0x{lut_id:x} ({lut_id}) in archive 0x{archive_id:x}")
                print(f"Adding LUT atlas to patch as 0x{lut_id:x}")
                if archive_id not in loaded_archives:
                    print(f"loading archive 0x{archive_id:x}")
                    sdk_material_interface.load_archive(archive_id)
                    loaded_archives.add(archive_id)

                sdk_material_interface.add_dds_to_patch(lut_id, shared_primary_lut_path)

        # Let the user do this themselves. That way, they can decide what needs to be part of what unit
        #bpy.ops.object.join()
        self.report({'INFO'}, "Merge complete")
        return {'FINISHED'}

    @classmethod
    def poll(cls, context: Context) -> bool:
        ao = context.active_object
        so = context.selected_objects

        if ao is None or len(so) < 2:
            cls.poll_message_set("Multiple objects must be selected")
            return False

        if any(o.type != "MESH" for o in [ao, *so]):
            cls.poll_message_set("All selected objects need meshes")
            return False
        
        if not bpy.ops.object.join.poll(): #type: ignore # This poll call is valid, it's not not exposed in this type system
            cls.poll_message_set("Cannot join these objects (as if via ctrl+J)")
            return False
        
        if (reason := sdk_material_interface.poll_create_sdk_lut_material()) is not None:
            cls.poll_message_set(reason)
            return False
        
        return True
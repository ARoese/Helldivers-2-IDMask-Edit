from pathlib import Path
from typing import List, Literal, Tuple

import bpy
from bpy.types import Context, Event
from PIL import Image as PILImage
from PIL.Image import Image as PILImageType
import pprint

from .utils.images import lut_from_blender_image, ensure_not_unpacked_exr
from .utils import accurate_shader
from .utils.custom_types import *
from .utils.sdk_material_interface import create_sdk_lut_material, setup_sdk_lut_material, poll_create_sdk_lut_material
from .. import IDMask
from ..IDMask import PackedChannels as PackedChannelsType
from .. import LUT
from ..LUT import LUT as LUTType


AtlasPieces = Tuple[bpy.types.Object, PackedChannelsType, Image | None, LUTType, LUTType, Image, Image | None, Image | None]
'''(obj, id_mask, pattern_mask, primary_lut, secondary_lut, normal, decal, pattern_lut)'''

class ComplexMergeNoAtlas(bpy.types.Operator):
    bl_idname = "hd2visual.complex_merge_no_atlas"
    bl_label = "Complex Merge (without atlasing)"
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

    def invoke(self, context: Context, event: Event) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        context.window_manager.fileselect_add
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

        def get_pieces(obj: bpy.types.Object) -> AtlasPieces | None:
            # NOTE: This function is the slowest part of this code. Probably because of the subprocesses
            mg = accurate_shader.find_main_group(obj)
            if mg is None:
                return None
            
            print(f"assembling pieces for '{obj.name}'")
            
            id_mask = mg.get_idmask()
            primary_lut_node = mg.get_primary_lut_texture_node()
            secondary_lut_node = mg.get_secondary_lut_texture_node()
            normal_node = mg.get_normal_texture_node()
            pattern_mask_node = mg.find_pattern_mask_node()
            decal_node = mg.get_decal_texture_node()
            pattern_lut_node = mg.get_pattern_lut_texture_node()

            if id_mask is None:
                print("failed to find id mask")
                return None
            
            if primary_lut_node is None or primary_lut_node.image is None:
                print("failed to find primary lut")
                return None
            
            if secondary_lut_node is None or secondary_lut_node.image is None:
                print("failed to find secondary lut")
                return None

            if normal_node is None or normal_node.image is None:
                print("failed to find normal")
                return None
            
            if decal_node is None:
                decal = None
            else:
                decal = decal_node.image

            if pattern_lut_node is None:
                pattern_lut = None
            else:
                pattern_lut = pattern_lut_node.image
            
            print("Loading LUTs")
            primary_lut = lut_from_blender_image(primary_lut_node.image)
            secondary_lut = lut_from_blender_image(secondary_lut_node.image)
            print("done Loading LUTs")

            idmd = id_mask.dim()
            if idmd[0] != idmd[1]:
                raise ValueError("id mask is not square. It cannot be atlased.")
            
            normal = normal_node.image
            if normal.size[0] != normal.size[1]:
                raise ValueError("normal is not square. It cannot be atlased.")
            
            if pattern_mask_node is not None and pattern_mask_node.image is not None:
                pattern_mask = pattern_mask_node.image
            else:
                pattern_mask = None
            
            def ensure_unpacked(img: Image|None):
                if img is None:
                    return
                
                if img.packed_file is not None:
                    img.unpack(method="WRITE_LOCAL")
                print("filepath after unpacking: ", img.filepath)
                ensure_not_unpacked_exr(img)
            
            ensure_unpacked(pattern_mask)
            ensure_unpacked(normal)
            ensure_unpacked(decal)
            ensure_unpacked(pattern_lut)

            #normal.save(Path("test_outputs/example_normal.png"))
            res: AtlasPieces = (obj, id_mask, pattern_mask, primary_lut, secondary_lut, normal, decal, pattern_lut)
            # pprint.pprint(res)
            print("assembled pieces: ")
            pprint.pprint(res)
            return res

        # largest_pattern_mask_dim = max(piece[2].size[0] for piece in pieces)
        pieces = [ps for obj in objects if (ps := get_pieces(obj)) is not None]
        assert len(pieces) == len(objects)

        max_idmask_dim = max(piece[1].dim()[0] for piece in pieces)
        max_idmask_dim = (max_idmask_dim, max_idmask_dim)
        lut_stack = pieces[0][3].clone() # start with the primary object's LUT
        secondary_lut_stack = pieces[0][4].clone() # start with the primary object's LUT
        global_pattern_lut = None
        for idx, piece in enumerate(pieces):
            obj, id_mask, pattern_mask, primary_lut, secondary_lut, normal, decal, pattern_lut = piece
            if piece[7] is not None:
                global_pattern_lut = piece[7]
            
            # extend LUTs
            print(f"Stacking LUTs for {obj.name}")
            if idx != 0:
                lut_stack.extend(primary_lut)
                secondary_lut_stack.extend(secondary_lut)

        output_dir = Path(self.directory)
        shared_primary_lut_path = output_dir / f"{ao.name}-primary-lut-atlas.dds"
        with open(shared_primary_lut_path, 'wb') as out_file:
            out_file.write(lut_stack.to_dds().getbuffer())
        with open(output_dir / f"{ao.name}-secondary-lut-atlas.dds", 'wb') as out_file:
            out_file.write(secondary_lut_stack.to_dds().getbuffer())
        
        shared_primary_lut = bpy.data.images.load(shared_primary_lut_path.as_posix(), check_existing=False)

        for idx, piece in enumerate(pieces):
            obj, id_mask, pattern_mask, primary_lut, secondary_lut, normal, decal, pattern_lut = piece
            assert isinstance(obj.data, bpy.types.Mesh)

            print(f"Creating lut material for {obj.name}")

            extended_id_mask = IDMask.empty_channel_pack(depth=(idx+1)*8, dim=max_idmask_dim)
            extended_id_mask.paste(id_mask, depth=idx*8)

            id_mask_path = output_dir / f"{obj.name}-idmask.dds"
            with open(id_mask_path, 'wb') as out_file:
                out_file.write(extended_id_mask.to_array().getbuffer())

            extended_id_mask_img = bpy.data.images.load(id_mask_path.as_posix(), check_existing=False)

            lut_material = create_sdk_lut_material()
            setup_sdk_lut_material(
                lut_material,
                decal,
                pattern_lut,
                normal,
                pattern_mask,
                extended_id_mask_img,
                shared_primary_lut
            )

            obj.material_slots[0].material = lut_material

        bpy.ops.object.join()
        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        ao = context.active_object
        so = context.selected_objects

        if ao is None or not so:
            cls.poll_message_set("Multiple objects must be selected")
            return False

        if any(o.type != "MESH" for o in [ao, *so]):
            cls.poll_message_set("All selected objects need meshes")
            return False
        
        if not bpy.ops.object.join.poll(): #type: ignore # This poll call is valid, it's not not exposed in this type system
            cls.poll_message_set("Cannot join these objects (as if via ctrl+J)")
            return False
        
        if (reason := poll_create_sdk_lut_material()) is not None:
            cls.poll_message_set(reason)
            return False
        
        return True
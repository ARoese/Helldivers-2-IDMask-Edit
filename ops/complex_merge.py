from pathlib import Path
from typing import List, Literal, Tuple

import bpy
from bpy.types import Context, Event
from PIL import Image as PILImage
from PIL.Image import Image as PILImageType
import pprint

from .utils.images import lut_from_blender_image, pillow_image_from_blender_image, rgba_pillow_image_from_blender_image
from .utils import accurate_shader
from .utils.custom_types import *
from .. import IDMask
from ..IDMask import PackedChannels as PackedChannelsType
from .. import LUT
from ..LUT import LUT as LUTType
from .. import square_packing
from ..square_packing import Square

def uv_scale_translate(layer: bpy.types.MeshUVLoopLayer, scale: float, translate: Tuple[float, float], wrap_range=True):
    out_of_range = 0
    for coord in layer.uv:
        if (
            coord.vector.x > 1.0 or 
            coord.vector.x < 0.0 or
            coord.vector.y > 1.0 or
            coord.vector.y < 0.0
        ): 
            out_of_range += 1
            if wrap_range:
                coord.vector.x %= 1.0
                coord.vector.y %= 1.0
        coord.vector.x *= scale
        coord.vector.y *= scale

        coord.vector.x += translate[0]
        coord.vector.y += translate[1]
    
    if out_of_range:
        warning = f"Warning: {out_of_range} uv coordinates are outside of the [0,1] range."
        if wrap_range:
            warning = f"{warning} They have been wrapped, but you should verify that they work on the atlas."
        print(warning)

AtlasPieces = Tuple[bpy.types.Object, PackedChannelsType, PILImageType | None, LUTType, LUTType, PILImageType]

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
            
            id_mask = mg.get_idmask()
            primary_lut_node = mg.get_primary_lut_texture_node()
            secondary_lut_node = mg.get_secondary_lut_texture_node()
            normal_node = mg.get_normal_texture_node()
            pattern_mask_node = mg.find_pattern_mask_node()

            print("id mask:", id_mask)
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

            primary_lut = lut_from_blender_image(primary_lut_node.image)
            secondary_lut = lut_from_blender_image(secondary_lut_node.image)

            idmd = id_mask.dim()
            if idmd[0] != idmd[1]:
                raise ValueError("id mask is not square. It cannot be atlased.")
            
            normal = normal_node.image
            if normal.size[0] != normal.size[1]:
                raise ValueError("normal is not square. It cannot be atlased.")
            
            if pattern_mask_node is not None and pattern_mask_node.image is not None:
                pattern_mask = pattern_mask_node.image
                if pattern_mask.size[0] != pattern_mask.size[1]:
                    raise ValueError("pattern mask is not square. It cannot be atlased.")
                pattern_mask = pillow_image_from_blender_image(pattern_mask_node.image)
            else:
                pattern_mask = None

            normal = rgba_pillow_image_from_blender_image(normal)
            

            #normal.save(Path("test_outputs/example_normal.png"))
            res = (obj, id_mask, pattern_mask, primary_lut, secondary_lut, normal)
            # pprint.pprint(res)
            return res
        
        # do square packing
        pieces = [piece for obj in objects if (piece := get_pieces(obj)) is not None]
        
        assert len(pieces) == len(objects)

        atlas_squares = [Square(i, piece[1].dim()[0]) for i,piece in enumerate(pieces)]
        container_size_guess = max(atlas_squares, key=lambda s: s.size()).size()
        container = Square("Container", container_size_guess)
        def force_find_packing():
            for attempt in range(8):
                container.size_exponent += 1
                packing = square_packing.try_pack_squares(atlas_squares, container)
                if packing is not None:
                    return packing
            
            raise Exception("Failed to find a valid packing")

        def calc_normal_map_scale_factor(pieces: List[AtlasPieces]) -> int:
            def get_ratio(id_mask: PackedChannelsType, normal: PILImageType) -> int:
                raw_ratio = normal.size[0] / id_mask.dim()[0]
                int_ratio = int(raw_ratio)

                if raw_ratio != int_ratio:
                    raise ValueError(f"normal/idmask size ratio is non-integer ({raw_ratio})")
                return int_ratio
            
            ratios = [get_ratio(piece[1], piece[5]) for piece in pieces]
            return max(ratios)
        
        packing = force_find_packing()
        # sort placements in ascending order, so that the placement for piece 0 comes first, etc
        packing.sort(key=lambda p: p.square.id) 
        
        nmsf = calc_normal_map_scale_factor(pieces)
        normal_map_dim = container.size()*nmsf

        # largest_pattern_mask_dim = max(piece[2].size[0] for piece in pieces)
        
        idmask_atlas = IDMask.empty_channel_pack(depth=len(objects)*8, dim=(container.size(), container.size()))
        pattern_mask_atlas = PILImage.new("L", (container.size(), container.size()))
        lut_stack = pieces[0][3].clone() # start with the primary object's LUT
        secondary_lut_stack = pieces[0][4].clone() # start with the primary object's LUT
        # The alpha is actually relevant for this normal map. I think it's an embedded curvature map or something.
        normal_map_atlas = PILImage.new("RGBA", (normal_map_dim, normal_map_dim), (128, 128, 255, 128)) 
        for placement in packing:
            # idmask channels are 1:1 with LUT rows. The LUT needs to be pasted in the same order as the IDMask channels
            piece_idx = placement.square.id
            assert isinstance(piece_idx, int)
            
            obj, id_mask, pattern_mask, primary_lut, secondary_lut, normal = pieces[piece_idx]
            assert isinstance(obj.data, bpy.types.Mesh)

            print(f"Pasting atlas piece for {obj.name}")

            uv_layer = obj.data.uv_layers[0]
            scale_factor = id_mask.dim()[0] / container.size()
            # bottom left corner is unchanged when scaled here,
            # so we move it to the bottom left corner of the placement
            px, py = placement.bottom_left() 
            # scale to 0-1 range, and map the y coordinate into blender's coordinate system
            px, py = px / container.size(), 1.0 - (py / container.size())

            # move uvs
            uv_scale_translate(uv_layer, scale_factor, (px,py))
            # paste IDMask into atlas
            idmask_atlas.paste(id_mask, placement.top_left(), piece_idx*8)
            if pattern_mask is not None:
                pattern_mask_atlas.paste(pattern_mask, placement.top_left())

            # paste normal map into atlas
            #print("normal map scale factor:", nmsf)
            scaled_normal_size = tuple(dim*nmsf for dim in id_mask.dim()) # using id mask here is not a mistake
            #print("scaled normal size: ", scaled_normal_size)
            #print("normal atlas dim:", normal_map_atlas.size)
            scaled_normal = normal.resize(scaled_normal_size)
            normal_corner = tuple(coord*nmsf for coord in placement.top_left())
            assert len(normal_corner) == 2
            normal_map_atlas.paste(scaled_normal, normal_corner)

            # extend primary LUT
            if piece_idx != 0:
                lut_stack.extend(primary_lut)
                secondary_lut_stack.extend(secondary_lut)
        
        idmask_atlas.save_channels(Path("test_outputs/channels/"), name="atlas_channels", file_type="png")
        target_array = idmask_atlas.to_array()

        output_dir = Path(self.directory)
        with open(output_dir / f"{ao.name}-lut-atlas.dds", 'wb') as out_file:
            out_file.write(lut_stack.to_dds().getbuffer())
        with open(output_dir / f"{ao.name}-secondary-lut-atlas.dds", 'wb') as out_file:
            out_file.write(secondary_lut_stack.to_dds().getbuffer())
        with open(output_dir / f"{ao.name}-idmask-atlas.dds", 'wb') as out_file:
            out_file.write(target_array.getbuffer())

        normal_map_atlas.save(output_dir / f"{ao.name}-normal-atlas.png", format="png")
        pattern_mask_atlas.save(output_dir / f"{ao.name}-pattern-mask-atlas.png", format="png")


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
        
        return True
from pathlib import Path
from typing import List, Literal, Tuple, Self
import pprint

import bpy
from bpy.types import Context, Event
from PIL import Image as PILImage
from PIL.Image import Image as PILImageType

from .images import lut_from_blender_image, ensure_not_unpacked_exr
from . import accurate_shader
from . import images as image_utils
from .custom_types import *
from .sdk_material_interface import create_sdk_lut_material, setup_sdk_lut_material, poll_create_sdk_lut_material
from ...utils import IDMask
from ...utils.IDMask import PackedChannels as PackedChannelsType
from ...utils import LUT
from ...utils.LUT import LUT as LUTType
from ...utils import sdf_mask

from . import images as image_utils

class AtlasPieces:
    obj: bpy.types.Object
    id_mask: PackedChannelsType
    pattern_mask: Image | None
    primary_lut: LUTType
    secondary_lut: LUTType
    normal: Image
    decal: Image | None
    pattern_lut: Image | None

    def __init__(
            self,
            obj: bpy.types.Object, 
            id_mask: PackedChannelsType, 
            pattern_mask: Image | None, 
            primary_lut: LUTType, 
            secondary_lut: LUTType, 
            normal: Image, 
            decal: Image | None, 
            pattern_lut: Image | None
        ):
        self.obj = obj
        self.id_mask = id_mask
        self.pattern_mask = pattern_mask
        self.primary_lut = primary_lut
        self.secondary_lut = secondary_lut
        self.normal = normal
        self.decal = decal
        self.pattern_lut = pattern_lut

    def optimize_lut(self):
        # trim off LUT rows that have no mask to match with
        while self.primary_lut.dim()[1] > self.id_mask.num_channels():
            print(f"'{self.obj.name}': Trimming bottom LUT row because it has no accompanying IDMask channel")
            self.primary_lut.del_row(self.primary_lut.dim()[1]-1)

        # trim off LUT rows whose corresponding IDMask channels are blank (unused LUT row)
        for channel_idx in reversed(range(len(self.id_mask.channels))):
            # when checking for bounding box, use a very forgiving alpha test to prevent accidental exclusions
            a_tested = self.id_mask.channels[channel_idx].point(lambda p: 255 if p > 60 else 0) #type: ignore
            if a_tested.getbbox() is None: # if the channel is completely blank
                print(f"'{self.obj.name}': Trimming LUT row {channel_idx} because its IDMask does not paint anywhere (unused LUT row)")
                self.primary_lut.del_row(channel_idx)
                self.id_mask.delete(channel_idx)

    def inherit_lut(self, pieces: List[Self]) -> bool:
        for other_piece in pieces:
            if other_piece.primary_lut.eq(self.primary_lut):
                self.primary_lut = other_piece.primary_lut
                return True
        return False

    def generate_id_mask(self, prior_depth: int):
        extended_id_mask = IDMask.empty_channel_pack(depth=prior_depth, dim=self.id_mask.dim()).extended([self.id_mask])
        self.id_mask = extended_id_mask

    def apply_sdk_material(self, shared_primary_lut: Image, output_dir: Path):
        assert isinstance(self.obj.data, bpy.types.Mesh)
        print(f"Creating lut material for {self.obj.name}")

        id_mask_path = output_dir / f"{self.obj.name}-idmask.dds"
        with open(id_mask_path, 'wb') as out_file:
            out_file.write(self.id_mask.to_array().getbuffer())

        pattern_mask_path = output_dir / f"{self.obj.name}-patternmask.png"
        if self.pattern_mask is not None:
            self.pattern_mask.save(filepath=pattern_mask_path.as_posix())
        with open(id_mask_path, 'wb') as out_file:
            out_file.write(self.id_mask.to_array().getbuffer())

        extended_id_mask_img = bpy.data.images.load(id_mask_path.as_posix(), check_existing=False)

        lut_material = create_sdk_lut_material()
        setup_sdk_lut_material(
            lut_material,
            self.decal,
            self.pattern_lut,
            self.normal,
            self.pattern_mask,
            extended_id_mask_img,
            shared_primary_lut
        )

        self.obj.material_slots[0].material = lut_material

def from_bpy_obj(obj: bpy.types.Object, sdf_downscale_target: int | None) -> AtlasPieces:
    mg = accurate_shader.find_main_group(obj)
    if mg is None:
        raise Exception(f"failed to find accurate shader while processing '{obj.name}'")
    
    print(f"assembling pieces for '{obj.name}'")
    
    id_mask = mg.get_idmask()
    primary_lut_node = mg.get_primary_lut_texture_node()
    secondary_lut_node = mg.get_secondary_lut_texture_node()
    normal_node = mg.get_normal_texture_node()
    pattern_mask_node = mg.find_pattern_mask_node()
    decal_node = mg.get_decal_texture_node()
    pattern_lut_node = mg.get_pattern_lut_texture_node()

    if id_mask is None:
        raise Exception(f"failed to find id mask while processing '{obj.name}'")
    
    if primary_lut_node is None or primary_lut_node.image is None:
        raise Exception(f"failed to find primary lut when processing '{obj.name}'")
    
    if secondary_lut_node is None or secondary_lut_node.image is None:
        raise Exception(f"failed to find secondary lut when processing '{obj.name}'")

    if normal_node is None or normal_node.image is None:
        raise Exception(f"failed to find normal when processing '{obj.name}'")
    
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
    
    normal = normal_node.image
    
    if pattern_mask_node is not None and pattern_mask_node.image is not None:
        pattern_mask = pattern_mask_node.image
    else:
        pattern_mask = None

    if sdf_downscale_target is not None:
        print(f"Downscale IDMask as ({sdf_downscale_target}, {sdf_downscale_target}) SDF")
        id_mask = id_mask.downscale_sdf((sdf_downscale_target, sdf_downscale_target))
        if pattern_mask is not None:
            pm_pil = image_utils.pillow_image_from_blender_image(pattern_mask)
            pm_sdf = sdf_mask.channel_into_sdf(pm_pil).resize((sdf_downscale_target, sdf_downscale_target))
            pattern_mask = image_utils.blender_image_from_pillow_image(pm_sdf, name=f"{obj.name}-cm-pattern-mask")
            pattern_mask.name = "complex merge pattern mask"
            pattern_mask.pack()
    
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
    res: AtlasPieces = AtlasPieces(obj, id_mask, pattern_mask, primary_lut, secondary_lut, normal, decal, pattern_lut)
    # pprint.pprint(res)
    print("assembled pieces: ")
    pprint.pprint(res)
    return res

def atlas_luts(pieces: List[AtlasPieces]) -> LUTType:
    primary_lut_stack = pieces[0].primary_lut.clone()
    for idx,piece in enumerate(pieces[1:]): # object 1 is exempt from optimization
        print(f"Processing {piece.obj.name}")
        # check if our LUT already exists deeper in the stack
        if not piece.inherit_lut(pieces[:idx]):
            # Optimize and try again
            piece.optimize_lut()
            if not piece.inherit_lut(pieces[:idx]):
                # if we still can't find rows that work, then append the new LUT onto the stack
                primary_lut_stack.extend(piece.primary_lut)

        # NOTE: we could sort merge objects by the popularity of their LUTs, in decreasing order. This
        # NOTE: will help minimize the IDMask stack depths

        prior_depth = 0
        for prior_piece in pieces[:idx+1]: # this intentionally includes ourselves as a stopping point
            if prior_piece.primary_lut == piece.primary_lut:
                piece.generate_id_mask(prior_depth)
                break
            else:
                prior_depth += prior_piece.primary_lut.dim()[1]

        piece.primary_lut = primary_lut_stack

    return primary_lut_stack
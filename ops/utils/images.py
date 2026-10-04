from typing import List, Callable, Tuple

import bpy
import numpy as np
from bpy.path import abspath, relpath
from bpy.types import ShaderNodeGroup
from tempfile import mkdtemp
from pathlib import Path
from pathlib import PurePosixPath
from PIL import Image as PILImage
from PIL.Image import Image as PILImageType
import re

from .custom_types import *
from ...utils import IDMask
from ...utils.IDMask import PackedChannels as PackedChannelsType
from ...utils import LUT
from ...utils.LUT import LUT as LUTType

from ...utils.itertools_ext import batched
import subprocess
from ...utils import env
import itertools

# TODO: Some of these functions are quite slow on large images. 4K is about the upper limit of usability. Improve this.
def convert_exr_image(image: Image) -> Image:
    if image.file_format != "OPEN_EXR":
        raise ValueError(f"Image '{image.name}' is not exr, so cannot convert it")

    safe_filename = re.sub(r'[^\w]', '_', image.name)
    fp = f"//textures/generated/{safe_filename}.png"
    # saving a copy of an image without is a bit annoying in bpy. Just use PIL
    pillow_image_from_blender_image(image).save(abspath(fp))
    return bpy.data.images.load(fp, check_existing=False)

def lut_from_blender_image(image: Image) -> LUTType:
    iterable_image_pixels = image.pixels[:] #type: ignore # This type is wrong. pixels is an iterable of float, not a float
    pixels = (tuple(pixel) for pixel in batched(iterable_image_pixels, 4))
    rows = [list(row) for row in batched(pixels, image.size[0])]
    rows.reverse() # blender coordinates are y-positive. Ours are Y-negative.
    
    return LUT.from_rows(rows)

def populate_blender_lut(lut: LUTType, image: Image):
    if not image.is_float:
        raise ValueError(f"Given image '{image.name}' is not a float image")

    if image.channels != 4:
        raise ValueError(f"Given image '{image.name}' does not have 4 channels")

    x,y = image.size
    image_dim = (x,y)
    if lut.dim() != image_dim:
        raise ValueError(f"Given image '{image.name}' does not match the LUT dimension. ({image_dim} != {lut.dim()})")

    pixels: List[float] = []
    for row in reversed(lut.rows()):
        for pixel in row:
            pixels.extend(pixel)

    image.pixels = pixels # type: ignore # This is actually a list[float]

def load_blender_mask_image_from_path(path: Path) -> bpy.types.Image:
    im = bpy.data.images.load(path.as_posix(), check_existing=False)
    im.name = path.stem
    im.pack()
    # This is important; Color space transforms on these will really mess up the shader's behavior
    im.colorspace_settings.name = "Non-Color" #type: ignore
    return im

# TODO: Use numpy for transfer instead of saving a temp file and loading it
def blender_image_from_pillow_image(image: PILImageType, name: str = "image") -> bpy.types.Image:
    td = mkdtemp()
    if True: 
        td_path = Path(td)
        image_path = td_path / f"{name}.png"
        image.save(image_path.as_posix())

        return load_blender_mask_image_from_path(image_path)

# TODO: Use numpy for transfer instead of saving a temp file and loading it
def make_id_mask_images(mask: PackedChannelsType, name: str) -> IDMaskImages:
    td = mkdtemp()
    # placeholder block for a `with TemporaryDirectory as td` statement. 
    # This is omitted because I don't want the directories getting cleaned up right now

    print(f"Converting idmask with {mask.num_channels()} channels to 8 blender images")
    # expect 8 images. If less, extend or truncate to match
    mask = mask.with_depth(8)

    if True: 
        td_path = Path(td)
        channel_paths = mask.save_channels(td_path, name)
        
        images = tuple(load_blender_mask_image_from_path(path) for path in channel_paths)

    assert len(images) == 8

    return images

# TODO: Use numpy for transfer instead of saving a temp file and loading it
def id_mask_array_from_images(images: IDMaskImages) -> PackedChannelsType:
    td = mkdtemp()
    # placeholder block for a `with TemporaryDirectory as td` statement. 
    # This is omitted because I don't want the directories getting cleaned up right now
    if True: 
        td_path = Path(td)
        
        # unpack them to the temp dir
        for image in images:
            out_name = (td_path / image.name).with_suffix(".png").as_posix()
            image.save(filepath=out_name)

        id_mask = IDMask.from_channels_dir(td_path)
    
    return id_mask

def pillow_image_from_blender_image(blend_image: bpy.types.Image) -> PILImageType:
    '''accepts an image with 1, 3, or 4 channels'''

    print(f"Converting {blend_image.name}")
    dim_x,dim_y = blend_image.size
    nchannels = blend_image.channels

    channel_modes = {
        1: "L",
        3: "RGB",
        4: "RGBA"
    }

    pixels = np.array(blend_image.pixels[:], dtype=np.float32) #type: ignore # This type is wrong. pixels is an iterable of float, not a float
    pixels = (pixels * 255).astype(np.uint8)
    pixels = pixels.reshape((dim_y, dim_x, nchannels))
    pixels = np.flipud(pixels)
    
    new_image = PILImage.fromarray(pixels, channel_modes[nchannels])
    return new_image

def rgba_pillow_image_from_blender_image(blend_image: bpy.types.Image) -> PILImageType:
    '''requires that the input image have RGBA channels on its own'''
    assert blend_image.channels == 4

    return pillow_image_from_blender_image(blend_image)

# TODO: Use numpy for transfer instead of saving a temp file and loading it
def id_mask_from_blender_channels(channels: List[bpy.types.Image]) -> PackedChannelsType:
    td = mkdtemp()
    if True:
        tdp = Path(td)

        channel_paths = [tdp / f"channel-{n+1}.png" for n in range(len(channels))]
        for channel, channel_path in zip(channels, channel_paths):
            channel.save(filepath=channel_path.as_posix())

        mask = IDMask.from_channels_dir(tdp)
        
        return mask

# TODO: Use numpy for transfer instead of saving a temp file and loading it
def id_mask_from_blender_strip(strip: bpy.types.Image) -> PackedChannelsType:
    '''
        converts a blender strip into an IDMask with 2 layers. If the mask is square, 1 layer is assumed.
    '''
    td = mkdtemp()
    if True:
        tdp = Path(td)

        strip_path = tdp / "strip.png"
        strip.save(filepath=strip_path.as_posix())

        mask = IDMask.from_file(strip_path)

        return mask.with_depth(8)
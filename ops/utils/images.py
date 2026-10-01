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

from .custom_types import *
from ...utils import IDMask
from ...utils.IDMask import PackedChannels as PackedChannelsType
from ...utils import LUT
from ...utils.LUT import LUT as LUTType

from ...utils.itertools_ext import batched
import subprocess
from ...utils import env
import itertools

def ensure_not_unpacked_exr(img: Image):
    if img.packed_file is not None:
        raise ValueError(f"Expected packed image. Given image {img.name} was not packed.")
    
    path = img.filepath_raw
    if ".exr" not in path:
        return
    
    path = Path(abspath(path))
    res = None
    try:
        res = subprocess.run([env.TEXCONV_BIN.as_posix(), "-ft", "dds", "-y", "-dx10", "-o", path.parent, "--", path.as_posix()], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        res.check_returncode()
    except Exception as e:
        out = res.stdout if res is not None else b"[No output]"
        out = out.decode()
        raise Exception(f"texconv failed:\n{out}") from e
    
    dds_path = path.with_suffix(".dds")
    if not dds_path.exists():
        raise Exception(f"texconv did not fail, but the file {dds_path.as_posix()} still does not exist")
    
    # do this so that relative/non-relative status is not affected
    img.filepath_raw = relpath(PurePosixPath(img.filepath_raw).with_suffix(".dds").as_posix())
    img.name = img.name.replace(".exr", ".dds")


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

def blender_image_from_pillow_image(image: PILImageType, name: str = "image_from_pil", is_data: bool = True) -> bpy.types.Image:
    pixel_array = np.asarray(image.convert("RGBA"), dtype=np.float32) / 255.0
    pixel_array = np.flipud(pixel_array)
    new_image = bpy.data.images.new(
        name=name,
        width=image.size[0],
        height=image.size[1],
        alpha=True,
        is_data=is_data
    )

    new_image.pixels.foreach_set(pixel_array.ravel()) # type: ignore # The pixels array has an incorrect type. It is float[], not float
    return new_image
    
def make_id_mask_images(mask: PackedChannelsType, name: str) -> IDMaskImages:
    print(f"Converting idmask with {mask.num_channels()} channels to 8 blender images")
    # expect 8 images. If less, extend or truncate to match
    mask = mask.with_depth(8)
    channels = tuple([blender_image_from_pillow_image(channel, f"{name}-{i+1}") for i,channel in enumerate(mask.channels)])

    assert len(channels) == 8

    return channels

#TODO: This still seems to be pretty slow. Not horribly so, but it could still do better.
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

    pixels = np.empty(dim_x * dim_y * 4, dtype=np.float32)
    blend_image.pixels.foreach_get(pixels) #type: ignore # This type is wrong. pixels is an iterable of float, not a float
    pixels = (pixels * 255).astype(np.uint8)
    pixels = pixels.reshape((dim_y, dim_x, nchannels))
    pixels = np.flipud(pixels)
    
    new_image = PILImage.fromarray(pixels, channel_modes[nchannels])
    return new_image

def rgba_pillow_image_from_blender_image(blend_image: bpy.types.Image) -> PILImageType:
    '''requires that the input image have RGBA channels on its own'''
    assert blend_image.channels == 4

    return pillow_image_from_blender_image(blend_image)

def id_mask_from_blender_channels(channels: List[bpy.types.Image]) -> PackedChannelsType:
    pillow_channels = [pillow_image_from_blender_image(channel) for channel in channels]
    return IDMask.PackedChannels(pillow_channels)

def id_mask_array_from_images(images: IDMaskImages) -> PackedChannelsType:
    return id_mask_from_blender_channels(list(images))

def id_mask_from_blender_strip(strip: bpy.types.Image) -> PackedChannelsType:
    '''
        converts a blender strip into an IDMask with 2 layers. If the mask is square, 1 layer is assumed.
    '''
    pillow_strip = pillow_image_from_blender_image(strip)
    x,y = pillow_strip.size
    n_layers = 1 if x == y else 2
    mask = IDMask.from_strip(pillow_strip, n_layers)
    return mask.with_depth(8)
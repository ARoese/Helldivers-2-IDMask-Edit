from typing import List, Callable, Tuple

import bpy
from bpy.path import abspath, relpath
from bpy.types import ShaderNodeGroup
from tempfile import mkdtemp
from pathlib import Path
from PIL import Image as PILImage
from PIL.Image import Image as PILImageType

from .custom_types import *
from ... import IDMask
from ...IDMask import PackedChannels as PackedChannelsType
from ... import LUT
from ...LUT import LUT as LUTType

from ...itertools_ext import batched
import subprocess
from ... import env

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
    img.filepath_raw = relpath(Path(img.filepath_raw).with_suffix(".dds").as_posix())
    img.name = img.name.replace(".exr", ".dds")


def lut_from_blender_image(image: Image) -> LUTType:
    iterable_image_pixels = image.pixels[:] #type: ignore # This type is wrong. pixels is an iterable of float, not a float
    pixels = (tuple(pixel) for pixel in batched(iterable_image_pixels, 4))
    rows = [list(row) for row in batched(pixels, image.size[0])]
    rows.reverse() # blender coordinates are y-positive. Ours are Y-negative.
    
    return LUT.from_rows(rows)

def make_id_mask_images(path: Path) -> IDMaskImages:
    if path.suffix == ".dds":
        mask = IDMask.from_array(path)
    else: # assume any other image type is a strip
        mask = IDMask.from_strip_path(path)

    name = path.stem

    td = mkdtemp()
    # placeholder block for a `with TemporaryDirectory as td` statement. 
    # This is omitted because I don't want the directories getting cleaned up right now
    if True: 
        td_path = Path(td)
        channel_paths = mask.save_channels(td_path, name)

        def load_image(path: Path) -> bpy.types.Image:
            im = bpy.data.images.load(path.as_posix(), check_existing=False)
            im.name = path.stem
            im.pack()
            # This is important; Color space transforms on these will really mess up the shader's behavior
            im.colorspace_settings.name = "Non-Color" #type: ignore
            return im
        
        images = tuple(load_image(path) for path in channel_paths)
    
    assert len(images) == 8
    return images

def save_id_mask_array_from_images(dest_path: Path, images: IDMaskImages):
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
    
    with open(dest_path, 'wb') as out_file:
        out_file.write(id_mask.to_array().getbuffer())

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

    iterable_image_pixels = blend_image.pixels[:] #type: ignore # This type is wrong. pixels is an iterable of float, not a float
    pixels = (tuple(pixel) for pixel in batched(iterable_image_pixels, nchannels))
    
    new_image = PILImage.new(channel_modes[nchannels], (dim_x,dim_y))
    for y in reversed(range(dim_y)):
        for x in range(dim_x):
            pixel = tuple(int(c*255) for c in next(pixels))
            if nchannels == 1:
                pixel = pixel[0] # L mode expects int, not Tuple[int]

            new_image.putpixel((x,y), pixel) # TODO: Using putpixel is slow. Prefer direct access if possible
    
    return new_image

def rgba_pillow_image_from_blender_image(blend_image: bpy.types.Image) -> PILImageType:
    '''requires that the input image have RGBA channels on its own'''
    assert blend_image.channels == 4

    return pillow_image_from_blender_image(blend_image)

def id_mask_from_blender_channels(channels: List[bpy.types.Image]) -> PackedChannelsType:
    td = mkdtemp()
    if True:
        tdp = Path(td)

        channel_paths = [tdp / f"channel-{n+1}.png" for n in range(len(channels))]
        for channel, channel_path in zip(channels, channel_paths):
            channel.save(filepath=channel_path.as_posix())

        mask = IDMask.from_channels_dir(tdp)
        if mask.num_channels() != 8:
            raise ValueError(f"id mask did not have 8 channels. Found {mask.num_channels()} channels instead")
        
        return mask
    
def id_mask_from_blender_strip(strip: bpy.types.Image, fix_long=True) -> PackedChannelsType:
    '''if fix_long is True, then the id mask is always read as if it was 2 layers deep. 
    So, a 256x1024 strip will still be read correctly. 
    This is done because some strips in the archive were incorrectly turned into these "long strips"
    '''
    td = mkdtemp()
    if True:
        tdp = Path(td)

        strip_path = tdp / "strip.png"
        strip.save(filepath=strip_path.as_posix())

        mask = IDMask.from_strip_path(strip_path, expect_2_layers=fix_long)
        if mask.num_channels() != 8:
            if not fix_long:
                raise ValueError(f"id mask did not have 8 channels. Found {mask.num_channels()} channels instead")
            


        return mask
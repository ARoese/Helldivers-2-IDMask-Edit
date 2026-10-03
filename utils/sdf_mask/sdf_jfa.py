'''Implementation of HD2 SDF generation using the Jump Flood Algorithm'''
from typing import Tuple

import pyopencl as cl
from pyopencl.tools import match_dtype_to_c_struct
from pyopencl import cltypes
from pyopencl.array import vec
from pathlib import Path

from PIL.Image import Image as PILImage
from PIL import Image
import numpy as np
from math import ceil

from functools import cache

@cache
def context_kernel() -> Tuple[cl.Context, cl.Kernel, cl.Kernel, cl.Kernel]:
    '''Build opencl context and sdf kernel. Future calls are cached to return the same objects.'''
    ctx = cl.create_some_context(interactive=False)
    print(f"Using device {ctx.devices[0]} for PyOpencl to compute sdf")
    print(f"Available devices: {str(ctx.devices)}")
    OPENCL_PROGRAM = open(Path(__file__).parent / "sdf_jfa.cl").read()
    built = cl.Program(ctx, OPENCL_PROGRAM).build()
    init_knl = built.init
    jfa_pass_knl = built.jfa_pass
    generate_image_knl = built.generate_image

    return (ctx, init_knl, jfa_pass_knl, generate_image_knl)

# Optimization notes:
# Average total exec time: ~490ms
# cl.create_image calls take ~150ms
# queue takes ~130ms to complete (kernel execs and memory copies
# match_dtype_to_c_struct takes ~200ms first time, then is negigable afterwards
# rest is probably PIL conversion back to "L"
# Ideal optimization target is probably vram memory usage. Reducing this will reduce bus contention 
# The SDFPixel struct is A LOT bigger than it needs to be, especially since bools are actually ints for compat.
# Estimated ~300MB minimum for a 4k image
def channel_into_sdf(channel: PILImage, spread_factor: float = 0.0315) -> PILImage:
    if spread_factor <= 0 or spread_factor > 1:
        raise ValueError(f"spread factor {spread_factor} outside range (0,1]")
    ctx,init_knl, jfa_pass_knl, generate_image_knl = context_kernel()
    image_shapes = channel.size
    queue = cl.CommandQueue(ctx)
    input_image_array = np.array(channel.convert("RGBA"), dtype=np.uint8)
    fmt = cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.UNORM_INT8)
    input_image = cl.create_image(
        ctx,
        cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, # type: ignore
        fmt,
        shape=image_shapes,
        hostbuf=input_image_array
    )

    out_image = np.empty_like(input_image_array, dtype=np.uint8)
    output_image = cl.create_image(
        ctx,
        cl.mem_flags.WRITE_ONLY, # type: ignore
        fmt,
        shape=image_shapes
    )

    scratch_pixel_type = np.dtype([
        ("initialized", np.int32),
        ("inside_shape", np.int32),
        ("is_edge", np.int32),
        ("nearest_edge", cltypes.int2)
    ])

    actual_scratch_pixel_type, c_decl = match_dtype_to_c_struct(
        ctx.devices[0], "SDFPixel", scratch_pixel_type
    )

    scratch_buffer = np.empty(shape=(channel.size[0]*channel.size[1]), dtype=actual_scratch_pixel_type)
    scratch_buffer_device = cl.Buffer(
        ctx,
        flags=cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR,
        hostbuf=scratch_buffer
    ) # don't bother copying here. The device will init it

    init_knl(queue, image_shapes, None, 
            input_image, 
            scratch_buffer_device
        )
    jump_dist = max(image_shapes)//2
    while jump_dist > 0:
        jfa_pass_knl(queue, image_shapes, None,
                np.int32(image_shapes[0]),
                np.int32(image_shapes[1]),
                np.int32(jump_dist),
                scratch_buffer_device
            )
        jump_dist //= 2
    generate_image_knl( queue, image_shapes, None,
        output_image,
        scratch_buffer_device,
        np.float32(spread_factor)
    )
    
    cl.enqueue_copy(queue, out_image, output_image, origin=(0,0), region=image_shapes)
    queue.finish()

    output_image = Image.fromarray(out_image).convert("L")
    return output_image

def sdf_channel_to_straight(channel: PILImage, new_dim: Tuple[int,int]) -> PILImage:
    return channel.resize(new_dim, resample=Image.Resampling.BILINEAR).point(lambda p: 255 if p > 127 else 0) # type: ignore

if __name__ == "__main__":
    import cProfile
    import pstats

    from .. import IDMask
    from ..env import ADDON_PATH
    from pathlib import Path
    from PIL import Image, ImageChops, ImageOps
    import time

    empty_pixel_mask = IDMask.from_file(Path("test/empty_pixel.png"))
    empty_pixel_mask.downscale_sdf((128,128))

    #blank_pm = Image.open(Path("test/blank-pm.png"))#.resize((128,128))
    #channel_into_sdf(blank_pm).resize((128,128)).show()
    
    test_id_mask = IDMask.from_strip(Image.open(Path("test/0xc89b26d36017d6e9.png")), 2)
    TARGET_MASK = 4
    original_channel = test_id_mask.channels[TARGET_MASK]
    #original_channel.show()
    HIGH_RES_DIM = (4098, 4098)
    high_res = sdf_channel_to_straight(original_channel, HIGH_RES_DIM)
    #straight.show()
    #profiler = cProfile.Profile()
    #profiler.enable()
    start_time = time.time_ns()
    sdf_result = channel_into_sdf(high_res)
    elapsed = time.time_ns() - start_time
    print(f"{elapsed/(1000*1000)}ms elapsed")
    sdf_recode = sdf_result.resize(original_channel.size)
    #sdf_result.show()
    #original_channel.show()
    #sdf_recode.show()
    #exit()
    #sdf_recode.show()

    diff = ImageChops.difference(sdf_recode, original_channel)
    if diff.getbbox():
        print(diff.getextrema())
        diff.point(lambda v: v).show()

    recode_high_res = sdf_channel_to_straight(sdf_recode, HIGH_RES_DIM)
    diff = ImageChops.difference(recode_high_res, high_res)
    if diff.getbbox():
        print(diff.getextrema())
        diff.point(lambda v: v).show()
    #invert_diff.show()
    #profiler.disable()
    #stats = pstats.Stats(profiler).sort_stats('tottime')
    #stats.print_stats(20)  # Limits output to the top 20 slowest functions
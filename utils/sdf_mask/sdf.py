from typing import Tuple

import pyopencl as cl
from pyopencl import cltypes
from pathlib import Path

from PIL.Image import Image as PILImage
from PIL import Image
import numpy as np
from math import ceil

from functools import cache

@cache
def context_kernel() -> Tuple[cl.Context, cl.Kernel]:
    '''Build opencl context and sdf kernel. Future calls are cached to return the same objects.'''
    ctx = cl.create_some_context(interactive=False)
    print(f"Using device {ctx.devices[0]} for PyOpencl to compute sdf")

    OPENCL_PROGRAM = open(Path(__file__).parent / "sdf.cl").read()
    sdf_knl = cl.Program(ctx, OPENCL_PROGRAM).build().sdf

    return (ctx, sdf_knl)

def channel_into_sdf(channel: PILImage, spread_factor: float = 0.03) -> PILImage:
    if spread_factor < 0 or spread_factor > 1:
        raise ValueError(f"spread factor {spread_factor} outside range [0,1]")
    spread_pixels = int(ceil(spread_factor*max(channel.size)))
    ctx,sdf_knl = context_kernel()
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

    sdf_knl(queue, image_shapes, None, input_image, output_image, np.uint32(spread_pixels))
    cl.enqueue_copy(queue, out_image, output_image, origin=(0,0), region=image_shapes)
    queue.finish()

    output_image = Image.fromarray(out_image).convert("L")
    return output_image

def sdf_channel_to_straight(channel: PILImage, new_dim: Tuple[int,int]) -> PILImage:
    # TODO: This doesn't appear to produce good results
    return channel.resize(new_dim, resample=Image.Resampling.BILINEAR).point(lambda p: 255 if p > 128 else 0) # type: ignore

if __name__ == "__main__":
    import cProfile
    import pstats

    from .. import IDMask
    from ..env import ADDON_PATH
    from pathlib import Path
    from PIL import Image

    test_id_mask = IDMask.from_strip(Image.open(Path("test/0xc89b26d36017d6e9.png")))
    TARGET_MASK = -1
    test_id_mask.channels[TARGET_MASK].show()
    straight = sdf_channel_to_straight(test_id_mask.channels[TARGET_MASK], (2048,2048))
    straight.show()
    #profiler = cProfile.Profile()
    #profiler.enable()
    channel_into_sdf(straight).show()
    #profiler.disable()
    #stats = pstats.Stats(profiler).sort_stats('tottime')
    #stats.print_stats(20)  # Limits output to the top 20 slowest functions
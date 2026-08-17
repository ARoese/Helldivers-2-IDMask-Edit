from typing import List, Tuple
from math import sqrt, ceil

from PIL.Image import Image as PILImage
from PIL import Image

def channel_into_sdf(channel: PILImage, spread_factor: float = 0.1) -> PILImage:
    if spread_factor < 0 or spread_factor > 1:
        raise ValueError("spread_factor must be in range [0,1]")
    sdf = channel.copy().convert("L")
    s_x,s_y = channel.size

    def is_inside(val: int) -> bool:
        return val > 128

    def within_bounds(coordinate: Tuple[int, int]) -> bool:
        return (
                coordinate[0] > 0 and coordinate[0] < s_x
            and coordinate[1] > 0 and coordinate[1] < s_y
            )

    loaded = channel.load()
    assert loaded is not None
    def getpixel(coordinate: tuple[int,int]) -> int:
        my_value = loaded[coordinate[0], coordinate[1]]
        assert isinstance(my_value, int)
        return my_value

    def signed_distance_to_boundary(coordinate: Tuple[int, int]) -> float:
        am_inside = is_inside(getpixel(coordinate))

        def uv_distance_to_boundary() -> float:
            def uv_distance_to(other: Tuple[int, int]) -> float:
                self_u = float(coordinate[0]) / s_x
                self_v = float(coordinate[1]) / s_y

                other_u = float(other[0]) / s_x
                other_v = float(other[1]) / s_y
                return sqrt((self_u-other_u)**2 + (self_v-other_v)**2)
    
            def relative_coordinate(offset: tuple[int,int]) -> tuple[int,int]:
                return (coordinate[0] + offset[0], coordinate[1] + offset[1])
            
            # TODO: Maybe use a more efficient algorithm to find the nearest opposite pixel
            opposite_distance: float | None = None
            
            def offer_coordinate(coordinate: Tuple[int,int]):
                nonlocal opposite_distance
                
                if not within_bounds(coordinate):
                    return
                
                # ^ xor: true only if operands are opposites.
                # I.E. one is true and the other is false. We only want to consider
                # pixels of OPPOSITE polarity
                if not (is_inside(getpixel(coordinate)) ^ am_inside):
                    return

                distance = uv_distance_to(coordinate)
                if distance >= spread_factor:
                    return
                
                if opposite_distance is None or opposite_distance > distance:
                    opposite_distance = distance
    
            max_square_size = int(ceil(max(channel.size)*spread_factor))
            #print(max_square_size)
            for size in range(3,max_square_size+1,2):
                #print(size)
                for x in range(size):
                    top = relative_coordinate((x,size))
                    bottom = relative_coordinate((x,-size))
                    #print(top, bottom)
                    offer_coordinate(top)
                    offer_coordinate(bottom)
    
                for y in range(1,size-1):
                    right = relative_coordinate((size,y))
                    left = relative_coordinate((-size,y))
                    offer_coordinate(right)
                    offer_coordinate(left)
    
                # optimization: all future iterations will have a greater distance
                if opposite_distance is not None:
                    return opposite_distance
    
            if opposite_distance is None:
                return spread_factor

        # NOTE: spread_factor is the maximum distance to a bounary
        # TODO: this following computation is a little wrong. Fix it
        signed_distance = (uv_distance_to_boundary() / spread_factor) / 2
        
        if am_inside: # inside pixels are > 0.5
            signed_distance = 0.5 + signed_distance
        else:
            signed_distance = 0.5 - signed_distance
        return signed_distance        
    i = 0
    
    for x in range(s_x):
        for y in range(s_y):
            coord = (x,y)
            sd = signed_distance_to_boundary(coord)
            sdf.putpixel(coord, int(sd*255))
            i+=1
            print(f"{i}")

    return sdf

def sdf_channel_to_straight(channel: PILImage, new_dim: Tuple[int,int] = (2048,2048)) -> PILImage:
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
    #test_id_mask.channels[TARGET_MASK].show()
    straight = sdf_channel_to_straight(test_id_mask.channels[TARGET_MASK], (128,128))
    #straight.show()
    profiler = cProfile.Profile()
    profiler.enable()
    channel_into_sdf(straight, spread_factor=0.05).show()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats(20)  # Limits output to the top 20 slowest functions
    
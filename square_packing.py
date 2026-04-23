'''Implements a square packing algorithm with the following constraints:
    1. Textures are always square
    2. Textures always have size 2^k
    3. The destination atlas has size 2^n
    4. The total area of all the textures doesn't exceed the area of the atlas

The implementation is based on this blog post: https://lisyarus.github.io/blog/posts/texture-packing.html
'''

from typing import Any, List, Tuple, Self
import math

Int2 = Tuple[int, int]

class Square:
    id: Any
    size_exponent: int
    def __init__(self, id: Any, size: int):
        size_exponent = int(math.log2(size))
        if 2**size_exponent != size:
            raise ValueError(f"Size must be a power of 2. Got {size}")
        
        self.id = id
        self.size_exponent = size_exponent
    
    def size(self) -> int:
        return 2**self.size_exponent 

class Placement:
    '''coordinate space is same as pillow; +x is right, +y is down'''
    x: int
    y: int
    square: Square
    def __init__(self, square: Square, loc: Int2):
        self.square = square
        x,y = loc
        self.x = x
        self.y = y

    def top_left(self) -> Int2:
        return (self.x,self.y)
    
    def bottom_left(self) -> Int2:
        size = self.square.size()
        return (self.x, self.y + size)
    
    def bottom_right(self) -> Int2:
        size = self.square.size()
        return (self.x + size, self.y + size)

    def overlaps(self, other: Self) -> bool:
        # use AABB
        stlx, stly = self.top_left()
        sbrx, sbry = self.bottom_right()

        otlx, otly = other.top_left()
        obrx, obry = other.bottom_right()
        if (
            sbrx <= otlx # I am completely to the left of other
            or obrx <= stlx # I am completely to the right of other
            or sbry <= otly # I am completely above other
            or stly <= obry # I am completely under other
            ):
            return False
        
        return True
    
    def completely_within(self, other: Self) -> bool:
        stlx, stly = self.top_left()
        sbrx, sbry = self.bottom_right()

        otlx, otly = other.top_left()
        obrx, obry = other.bottom_right()

        if (
            stlx >= otlx and # top left is inside
            stly >= otly and
            sbrx <= obrx and # bottom right is inside
            sbry <= obry 
        ):
            return True
        
        return False

def try_pack_squares(squares: List[Square], container: Square) -> List[Placement] | None:
    # if constraint is not met, this is impossible
    total_area = sum(square.size()**2 for square in squares)
    if total_area > container.size()**2:
        return None

    # sort in descending order by size
    squares.sort(key=lambda s: s.size_exponent, reverse=True)

    pen = [0,0]
    ladder = []
    result: List[Placement] = []
    for square in squares:
        size = square.size()

        # allocate a texture region
        result.append(Placement(square, (pen[0], pen[1])))

        # shift the pen to the right
        pen[0] += size

        # update the ladder
        if ladder and ladder[-1][1] == pen[1] + size:
            ladder[-1][0] = pen[0]
        else:
            ladder.append([pen[0], pen[1] + size])

        if (pen[0] == container.size()):
            # the pen hit the right edge of the atlas
            ladder.pop()

            pen[1] += size
            if ladder:
                pen[0] = ladder[-1][0]
            else:
                pen[0] = 0

    # ensure the result is always valid
    container_placement = Placement(container, (0,0))
    for i,placement in enumerate(result):
        for o_placement in result[i+1:]:
            assert not placement.overlaps(o_placement)
            assert placement.completely_within(container_placement)

    return result
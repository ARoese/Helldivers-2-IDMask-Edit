from typing import List, Tuple, Iterable, Self

from io import BytesIO
from pathlib import Path
import subprocess
import struct
import itertools
import pprint

from . import env

class LUTException(Exception):
    pass

Float4 = Tuple[float, float, float, float]

class LUT:
    '''R32G32B32A32_FLOAT lookup table. Follows PIL coordinate system; 0,0 is top left'''
    # hidden; Interact with this via a row-column interface
    # index order is [y][x] with the first y being the top row
    _channels: List[List[Float4]] 

    def __init__(self, pixels: List[List[Float4]]):
        self._channels = pixels

    def dim(self) -> Tuple[int, int]:
        y_dim = len(self._channels)
        x_dim = len(self._channels[0])
        return (x_dim, y_dim)

    def set_pixel(self, xy: Tuple[int, int], value: Float4):
        self._channels[xy[1]][xy[0]] = value

    def get_pixel(self, xy: Tuple[int, int]) -> Float4:
        return self._channels[xy[1]][xy[0]]
    
    def set_row(self, row: int, values: Iterable[Float4]):
        columns = range(self.dim()[0])
        for c,v in zip(columns, values):
            self.set_pixel((row,c),v)

    def get_row(self, row: int) -> List[Float4]:
        row_length = self.dim()[0]
        pixels = [
            self.get_pixel((col, row)) for col in range(row_length)
        ]

        assert len(pixels) == self.dim()[0]

        return pixels
    
    def rows(self) -> List[List[Float4]]:
        num_rows = self.dim()[1]

        rows = [self.get_row(row) for row in range(num_rows)]
        assert len(rows) == self.dim()[1]

        return rows

    
    def append_rows(self, rows: Iterable[Iterable[Float4]]):
        if not rows:
            return
        rows = [list(row) for row in rows]
        if not all(len(row) == len(rows[0]) for row in rows):
            pretty_rows = pprint.pformat(rows)
            lengths = "\n".join(str(len(r)) for r in rows)
            raise ValueError(f"Jagged matrix passed to append rows function. Row lengths: \n{lengths}")
        if not all(len(row) == self.dim()[0] for row in rows):
            x,y = len(rows[0]), len(rows)
            raise ValueError(f"Passed rows are not long enough. self: {self.dim()[0]}x{self.dim()[1]} passed: {x}x{y}")
        
        self._channels.extend(rows)
    
    def extend(self, other: Self):
        other_rows = other.rows()
        self.append_rows(other_rows)

    def as_matrix(self) -> bytes:
        # width, height as uint32
        width, height = self.dim()
        dims = struct.pack(">II", width, height)

        # pack into 4 4-byte floats representing RGBA
        pixels = [struct.pack(">ffff", *pixel) for pixel in itertools.chain.from_iterable(self._channels)]
        pixels = b"".join(pixels)

        output = b"".join([dims, pixels])
        assert(len(output) == 8 + width*height*4*4)
        return output

    def to_dds(self) -> BytesIO:
        output = BytesIO()

        matrix = self.as_matrix()

        res = None
        try:
            args = [env.LUTRANSLATE_BIN.as_posix(), "--to-dds"]
            res = subprocess.run(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE, input=matrix)
            res.check_returncode()
        except Exception as e:
            err_output = res.stderr if res is not None else b"[No output]"
            err_output = err_output.decode()
            raise LUTException(f"LUTranslate failed:\n{err_output}") from e
        
        output.write(res.stdout)
        return output

    def __copy__(self):
        return LUT(self._channels)

    def clone(self):
        return self.__copy__()

def from_matrix(matrix: bytes) -> LUT:
    if len(matrix) < 8:
        raise ValueError("LUT Matrix is too short to read header")
    dims_header, matrix = matrix[:8], matrix[8:]
    # width, height as uint32
    width, height = struct.unpack(">II", dims_header)

    if len(matrix) < width*height*4*4:
        raise ValueError("LUT Matrix pixel data is too short")

    rows: List[List[Float4]] = []
    for y in range(height):
        new_row: List[Float4] = []
        for x in range(width):
            # this way of doing it is slow and makes lots of copies,
            # but the files really aren't large enough for this to matter
            pixel_bytes, matrix = matrix[:16], matrix[16:] 
            pixel = struct.unpack(">ffff", pixel_bytes)
            # print(pixel_bytes.hex(), "->", pixel)
            new_row.append(pixel)
        rows.append(new_row)

    if len(matrix) != 0:
        raise ValueError(f"Garbage bytes detected after reading LUT matrix: {matrix}")
    
    return LUT(rows)

def from_rows(rows: List[List[Float4]]) -> LUT:
    return LUT(rows)

def from_dds(path: Path) -> LUT:
    res = None
    try:
        args = [env.LUTRANSLATE_BIN.as_posix(), "--from-dds", "-i", path.as_posix()]
        res = subprocess.run(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        res.check_returncode()
    except Exception as e:
        err_output = res.stderr if res is not None else b"[No output]"
        err_output = err_output.decode()
        raise LUTException(f"LUTranslate failed:\n{err_output}") from e
    
    matrix_bytes = res.stdout
    return from_matrix(matrix_bytes)


if __name__ == "__main__":
    lut = from_dds(Path("test/test_lut.dds"))

    for row in lut._channels:
        for pixel in row:
            print(pixel)

    dds = lut.to_dds()
    with open("test_outputs/test_lut-copy.dds", 'wb') as out_file:
        out_file.write(dds.getbuffer())
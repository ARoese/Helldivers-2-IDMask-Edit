from PIL import Image
from PIL.Image import Image as ImageClass
from io import BytesIO
import os
from typing import Set, Tuple, List
from pathlib import Path
import subprocess
import tempfile
import sys

from .exception import MaskSplitException

IDMaskLayer = Tuple[ImageClass, ImageClass, ImageClass, ImageClass]
IDMaskLayers = Tuple[IDMaskLayer, IDMaskLayer]

ADDON_PATH = Path(os.path.dirname(__file__))
if sys.platform == 'linux':
    TEXASSEMBLE_BIN = ADDON_PATH / "deps" / "texassemble"
else:
    TEXASSEMBLE_BIN = ADDON_PATH / "deps" / "Texassemble.exe"

class IDMask():
    layers: IDMaskLayers

    def __init__(self, layers: IDMaskLayers):
        layers_flat = [*layers[0], *layers[1]]

        for l in layers_flat:
            l1s = l.size
            l2s = layers_flat[0].size
            if l1s != l2s:
                raise MaskSplitException(f"Mask layer sizes do not match. ({l1s} != {l2s})")

        for i,l in enumerate(layers_flat):
            if l.mode != 'L':
                print("Converting non-greyscale channel to greyscale. Things might be weird.")
                layers_flat[i] = l.convert('L')

        l1 = tuple(layers_flat[:4])
        l2 = tuple(layers_flat[4:])
        assert len(l1) == 4
        assert len(l2) == 4
        self.layers = (l1, l2)

    def swizzle_layers(self) -> Tuple[ImageClass, ImageClass]:
        layer1, layer2 = self.layers

        return Image.merge("RGBA", bands=layer1), Image.merge("RGBA", bands=layer2)
    
    def to_strip(self) -> ImageClass:
        layer1, layer2 = self.swizzle_layers()

        x,y = layer1.size
        new_img = Image.new("RGBA", (x, y*2))

        new_img.paste(layer1, (0,0))
        new_img.paste(layer2, (0, y))
        return new_img
    
    def to_array(self) -> BytesIO:
        '''
        returns an array dds file
        '''
        output = BytesIO()

        tmpdir = tempfile.mkdtemp()
        # placeholder block for a `with TemporaryDirectory as td` statement. 
        # This is omitted because I don't want the directories getting cleaned up right now
        if True:
            tmpdir = Path(tmpdir)
            layer_1 = tmpdir / "1.png"
            layer_2 = tmpdir / "2.png"
            output_file = tmpdir / "out.dds"
            layers = self.swizzle_layers()
            
            layers[0].save(layer_1, format="png")
            layers[1].save(layer_2, format="png")

            layers = self.swizzle_layers()
            res = None
            try:
                res = subprocess.run([TEXASSEMBLE_BIN.as_posix(), "array", "-y", "-f", "R8G8B8A8_UNORM", "-dx10", "-o", output_file, "--", layer_1.as_posix(), layer_2.as_posix()],
                                    stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                res.check_returncode()
            except Exception as e:
                out = res.stdout if res is not None else b"[No output]"
                out = out.decode()
                raise MaskSplitException(f"texassemble failed:\n{out}") from e
            
            if not output_file.exists():
                raise MaskSplitException(f"texassemble output '{output_file.as_posix()}' does not exist!")
        
            with open(output_file, 'rb') as output_file:
                output.write(output_file.read())
        
        return output

    def save_channels(self, dest: Path, name: str, file_type: str = "png") -> List[Path]:
        '''list is of length 8, sorted in ascending channel order'''
        dest_paths = []
        for (channel, num) in zip([*self.layers[0], *self.layers[1]], "12345678"):
            dest_path = dest / f"{name}-{num}.{file_type}"

            channel.save(dest_path)
            dest_paths.append(dest_path)
        
        return dest_paths

    def dim(self) -> Tuple[int, int]:
        return self.layers[0][0].size

    def get_overlap_percentage(self) -> float:
        '''
        Calculate the proportion of pixels which are overlap. Overlap occurs when multiple channels 
        are non-zero for a single pixel, introducing ambiguity as to which material will get applied at that point.
        '''

        x,y = self.dim()
        pixel_count = x*y
        pixel_generators = [(1 if p else 0 for p in img.getdata()) for img in (*self.layers[0], *self.layers[1])] # type: ignore

        overlap_count = 0
        # vals is Tuple[8; int]
        for vals in zip(*pixel_generators):
            if sum(vals) > 1:
                overlap_count+=1
        
        return overlap_count / pixel_count

def from_strip(image: ImageClass) -> IDMask:
    x,y = image.size

    if y != 2*x:
        raise MaskSplitException("wrong input image dimensions. y dim should be 2*x")
    layer_1=image.crop((0, 0, x, y//2))
    layer_2=image.crop((0, y//2, x, y))

    layer_1,layer_2 = (layer_1.split(), layer_2.split())

    if len(layer_1) != 4 or len(layer_2) != 4:
        raise MaskSplitException("input image did not have enough channels")
    
    return IDMask((layer_1, layer_2))

def from_strip_path(src: Path) -> IDMask:
    img = Image.open(src)
    return from_strip(img)

def from_array(src: Path) -> IDMask:
    res = None
    try:
        temp_output = Path(tempfile.gettempdir()) / f"{src.stem}.png"
        res = subprocess.run([TEXASSEMBLE_BIN.as_posix(), "array-strip", "-y", "-f", "R8G8B8A8_UNORM", "-o", temp_output.as_posix(), "--", src.absolute().as_posix()],
                              stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        res.check_returncode()
    except Exception as e:
        out = res.stdout if res is not None else b"[No output]"
        out = out.decode()
        raise MaskSplitException(f"Failed to run texassemble:\n{out}") from e
    
    if not temp_output.exists():
        raise MaskSplitException(f"texassemble output '{temp_output.as_posix()}' does not exist!")
    
    return from_strip(Image.open(temp_output))

def _find_channels(root: Path, name: str) -> List[ImageClass]:
    def load_channel(p: Path) -> Tuple[int, ImageClass] | None:
        split = p.stem.rsplit('-', 1)
        if len(split) != 2:
            return None
        
        number_part = "".join(c for c in split[1] if c.isdigit())
        if not number_part:
            return None
        
        return int(number_part), Image.open(p)

    images = [
        load_channel(p)
        for p in root.iterdir() 
        if p.is_file() and p.suffix in (".png", ".dds") and name in p.stem
    ]

    images = [image for image in images if image is not None]

    images.sort(key=lambda x: x[0])

    return [g[1] for g in images]

def from_channels_dir(root_dir: Path, name: str | None = None) -> IDMask:
    def _infer_names() -> List[str]:
        names = [file.stem.rsplit("-", maxsplit=1)[0] for file in root_dir.iterdir() if file.is_file() and "-" in file.stem]

        return list(set(names))
    
    # try to infer the name based on what files are in the directory.
    if name is None:
        names = _infer_names()
        for name in names[:-1]:
            try:
                return from_channels_dir(root_dir, name)
            except MaskSplitException as e:
                continue
        
        return from_channels_dir(root_dir, names[-1])

    channels = _find_channels(root_dir, name)
    if len(channels) != 8:
        raise MaskSplitException(f"expected 8 channels. Only found {len(channels)}.")
    
    l1 = tuple(channels[:4])
    l2 = tuple(channels[4:])
    
    return IDMask((l1, l2)) #type: ignore
from PIL import Image
from PIL.Image import Image as ImageClass
from io import BytesIO
from typing import Iterable, Tuple, List, Self
from pathlib import Path
import subprocess
import tempfile
import itertools

from .itertools_ext import batched
from . import env
from .exception import MaskSplitException

IDMaskLayer = Tuple[ImageClass, ImageClass, ImageClass, ImageClass]
IDMaskLayers = Tuple[IDMaskLayer, IDMaskLayer]

class PackedChannels:
    channels: List[ImageClass]

    def __init__(self, channels: List[ImageClass]):
        for l in channels:
            l1s = l.size
            l2s = channels[0].size
            if l1s != l2s:
                raise ValueError(f"Layer sizes do not match. ({l1s} != {l2s}) This is a programmer error.")

        for i,l in enumerate(channels):
            if l.mode != 'L':
                print("Converting non-greyscale channel to greyscale. Things might be weird.")
                channels[i] = l.convert('L')

        self.channels = channels
    
    def dim(self) -> Tuple[int, int]:
        return self.channels[0].size
    
    def num_channels(self) -> int:
        return len(self.channels)

    def swizzle_layers(self) -> List[ImageClass]:        
        layers = batched(self.channels, 4, pad_with=lambda: Image.new(mode="L", size=self.dim()))
        images = [Image.merge("RGBA", bands=layer) for layer in layers]
        return images
    
    def to_strip(self) -> ImageClass:
        swizzled = self.swizzle_layers()

        x,y = self.dim()
        target_image = Image.new(mode="RGBA", size=(x, y*len(swizzled)))

        for i,img in enumerate(swizzled):
            y_offset = i*y
            target_image.paste(img, (0, y_offset))
        
        return target_image
    
    def to_array(self) -> BytesIO:
        output = BytesIO()

        tmpdir = tempfile.mkdtemp()
        # placeholder block for a `with TemporaryDirectory as td` statement. 
        # This is omitted because I don't want the directories getting cleaned up right now
        if True:
            tmpdir = Path(tmpdir)
            swizzled_layers = self.swizzle_layers()
            layer_paths = [tmpdir / f"{n+1}.png" for n in range(len(swizzled_layers))]
            output_path = tmpdir / "out.dds"
            for path, layer in zip(layer_paths, swizzled_layers):
                layer.save(path, format="png")

            res = None
            try:
                args = [env.TEXASSEMBLE_BIN.as_posix(), "array", "-y", "-f", "R8G8B8A8_UNORM", "-dx10", "-o", output_path, "--"]
                args.extend([lp.as_posix() for lp in layer_paths])
                res = subprocess.run(args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                res.check_returncode()
            except Exception as e:
                out = res.stdout if res is not None else b"[No output]"
                out = out.decode()
                raise MaskSplitException(f"texassemble failed:\n{out}") from e
            
            if not output_path.exists():
                raise MaskSplitException(f"texassemble output '{output_path.as_posix()}' does not exist!")
        
            with open(output_path, 'rb') as output_path:
                output.write(output_path.read())
        
        return output
    
    def save_channels(self, dest: Path, name: str, file_type: str = "png") -> List[Path]:
        '''list is sorted in ascending channel order'''
        dest_paths = []
        for (channel, num) in zip(self.channels, range(self.num_channels())):
            dest_path = dest / f"{name}-{num+1}.{file_type}"

            channel.save(dest_path)
            dest_paths.append(dest_path)
        
        return dest_paths
    
    def extend(self, others: Iterable[Self]):
        for o in others:
            self.channels.extend(o.channels)

    def paste(self, other: Self, corner: Tuple[int, int], depth: int = 0):        
        if other.num_channels() + depth > self.num_channels():
            raise ValueError("Not enough channel depth for this paste.")
        
        for my_channel, their_channel in zip(self.channels[depth:], other.channels):
            my_channel.paste(their_channel, corner)

def empty_channel_pack(depth: int, dim: Tuple[int, int]) -> PackedChannels:
    channels = [Image.new(mode="L", size=dim) for _ in range(depth)]
    return PackedChannels(channels)

def from_strip(image: ImageClass, n_layers: int | None = None) -> PackedChannels:
    x,y = image.size

    if n_layers is None:
        div = y / x
        num_layers = int(div)
        if x*num_layers != y:
            raise MaskSplitException(f"y dimension is not a clean multiple of x dimension. ({x}x{y})")
    else:
        num_layers = n_layers
    
    y_height = y // num_layers
    
    layers = [image.crop((0, layer*y_height, x, (layer+1)*y_height)) for layer in range(num_layers)]
    layers = [layer.split() for layer in layers]
    layers = list(itertools.chain(*layers))
    
    return PackedChannels(layers)

def from_strip_path(src: Path, expect_2_layers: bool = False) -> PackedChannels:
    img = Image.open(src)

    x, y = img.size
    if expect_2_layers and y != 2*x:
        img = img.resize((x, 2*x))

    return from_strip(img)

def from_array(src: Path) -> PackedChannels:
    res = None
    try:
        temp_output = Path(tempfile.gettempdir()) / f"{src.stem}.png"
        res = subprocess.run([env.TEXASSEMBLE_BIN.as_posix(), "array-strip", "-y", "-f", "R8G8B8A8_UNORM", "-o", temp_output.as_posix(), "--", src.absolute().as_posix()],
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

def from_channels_dir(root_dir: Path, name: str | None = None) -> PackedChannels:
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
    
    pack = PackedChannels(channels)
    
    return pack
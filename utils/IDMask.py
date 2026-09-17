from PIL import Image
from PIL.Image import Image as ImageClass
from io import BytesIO
from typing import Iterable, Tuple, List, Self
from pathlib import Path
import subprocess
import tempfile
import itertools

from .sdf_mask import sdf_channel_to_straight, channel_into_sdf

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

    def upscale_at(self, new_dim: Tuple[int, int]):
        scaled_channels = [sdf_channel_to_straight(c, new_dim) for c in self.channels]
        return PackedChannels(scaled_channels)

    def downscale_sdf(self, new_dim: Tuple[int, int]):
        scaled_channels = [channel_into_sdf(c).resize(new_dim) for c in self.channels]
        return PackedChannels(scaled_channels)
    
    def dim(self) -> Tuple[int, int]:
        return self.channels[0].size
    
    def resize(self, dim: Tuple[int, int]) -> "PackedChannels":
        if self.dim() == dim:
            return PackedChannels(self.channels)
        
        resized = [channel.resize(dim) for channel in self.channels]
        return PackedChannels(resized)
    
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

    def extended(self, others: Iterable[Self]):
        channels = list(self.channels)
        for o in others:
            channels.extend(o.channels)

        return PackedChannels(channels)

    def paste(self, other: Self, depth: int = 0, corner: Tuple[int, int] = (0,0)):        
        if other.num_channels() + depth > self.num_channels():
            raise ValueError("Not enough channel depth for this paste.")
        
        for my_channel, their_channel in zip(self.channels[depth:], other.channels):
            my_channel.paste(their_channel, corner)

    def with_depth(self, depth: int):
        if self.channels == depth:
            return PackedChannels(self.channels)
        elif len(self.channels) > depth:
            return PackedChannels(self.channels[:depth])
        else:
            diff = depth - len(self.channels)
            extra = [Image.new("L", self.dim()) for _ in range(diff)]
            return PackedChannels([*self.channels, *extra])


def empty_channel_pack(depth: int, dim: Tuple[int, int]) -> PackedChannels:
    channels = [Image.new(mode="L", size=dim) for _ in range(depth)]
    return PackedChannels(channels)

def from_strip(image: ImageClass, n_layers: int) -> PackedChannels:
    '''Load a PackedChannels from a strip, expecting no more than `max_layers` layers'''
    x,y = image.size

    print(f"Image with dims {image.size} with {n_layers} layers preparing to be loaded as IDMask.")
    
    y_height = y // n_layers
    if y != y_height * n_layers:
        raise MaskSplitException(f"{n_layers} does not divide {y}. This indicates that the given number of layers on the strip is incorrect.")
    
    layers = [image.crop((0, layer*y_height, x, (layer+1)*y_height)) for layer in range(n_layers)]
    layers = [layer.split() for layer in layers]
    layers = list(itertools.chain(*layers))

    print(f"Read IDMask with {len(layers)} layers")
    
    return PackedChannels(layers)

def from_array(src: Path) -> PackedChannels:
    res = None
    temp_output = Path(tempfile.gettempdir()) / f"{src.stem}.png"
    # PILLOW does not support arrays, so we can't use this for a full load. 
    # We can, however, use it to get the dimension
    pillow_dim = Image.open(src).size 
    try:
        res = subprocess.run([env.TEXASSEMBLE_BIN.as_posix(), "array-strip", "-y", "-f", "R8G8B8A8_UNORM", "-o", temp_output.as_posix(), "--", src.absolute().as_posix()],
                              stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        res.check_returncode()
    except Exception as e:
        out_texassemble = res.stdout if res is not None else b"[No output]"
        out_texassemble = out_texassemble.decode()
        if "ERROR: Input must be a 1D/2D array" in out_texassemble:
            print("Failed to convert to png strip because the input is not an array. Attempting direct conversion.")
            try:
                # with tempfile.TemporaryDirectory() as tempdir:
                td = tempfile.mkdtemp()
                # placeholder block for a `with TemporaryDirectory as td` statement. 
                # This is omitted because I don't want the directories getting cleaned up right now
                tp = Path(td)
                temp_output = tp / f"{src.with_suffix('.png').name}"

                res = subprocess.run([env.TEXCONV_BIN.as_posix(), "-y", "-ft", "png", "-o", tp.as_posix(), "--", src.absolute().as_posix()],
                                        stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                res.check_returncode()
                n_layers = 1
            except Exception as e:
                out_texconv = res.stdout if res is not None else b"[No output]"
                out_texconv = out_texconv.decode()
                raise MaskSplitException(f"Failed to run texassemble:\n{out_texassemble}\n\nAdditionally, failed to run texconv:\n{out_texconv}") from e
        else: 
            raise MaskSplitException(f"Failed to run texassemble:\n{out_texassemble}") from e
    
    if not temp_output.exists():
        raise MaskSplitException(f"texassemble output '{temp_output.as_posix()}' does not exist!")

    strip = Image.open(temp_output)
    n_layers = strip.size[1] // pillow_dim[1]
    return from_strip(strip, n_layers)

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
    
    pack = PackedChannels(channels)
    
    return pack

def from_file(path: Path) -> PackedChannels:
    '''Create a PackedChannels object, automatically detecting the source type.
    If the source is a non-dds image, the number of layers is assumed to be 2 unless the image is square, in which case it is assumed to be 1'''
    if path.suffix == ".dds":
        mask = from_array(path)
    else: # assume any other image type is a strip
        strip = Image.open(path)
        strip.load()
        n_layers = 2
        if strip.size[0] == strip.size[1]:
            n_layers = 1
        mask = from_strip(strip, n_layers)

    return mask
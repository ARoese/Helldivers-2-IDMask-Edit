from PIL import Image
from pathlib import Path

from . import IDMask

TEST_DIR=Path("test")
ARRAY_STRIP=TEST_DIR / "0xc89b26d36017d6e9.png"
SINGLE_LAYER=TEST_DIR / "1-layer-test.dds"
SINGLE_LAYER_STRIP=TEST_DIR / "1-layer-test.png"
ARRAY=TEST_DIR / "14455190118267868905.dds"


if __name__ == "__main__":
    name = ARRAY.stem

    one_layer = IDMask.from_file(SINGLE_LAYER)
    print(f"loaded one-layer IDMask dds and got {one_layer.num_channels()} channels")

    one_layer = IDMask.from_file(SINGLE_LAYER_STRIP)
    print(f"loaded one-layer IDMask png and got {one_layer.num_channels()} channels")

    id_mask = IDMask.from_file(ARRAY)
    id_mask.save_channels(TEST_DIR, name, "png")
    #print(id_mask.get_overlap_percentage())

    IDMask.from_channels_dir(TEST_DIR, name)

    dds = id_mask.to_array()
    dds_out_path = ARRAY.with_suffix(".dds").with_name(f"{ARRAY.stem}-copy")
    with open(dds_out_path, "wb") as out:
        out.write(dds.getbuffer())
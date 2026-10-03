import json
from functools import cache
from pathlib import Path
from typing import Tuple
from .. import hashing

# This file is from RiderAnton. It should be updated with each new content update that adds armor.
_CAS_JSON_PATH = Path(__file__).with_name("customization_armor_sets.json")

@cache
def load_armor_sets():
    with open(_CAS_JSON_PATH, "r") as jf:
        return json.load(jf)

# sometimes, a string is given instead of the simple hash. This automatically hashes the string if given
def id_from_hashable(id: str) -> int:
    try:
        return int(id, base=16)
    except ValueError:
        return hashing.murmur64_hash(id.encode('utf-8'))

# NOTE: This could be optimized a lot, but probably isn't slow enough to justify
def find_lut_for_obj(
        object_id: int,
) -> Tuple[int, int] | None:
    '''use customization_armor_sets to locate the LUT for a given object. Returns (archive_id, lut_id) for the material LUT'''
    armor_sets = load_armor_sets()
    for armor_set in armor_sets:
        name: str = armor_set["name"]
        archive: int = id_from_hashable(armor_set["archive"])
        for body_type in armor_set["body_types"]:
            body_type_str: str = body_type["body_type"]
            for piece in body_type["pieces"]:
                path_id: int = id_from_hashable(piece["path"])
                path_32: int = path_id >> 32 # allow for matches of both murmur32 and murur64
                material_lut: str = piece["material_lut"]

                if object_id in [path_id, path_32]:
                    return (archive, id_from_hashable(material_lut))
from enum import Enum
from typing import List, Tuple


class BumpMap(Enum):
    FLAT_GRIME_DRY = 0
    FLAT_GRIM_WET = 1
    DAMASCUS = 2
    SUEDE_DRY_GRIME = 3
    SUEDE_WET_GRIME = 4
    WALL_BULLET_HOLES = 5
    DENIM = 6
    CORDUROY = 7
    WAFFLE = 8
    WALL_PLASTER = 9
    WALL_CONCRETE = 10
    RAINCOAT = 11
    WOOL_KNITTED = 12
    WOOL_WOVEN = 13
    SCRAP_METAL = 14
    LEATHER_WORN = 15
    LINEN = 16
    LINEN_WORN = 17
    NYLON = 18
    LEATHER_WET_GRIME = 19
    LEATHER_DRY_GRIME = 20
    BOULDER = 21
    CIRCUITBOARD = 22
    DIMPLED_SQUARE = 23
    VINYL = 24
    CIRCUITBOARD_LIGHT = 25

    @classmethod
    def values(cls) -> List[Tuple[str, str, str]]:
        pretty_names = [
            "Flat (dry grime)",
            "Flat (wet grime)",
            "Damascus",
            "Suede (dry grime)",
            "Suede (wet grime)",
            "Wall (Bullet Holes)",
            "Denim",
            "Corduroy",
            "Waffle",
            "Wall (Plaster)",
            "Wall (Concrete)",
            "Raincoat",
            "Wool (Knitted)",
            "Wool (Woven)",
            "Scrap Metal",
            "Leather (Worn)",
            "Linen",
            "Linen (Worn)",
            "Nylon",
            "Leather (wet grime)",
            "Leather (dry grime)",
            "Boulder",
            "Circuitboard",
            "Dimpled (Square)",
            "Vinyl",
            "Circuitboard (Light)"
        ]
        o: List[Tuple[str, str, str]] = []
        for idx, name in enumerate(pretty_names):
            o.append((str(idx), name, ""))

        return o

class LUTColumn1A(Enum):
    O1 = 0
    DISABLE_EMISSIVE = 1
    RIM_BRIGHTENING = 2
    DETAIL_ARRAY = 3

    def to_float(self) -> float:
        match self:
            case self.O1:
                return 0.0
            case self.DISABLE_EMISSIVE:
                return 1.0
            case self.RIM_BRIGHTENING:
                return 2.0
            case self.DETAIL_ARRAY:
                return 4.0

    @classmethod
    def from_float(cls, f: float):
        if f < 1.0:
            return cls.O1
        elif f < 2.0:
            return cls.DISABLE_EMISSIVE
        elif f < 3.0:
            return cls.RIM_BRIGHTENING
        elif f < 5.0:
            return cls.DETAIL_ARRAY
        else:
            return cls.DETAIL_ARRAY

    @classmethod
    def values(cls) -> List[Tuple[str, str, str]]:
        return [
            ("0", "Off/default", ""),
            ("1", "Enable Curvature Gradient / Disable Emissive / Disable Camo Alpha Masks", ""),
            ("2", "Enable Rim Brightening Support", ""),
            ("3", "Use composite detail array", ""),
        ]
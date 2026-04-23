import sys
import os
from pathlib import Path

ADDON_PATH = Path(os.path.dirname(__file__))
if sys.platform == 'linux':
    TEXASSEMBLE_BIN = ADDON_PATH / "deps" / "texassemble"
    LUTRANSLATE_BIN = ADDON_PATH / "deps" / "LUTranslate"
else:
    TEXASSEMBLE_BIN = ADDON_PATH / "deps" / "Texassemble.exe"
    LUTRANSLATE_BIN = ADDON_PATH / "deps" / "LUTranslate.exe"
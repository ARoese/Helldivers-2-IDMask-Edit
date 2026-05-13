import sys
import os
from pathlib import Path

ADDON_PATH = Path(os.path.dirname(__file__))
_DEPS_PATH = ADDON_PATH / "deps"
if sys.platform == 'linux':
    TEXASSEMBLE_BIN = _DEPS_PATH / "texassemble"
    TEXCONV_BIN = _DEPS_PATH / "texconv"
    LUTRANSLATE_BIN = _DEPS_PATH / "LUTranslate"
else:
    TEXASSEMBLE_BIN = _DEPS_PATH / "Texassemble.exe"
    TEXCONV_BIN = _DEPS_PATH / "texconv.exe"
    LUTRANSLATE_BIN = _DEPS_PATH / "LUTranslate.exe"
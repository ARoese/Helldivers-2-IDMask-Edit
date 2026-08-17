from typing import Annotated, List, Literal, Tuple
import bpy

from .ops import pillow_install
from .ops.pillow_install import LibsInstallPanel, InstallLibsOperator
from . import info

bl_info = info.bl_info

#pillow_install.is_pillow_installed = False

def register():
    if pillow_install.are_libs_installed:
        from . import registration
        registration.register()
    else:
        print("Pillow is not installed. Only the pillow installation panel will be shown")
        bpy.utils.register_class(LibsInstallPanel)
        bpy.utils.register_class(InstallLibsOperator)


def unregister():
    if pillow_install.are_libs_installed:
        from . import registration
        registration.unregister() 
    else:
        bpy.utils.unregister_class(LibsInstallPanel)
        bpy.utils.unregister_class(InstallLibsOperator)

if __name__ == "__main__":
    register()
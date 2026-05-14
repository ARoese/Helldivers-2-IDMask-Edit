from typing import Literal

import bpy
import sys, subprocess, textwrap
from bpy.types import Context
try:
    import PIL
    is_pillow_installed=True
except Exception as e:
    print(f"Pillow could not be imported with the following error: {e}")
    is_pillow_installed=False

_pil_was_just_installed = False

class InstallPillowOperator(bpy.types.Operator):
    bl_idname = "hd2visual.install_pillow"
    bl_label = "Install Pillow"
    bl_options = {'REGISTER'}

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        subprocess.run([sys.executable, "-m", "pip", "install", "pillow"]).check_returncode()
        global _pil_was_just_installed
        _pil_was_just_installed=True
        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        if is_pillow_installed or _pil_was_just_installed:
            cls.poll_message_set("Pillow is already installed")
            return False
        
        return True

class PillowInstallPanel(bpy.types.Panel):
    """Panel for installing pillow if necessary"""
    bl_label = "Install Pillow"
    bl_idname = "UI_PT_InstallPillowPanel"
    bl_category = "HD2 Visual Edit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context: Context) -> None:
        layout = self.layout
        assert layout is not None

        if not is_pillow_installed and not _pil_was_just_installed:
            col = layout.column(align=True)
            lines = textwrap.wrap("The python PIL (pillow) library is required to use this plugin. Click the button below to install it into blender.", width=40)

            for line in lines:
                col.label(text=line)
            op = col.operator(InstallPillowOperator.bl_idname, text=f"Install pillow")
        else:
            layout.label(text="Pillow is installed.")
            layout.label(text="Please restart blender.")
        
        
            
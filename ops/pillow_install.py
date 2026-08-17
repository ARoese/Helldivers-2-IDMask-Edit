from typing import Literal

import bpy
import sys, subprocess, textwrap
from bpy.types import Context
try:
    import PIL
    import pyopencl
    are_libs_installed=True
except Exception as e:
    print(f"Libraries could not be imported with the following error: {e}")
    are_libs_installed=False

_just_installed = False

class InstallLibsOperator(bpy.types.Operator):
    bl_idname = "hd2visual.install_pillow"
    bl_label = "Install Pillow"
    bl_options = {'REGISTER'}

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        subprocess.run([sys.executable, "-m", "pip", "install", "pillow", "pyopencl"]).check_returncode()
        global _just_installed
        _just_installed=True
        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        if are_libs_installed or _just_installed:
            cls.poll_message_set("Libs are already installed")
            return False
        
        return True

class LibsInstallPanel(bpy.types.Panel):
    """Panel for installing libs if necessary"""
    bl_label = "Install Libs"
    bl_idname = "UI_PT_InstallLibsPanel"
    bl_category = "HD2 Visual Edit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context: Context) -> None:
        layout = self.layout
        assert layout is not None

        if not are_libs_installed and not _just_installed:
            col = layout.column(align=True)
            lines = textwrap.wrap("The python PIL (pillow) and pyopencl libraries are required to use this plugin. Click the button below to install them into blender.", width=40)

            for line in lines:
                col.label(text=line)
            op = col.operator(InstallLibsOperator.bl_idname, text=f"Install Libs")
        else:
            layout.label(text="Libs are installed.")
            layout.label(text="Please restart blender.")
        
        
            
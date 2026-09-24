from typing import Annotated, List, Literal, Tuple
import bpy

from .ops.accurate_to_sdk import AccurateToSDK
from .ops.patch_accurate_shader import PatchAccurate
from .ops.import_export import ImportIDMaskOperator, ExportToArrayOperator, ImportPatternMaskOperator, ExportPatternMaskOperator, AddIDMask
from .ops.lut.lut_panel import ExportLUTOperator
from .ops.painting import PaintMaterial, MaterialSwitcherPanel
from .ops.complex_merge import ComplexMerge
from .ops.lut import lut_panel

def draw_object_func(self: bpy.types.Menu, context):
    assert self.layout is not None
    layout = self.layout
    layout.separator(type="LINE")
    layout.operator_context = "INVOKE_DEFAULT"
    layout.label(text="HD2 IDMask Edit")
    layout.operator(AddIDMask.bl_idname, text="Create Debug IDMask")
    layout.operator(ImportIDMaskOperator.bl_idname, text="Import IDMask")
    layout.operator(ImportPatternMaskOperator.bl_idname, text="Import Pattern Mask")
    layout.operator(ExportToArrayOperator.bl_idname, text="Export IDMask to Array")
    layout.operator(ExportPatternMaskOperator.bl_idname, text="Export Pattern Mask")
    layout.operator(ExportLUTOperator.bl_idname, text="Export LUT to DDS")
    layout.separator(type="LINE")
    layout.operator(ComplexMerge.bl_idname, text="Merge Assets")
    layout.operator(AccurateToSDK.bl_idname, text="Convert to SDK material")
    layout.operator(PatchAccurate.bl_idname, text="Patch Accurate Shader")
        

CLASSES = [
    ImportIDMaskOperator, ExportToArrayOperator, ImportPatternMaskOperator, ExportPatternMaskOperator, 
    PaintMaterial, MaterialSwitcherPanel, ComplexMerge, AddIDMask, AccurateToSDK, PatchAccurate
]

def register():
    print("registered visual edit addon")

    for cl in CLASSES:
        bpy.utils.register_class(cl)

    lut_panel.register()
    #bpy.types.NODE_MT_context_menu.append(draw_node_menu)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_object_func)

def unregister():
    for cl in CLASSES:
        bpy.utils.unregister_class(cl)

    lut_panel.unregister()
    #bpy.types.NODE_MT_context_menu.remove(draw_node_menu)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_object_func)
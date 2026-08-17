from typing import Annotated, List, Literal, Tuple
import bpy

from .ops.import_export import ImportIDMaskOperator, ExportToArrayOperator, AddIDMask
from .ops.painting import PaintMaterial, MaterialSwitcherPanel
from .ops.complex_merge_no_atlas import ComplexMergeNoAtlas

def draw_object_func(self: bpy.types.Menu, context):
    assert self.layout is not None
    layout = self.layout
    layout.separator(type="LINE")
    layout.operator_context = "INVOKE_DEFAULT"
    layout.label(text="HD2 IDMask Edit")
    layout.operator(AddIDMask.bl_idname, text="Create Debug IDMask")
    layout.operator(ImportIDMaskOperator.bl_idname, text="Import IDMask")
    layout.operator(ExportToArrayOperator.bl_idname, text="Export IDMask to Array")
    layout.separator(type="LINE")
    layout.operator(ComplexMergeNoAtlas.bl_idname, text="Merge Assets")

CLASSES = [ImportIDMaskOperator, ExportToArrayOperator, PaintMaterial, MaterialSwitcherPanel, ComplexMergeNoAtlas, AddIDMask]

def register():
    print("registered visual edit addon")

    for cl in CLASSES:
        bpy.utils.register_class(cl)
    #bpy.types.NODE_MT_context_menu.append(draw_node_menu)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_object_func)

def unregister():
    for cl in CLASSES:
        bpy.utils.unregister_class(cl)
    #bpy.types.NODE_MT_context_menu.remove(draw_node_menu)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_object_func)
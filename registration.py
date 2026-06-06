from typing import Annotated, List, Literal, Tuple
import bpy

from .ops.import_export import MakeEditableOperator, ExportToArrayOperator
from .ops.painting import PaintMaterial, MaterialSwitcherPanel, AddIDMask, ExportDebugIDMaskToArrayOperator, EditWithDebugIDMask
from .ops.complex_merge_no_atlas import ComplexMergeNoAtlas

def draw_node_menu(self: bpy.types.Menu, context):
    assert self.layout is not None
    layout = self.layout
    layout.separator(type="LINE")
    layout.operator_context = 'INVOKE_DEFAULT'
    layout.operator(MakeEditableOperator.bl_idname, text="Make Editable")
    layout.operator(ExportToArrayOperator.bl_idname, text="Export to IDMask Array")    

def draw_object_func(self: bpy.types.Menu, context):
    assert self.layout is not None
    layout = self.layout
    layout.separator(type="LINE")
    layout.operator_context = "INVOKE_DEFAULT"
    layout.operator(ComplexMergeNoAtlas.bl_idname, text="Merge Assets")

    if True: #AddIDMask.poll(context):
        layout.operator(AddIDMask.bl_idname, text="Create IDMask")
    if True: #ExportDebugIDMaskToArrayOperator.poll(context):
        layout.operator(ExportDebugIDMaskToArrayOperator.bl_idname, text="Export IDMask from Debug Material")
    if True: #EditWithDebugIDMask.poll(context):
        layout.operator(EditWithDebugIDMask.bl_idname, text="Apply IDMask to Debug Material")

CLASSES = [MakeEditableOperator, ExportToArrayOperator, PaintMaterial, MaterialSwitcherPanel, ComplexMergeNoAtlas, AddIDMask, ExportDebugIDMaskToArrayOperator, EditWithDebugIDMask]

def register():
    print("registered visual edit addon")

    for cl in CLASSES:
        bpy.utils.register_class(cl)
    bpy.types.NODE_MT_context_menu.append(draw_node_menu)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_object_func)

def unregister():
    for cl in CLASSES:
        bpy.utils.unregister_class(cl)
    bpy.types.NODE_MT_context_menu.remove(draw_node_menu)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_object_func)
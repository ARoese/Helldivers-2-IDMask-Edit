from typing import Annotated, List, Literal, Tuple
import bpy

from .ops.import_export import MakeEditableOperator, ExportToArrayOperator
from .ops.painting import PaintMaterial, MaterialSwitcherPanel
from .ops.complex_merge import ComplexMerge

bl_info = {
    "name": "HD2 LUT Visual Edit",
    "blender": (4, 3, 0),
    "version": (1, 1, 1),
    "category": "Material",
}
    
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
    layout.operator(ComplexMerge.bl_idname, text="Merge Assets")

def register():
    print("registered visual edit addon")
    bpy.utils.register_class(MakeEditableOperator)
    bpy.utils.register_class(ExportToArrayOperator)
    bpy.utils.register_class(PaintMaterial)
    bpy.utils.register_class(MaterialSwitcherPanel)
    bpy.utils.register_class(ComplexMerge)
    bpy.types.NODE_MT_context_menu.append(draw_node_menu)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_object_func)

def unregister():
    bpy.utils.unregister_class(MakeEditableOperator)
    bpy.utils.unregister_class(ExportToArrayOperator)
    bpy.utils.unregister_class(PaintMaterial)
    bpy.utils.unregister_class(MaterialSwitcherPanel)
    bpy.utils.unregister_class(ComplexMerge)
    bpy.types.NODE_MT_context_menu.remove(draw_node_menu)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_object_func)

if __name__ == "__main__":
    register()
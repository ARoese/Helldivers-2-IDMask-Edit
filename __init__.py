from typing import Annotated, List, Literal, Tuple
import bpy

from .ops.import_export import MakeEditableOperator, ExportToArrayOperator
from .ops.painting import PaintMaterial, MaterialSwitcherPanel

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

def register():
    print("registered visual edit addon")
    bpy.utils.register_class(MakeEditableOperator)
    bpy.utils.register_class(ExportToArrayOperator)
    bpy.utils.register_class(PaintMaterial)
    bpy.utils.register_class(MaterialSwitcherPanel)
    bpy.types.NODE_MT_context_menu.append(draw_node_menu)

def unregister():
    bpy.utils.unregister_class(MakeEditableOperator)
    bpy.utils.unregister_class(ExportToArrayOperator)
    bpy.utils.unregister_class(PaintMaterial)
    bpy.utils.unregister_class(MaterialSwitcherPanel)
    bpy.types.NODE_MT_context_menu.remove(draw_node_menu)

if __name__ == "__main__":
    register()
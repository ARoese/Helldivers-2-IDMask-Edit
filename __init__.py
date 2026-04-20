from typing import Annotated, List, Literal, Tuple
import bpy

from .ops.import_export import MakeEditableOperator, ExportToArrayOperator
from .ops.painting import PaintMaterial, MaterialSwitcherPanel

bl_info = {
    "name": "HD2 LUT Visual Edit",
    "blender": (4, 3, 0),
    "version": (1, 1, 0),
    "category": "Material",
}
    
def add_make_editable_context():
    def draw_menu(self: bpy.types.Menu, context):
        assert self.layout is not None
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator(MakeEditableOperator.bl_idname, text="Make Editable")
        layout.operator(ExportToArrayOperator.bl_idname, text="Export to IDMask Array")

    bpy.types.NODE_MT_context_menu.append(draw_menu)

def register():
    print("registered visual edit addon")
    bpy.utils.register_class(MakeEditableOperator)
    bpy.utils.register_class(ExportToArrayOperator)
    bpy.utils.register_class(PaintMaterial)
    bpy.utils.register_class(MaterialSwitcherPanel)
    add_make_editable_context()

def unregister():
    bpy.utils.unregister_class(MakeEditableOperator)
    bpy.utils.unregister_class(ExportToArrayOperator)
    bpy.utils.unregister_class(PaintMaterial)
    bpy.utils.unregister_class(MaterialSwitcherPanel)

if __name__ == "__main__":
    register()
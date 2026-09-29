import bpy
from pathlib import Path
from typing import List, Literal, Self
from bl_ui.generic_ui_list import draw_ui_list

from ..utils import accurate_shader
from ...utils import LUT
from ...utils.LUT import LUT as LUTType
from .util import is_LUT_image
from ..utils import images as image_util
from .lut_panel import LUTProperty

from ...__init__ import ADDON_DIR

class LUTRowsDir:
    dir: Path

    def __init__(self, dir: Path):
        self.dir = dir
        dir.mkdir(parents=True, exist_ok=True)

    def _path_to(self, name: str) -> Path:
        return (self.dir / f"{name}.dds")

    def get(self, name: str) -> LUTType | None:
        location = self._path_to(name)
        if location.exists():
            return LUT.from_dds(location)
        else:
            return None

    def set(self, name: str, lut: LUTType | None):
        if lut is None:
            self._path_to(name).unlink()
            return

        rows = lut.dim()[1]
        if rows != 1:
            raise ValueError(f"Given LUT must have exactly 1 row. Got {rows}.")

        out_bytes = lut.to_dds()
        with open(self._path_to(name), 'wb') as out_file:
            out_file.write(out_bytes.getbuffer())

    def rows(self) -> List[str]:
        return [p.stem for p in self.dir.iterdir() if p.suffix.lower() == ".dds"]

SAVED_ROWS_DIR_23=LUTRowsDir(ADDON_DIR / "saved_data" / "LUT" / "23")
# TODO: Make LUT row saving and such also work in the image viewer, not just 3d view
class SaveNewLUTRow(bpy.types.Operator):
    bl_idname = "hd2visual.save_lut_row"
    bl_label = "Save LUT Row"
    bl_options = {'REGISTER'}

    new_row_name: bpy.props.StringProperty(name="New Row Name", default="New LUT Row") #type: ignore

    def invoke(self, context, event):
        assert context.window_manager is not None
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        ao = context.active_object
        assert ao is not None
        mg = accurate_shader.find_main_group(ao)
        assert mg is not None
        lut_node = mg.get_primary_lut_texture_node()
        assert lut_node is not None
        lut_image = lut_node.image
        assert lut_image is not None

        bridge = SavedLUTRowsBridge.from_windowmanager(context.window_manager, SAVED_ROWS_DIR_23)
        source_lut = image_util.lut_from_blender_image(lut_image)
        row_to_save = source_lut.take_row(bridge.editor_pg.selected_row-1) # 1-indexed to 0-indexed
        bridge.dir.set(self.new_row_name, row_to_save)

        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        if (
            context.window_manager is None
            or context.active_object is None
            or (mg := accurate_shader.find_main_group(context.active_object)) is None
            or (tn := mg.get_primary_lut_texture_node()) is None
            or tn.image is None
            ):
            return False

        if not is_LUT_image(tn.image):
            return False

        return True

class ApplySelectedLUTRow(bpy.types.Operator):
    bl_idname = "hd2visual.apply_selected_lut_row"
    bl_label = "Apply Row"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        ao = context.active_object
        assert ao is not None
        mg = accurate_shader.find_main_group(ao)
        assert mg is not None
        lut_node = mg.get_primary_lut_texture_node()
        assert lut_node is not None
        lut_image = lut_node.image
        assert lut_image is not None

        bridge = SavedLUTRowsBridge.from_windowmanager(context.window_manager, SAVED_ROWS_DIR_23)
        current_lut = image_util.lut_from_blender_image(lut_image)
        paste_row_index = bridge.editor_pg.selected_row-1 # 1-indexed to 0-indexed

        name_index = bridge.pg.selected_row
        selected_name: str = bridge.pg.rows[name_index].name
        row_to_paste = bridge.dir.get(selected_name)
        assert row_to_paste is not None

        current_lut.set_row(paste_row_index, row_to_paste.get_row(0))

        image_util.populate_blender_lut(current_lut, lut_image)

        # make sure other scenes render the update immediately
        for scene in bpy.data.scenes:
            scene.update_render_engine()
        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        if (
            context.window_manager is None
            or context.active_object is None
            or (mg := accurate_shader.find_main_group(context.active_object)) is None
            or (tn := mg.get_primary_lut_texture_node()) is None
            or tn.image is None
            ):
            return False

        if not is_LUT_image(tn.image):
            return False

        bridge = SavedLUTRowsBridge.from_windowmanager(context.window_manager, SAVED_ROWS_DIR_23)
        if bridge.pg.selected_row > len(bridge.pg.rows) or len(bridge.pg.rows) == 0 or bridge.pg.selected_row < 0:
            return False
        return True

class DelSelectedLUTRow(bpy.types.Operator):
    bl_idname = "hd2visual.del_saved_lut_row"
    bl_label = "Delete Saved LUT Row"
    bl_options = {'REGISTER'}

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        ao = context.active_object
        assert ao is not None
        mg = accurate_shader.find_main_group(ao)
        assert mg is not None
        lut_node = mg.get_primary_lut_texture_node()
        assert lut_node is not None
        lut_image = lut_node.image
        assert lut_image is not None

        bridge = SavedLUTRowsBridge.from_windowmanager(context.window_manager, SAVED_ROWS_DIR_23)
        name_index = bridge.pg.selected_row
        selected_name: str = bridge.pg.rows[name_index].name

        bridge.dir.set(selected_name, None)

        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        if (
            context.window_manager is None
            or context.active_object is None
            or (mg := accurate_shader.find_main_group(context.active_object)) is None
            or (tn := mg.get_primary_lut_texture_node()) is None
            or tn.image is None
            ):
            return False

        if not is_LUT_image(tn.image):
            return False

        bridge = SavedLUTRowsBridge.from_windowmanager(context.window_manager, SAVED_ROWS_DIR_23)
        if bridge.pg.selected_row > len(bridge.pg.rows) or len(bridge.pg.rows) == 0 or bridge.pg.selected_row < 0:
            return False
        return True

class SavedLUTRows(bpy.types.PropertyGroup):
    rows: bpy.props.CollectionProperty(
        type=bpy.types.PropertyGroup, # type: ignore
        name="Saved LUT Rows"
    ) #type: ignore

    selected_row: bpy.props.IntProperty(
        name="Selected LUT Row",
    ) #type: ignore

class SavedLUTRowsBridge:
    pg: SavedLUTRows
    dir: LUTRowsDir
    editor_pg: LUTProperty
    def __init__(self, dir: LUTRowsDir, pg: SavedLUTRows, editor_pg: LUTProperty):
        self.dir = dir
        self.pg = pg
        self.editor_pg = editor_pg

    def populate_property_group(self):
        self.pg.rows.clear()
        for row in self.dir.rows():
            nr: bpy.types.StringProperty = self.pg.rows.add()
            nr.name = row

    @classmethod
    def from_windowmanager(cls, wm: bpy.types.WindowManager, dir: LUTRowsDir) -> Self:
        return SavedLUTRowsBridge(
            dir, 
            wm.hd2_saved_idmask_lut_property, #type: ignore
            wm.hd2_idmask_lut_property #type: ignore
        ) #type: ignore

class LUTRowsList(bpy.types.UIList):
  def draw_item(self, context, layout, data, item, icon, active_data, active_property): #type: ignore
    if self.layout_type in {'DEFAULT', 'COMPACT'}:
      layout.prop(item, 'name', text='', emboss=False, icon='MATERIAL')

def panel_draw(layout: bpy.types.UILayout, context: bpy.types.Context, bridge: SavedLUTRowsBridge):
    col = layout.column()
    col.prop(bridge.editor_pg, "selected_row")
    split = col.row().split(factor=0.7)
    split.column().template_list("LUTRowsList", "", bridge.pg, "rows", bridge.pg, "selected_row")
    crud_column = split.column()
    crud_column.operator(SaveNewLUTRow.bl_idname, icon="ADD", text="")
    crud_column.operator(DelSelectedLUTRow.bl_idname, icon="REMOVE", text="")
    crud_column.separator(factor=2.0)
    crud_column.operator(ApplySelectedLUTRow.bl_idname, icon="MATERIAL")

class SavedLUTRowsPanel3D(bpy.types.Panel):
    """Creates a Panel in the View3D space"""
    bl_label = "Saved LUT Rows"
    bl_idname = "UI_PT_SavedLUTRowsPanelView3D"
    bl_category = "LUT Editor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context: bpy.types.Context) -> None:
        assert context.window_manager is not None
        ao = context.active_object
        assert ao is not None
        mg = accurate_shader.find_main_group(ao)
        assert mg is not None
        lut_node = mg.get_primary_lut_texture_node()
        assert lut_node is not None
        lut_image = lut_node.image
        assert lut_image is not None
        
        layout = self.layout
        assert layout is not None

        bridge = SavedLUTRowsBridge.from_windowmanager(context.window_manager, SAVED_ROWS_DIR_23)
        bridge.populate_property_group()
        panel_draw(layout, context, bridge)
        
    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        if (
            context.window_manager is None
            or context.active_object is None
            or (mg := accurate_shader.find_main_group(context.active_object)) is None
            or (tn := mg.get_primary_lut_texture_node()) is None
            or tn.image is None
            ):
            return False

        if not is_LUT_image(tn.image):
            return False

        return True

CLASSES = [SavedLUTRows, LUTRowsList, SavedLUTRowsPanel3D, SaveNewLUTRow, DelSelectedLUTRow, ApplySelectedLUTRow]
def register():
    for c in CLASSES:
        bpy.utils.register_class(c)

    bpy.types.WindowManager.hd2_saved_idmask_lut_property = bpy.props.PointerProperty(type=SavedLUTRows) #type: ignore
def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)

    del bpy.types.WindowManager.hd2_saved_idmask_lut_property #type: ignore

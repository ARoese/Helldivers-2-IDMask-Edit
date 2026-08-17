from pathlib import Path
from typing import Literal, Tuple

import bpy
from bpy.types import Context, Event

from ...utils import IDMask
from ...utils.IDMask import PackedChannels

class IDMask_Import(bpy.types.Operator):
    '''utility superclass for operations that import an IDMask'''
    filepath: bpy.props.StringProperty(name="ID Mask Path", subtype="FILE_PATH") #type: ignore
    is_sdf: bpy.props.BoolProperty(default=False, name="Is SDF", description="Assume the given mask is an SDF. SDFs have soft, blurry edges. This will allow intuitive fine editing of the imported mask.") #type: ignore
    sdf_upscale_target: bpy.props.IntProperty(name="Target Resolution", default=1024, min=32, description="The resolution that this mask will be edited at. You can set this very high, as it can be downscaled on export.") #type: ignore

    filter_glob: bpy.props.StringProperty(
        default="*.png;*.dds",
        options={'HIDDEN'},
    ) #type: ignore

    def draw(self, context):
        layout = self.layout
        assert layout is not None

        layout.label(text="Select a 2-layer RGBA dds file to import", icon='INFO')
        
        layout.prop(self, "is_sdf")
        if self.is_sdf:
            layout.prop(self, "sdf_upscale_target")

    def invoke(self, context: Context, event: Event) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def read_picked_mask(self) -> Tuple[str, PackedChannels]:
        '''read the IDMask picked by the user, applying SDF conversion as needed. Returns the mask, and the name associated with that mask'''
        id_mask_array_path = Path(self.filepath)
        id_mask_array = IDMask.from_file(id_mask_array_path)

        if self.is_sdf:
            id_mask_array = id_mask_array.upscale_at((self.sdf_upscale_target, self.sdf_upscale_target))

        return (id_mask_array_path.stem, id_mask_array)

class IDMask_Export(bpy.types.Operator):
    '''utility superclass for operations that export an IDMask'''
    filepath: bpy.props.StringProperty(name="ID Mask Array Path", subtype="FILE_PATH") #type: ignore
    
    filter_glob: bpy.props.StringProperty(
        default="*.dds",
        options={'HIDDEN'},
    ) #type: ignore

    to_sdf: bpy.props.BoolProperty(default=False, name="as SDF", description="Export to a SDF at a lower resolution. See the README to understand what this means.") #type: ignore
    sdf_downscale_target: bpy.props.IntProperty(name="SDF resolution", default=256, min=32, description="The resolution of the exported SDF.") #type: ignore

    def draw(self, context):
        layout = self.layout
        assert layout is not None

        layout.label(text="Export to a .dds file.", icon='INFO')
                
        layout.prop(self, "to_sdf")
        if self.to_sdf:
            layout.prop(self, "sdf_downscale_target")

    def invoke(self, context: Context, event: Event) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        assert context.window_manager is not None
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def write_mask(self, mask: PackedChannels):
        '''write the given IDMask to the location picked by the user, applying SDF conversion as needed.'''
        out_path = Path(self.filepath)
        if out_path.suffix == ".blend":
            raise Exception("Refusing to overwrite blend file!")

        if self.to_sdf:
            mask = mask.downscale_sdf((self.sdf_downscale_target, self.sdf_downscale_target))

        with open(out_path, 'wb') as out_file:
            out_file.write(mask.to_array().getbuffer())
        

    
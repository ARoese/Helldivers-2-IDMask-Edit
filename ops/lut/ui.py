import bpy
from typing import Dict
from .properties import BPYLUTBridge, LUTPixelProperty

def draw_lut_color(col: bpy.types.UILayout, pixel: LUTPixelProperty):
    col.prop(pixel, "color", text="")

def draw_lut_color_with_alpha_slider(col: bpy.types.UILayout, pixel: LUTPixelProperty, alpha_text: str | None = None):
    col.prop(pixel, "color", text="")
    col.prop(pixel, "a", text=alpha_text)

def draw_lut_r_slider(col: bpy.types.UILayout, pixel: LUTPixelProperty, text: str | None=None):
    col.prop(pixel, "r", text=text)

def draw_lut_g_slider(col: bpy.types.UILayout, pixel: LUTPixelProperty, text: str | None=None):
    col.prop(pixel, "g", text=text)

def draw_lut_b_slider(col: bpy.types.UILayout, pixel: LUTPixelProperty, text: str | None=None):
    col.prop(pixel, "b", text=text)

def draw_lut_a_slider(col: bpy.types.UILayout, pixel: LUTPixelProperty, text: str | None=None):
    col.prop(pixel, "a", text=text)

def draw_lut_rgba_sliders(
        col: bpy.types.UILayout,
        pixel: LUTPixelProperty,
        red_text: str | None = None,
        green_text: str | None = None,
        blue_text: str | None = None,
        alpha_text: str | None = None):
    col.prop(pixel, "r", text=red_text)
    col.prop(pixel, "g", text=green_text)
    col.prop(pixel, "b", text=blue_text)
    col.prop(pixel, "a", text=alpha_text)

def draw_generic_mask_sliders(
        col: bpy.types.UILayout,
        pixel: LUTPixelProperty):
    
    split = col.split(factor=0.2)
    col1 = split.column()
    col1.label(text="Detail Map")
    row = split.column().row()
    draw_lut_r_slider(row, pixel, text="Texture")
    draw_lut_g_slider(row, pixel, text="Surface")

    split = col.split(factor=0.2)
    col1 = split.column()
    col1.label(text="Normal Map")
    row = split.column().row()
    draw_lut_a_slider(row, pixel, text="AO")
    draw_lut_b_slider(row, pixel, text="Curvature")
    #draw_lut_rgba_sliders(col, pixel, 
    #    "Bump Map Blue Channel Mask",
    #    "Bump Map Alpha Channel Mask",
    #    "Normal Map Alpha Channel Mask",
    #    "Normal Map Blue Channel Mask"
    #)

def draw_centered_label(layout: bpy.types.UILayout, text: str):
    row = layout.row()
    row.alignment = 'CENTER'
    row.label(text=text)

def draw_lut_user_friendly(layout: bpy.types.UILayout, bridge: BPYLUTBridge):
    # TODO: Replace references to "Application inversion" with something more sensible

    # TODO: Do not draw or at least disable certain props when they are disabled based on other material properties.
    # Like, disable emissive when the disable emissive option is selected. Check the LUT sheet for these associations
    row_index = bridge.lut_property.selected_row-1
    x_dim,y = bridge.lut.dim()
    lut_row_start = x_dim*row_index
    def column(column: int) -> LUTPixelProperty:
        if column < 1 or column > 23:
            raise ValueError(f"LUT column {column} out of range")

        return bridge.lut_property.lut[lut_row_start+column-1]

    def surface_properties():
        draw_centered_label(layout, "Surface Properties")
        layout.prop(column(1), "col1_a") # Special material mode
        draw_lut_r_slider(layout, column(11), text="Roughness [0 to 10]")
        draw_lut_r_slider(layout, column(14), text="Emissive [0 to 0.06]")

    def detail_map():
        draw_centered_label(layout, "Detailing Map")
        split = layout.split(factor=0.8)
        split.column().prop(column(2), "bump_map_index_enum")
        split.column().prop(column(2), "bump_map_index_int", text="")
        draw_lut_g_slider(layout, column(2), text="Detailing Normal Map Intensity")
        draw_lut_r_slider(layout, column(23), text="Scale")

    def primary_color():
        draw_centered_label(layout, "Primary Color")
        draw_lut_color(layout, column(1))

    def mask1():
        draw_centered_label(layout, "Mask 1")
        draw_lut_color(layout, column(3))
        draw_lut_b_slider(layout, column(2), text="Application Inversion")
        draw_lut_g_slider(layout, column(23), text="Matte [0 to 1]")
        draw_lut_b_slider(layout, column(23), text="Gloss [0 to 1]")
        draw_generic_mask_sliders(layout, column(4))

    def mask2():
        draw_centered_label(layout, "Mask 2")
        split = layout.split(factor=0.5)
        col1 = split.column()
        draw_centered_label(col1, "Inner Color")
        draw_lut_color(col1, column(6)) # inner
        col2 = split.column()
        draw_centered_label(col2, "Outer Color")
        draw_lut_color(col2, column(7)) # outer
        draw_lut_a_slider(layout, column(2), text="Application Inversion")
        draw_generic_mask_sliders(layout, column(5))

    def metallic():
        draw_centered_label(layout, "Metallic (Mask 3)")
        draw_lut_a_slider(layout, column(7), text="Application Inversion")
        draw_generic_mask_sliders(layout, column(8))

    def gloss():
        draw_centered_label(layout, "Gloss (Mask 4)")
        draw_generic_mask_sliders(layout, column(10))

    def camo():
        draw_centered_label(layout, "Camo (Mask 5)")
        layout.prop(column(22), "camo_type")
        draw_lut_a_slider(layout, column(21), "Application Inversion")
        split = layout.split(factor=0.5)
        col1 = split.column()
        col2 = split.column()
        draw_lut_color(col1, column(17)) # color 1
        draw_lut_color(col2, column(18)) # color 2
        draw_lut_color(col1, column(19)) # color 3
        draw_lut_color(col2, column(20)) # color 4
        draw_lut_b_slider(layout, column(22), text="Size")
        draw_lut_r_slider(layout, column(22), text="Sharpness")
        draw_lut_a_slider(layout, column(23), text="Roughness")
        draw_lut_a_slider(layout,column(17), text="Roughness Inversion")
        draw_lut_g_slider(layout, column(22), text="Green Channel Strength")

        split = layout.split(factor=0.2)
        col1 = split.column()
        col1.label(text="Detail Map")
        row = split.column().row()
        draw_lut_a_slider(row, column(18), text="Blue Channel")
        draw_lut_a_slider(row, column(19), text="Alpha Channel")

        split = layout.split(factor=0.2)
        col1 = split.column()
        col1.label(text="Normal Map")
        row = split.column().row()
        row.label(text="No control")
        draw_lut_a_slider(row, column(20), text="Curvature")
        

        # TODO: Column 16 with how it affects camo
        # NOTE: Column 16 has a really complex interaction with the mask 2 inner and outer colors.
        # It seems to pick complimentry colors for both and then do some more math on them and use
        # the bump map to pick which color is drawn. This creates really weird but colorful bump-map-shaped
        # patterns on the surface

    def special():
        draw_centered_label(layout, "Special")
        draw_lut_b_slider(layout, column(11), text="Rim Brightening")
        layout.label(text="Curvature Gradient")
        split = layout.split(factor=0.5)
        col1 = split.column()
        col2 = split.column()
    
        draw_lut_color(col1, column(13))
        draw_lut_a_slider(col2, column(13), text="Intensity [0 to 1]")
        layout.label(text="Tint Override")
        split = layout.split(factor=0.5)
        col1 = split.column()
        col2 = split.column()
    
        draw_lut_color(col1, column(15))
        draw_lut_a_slider(col2, column(15), text="Intensity?")

    surface_properties()
    detail_map()
    primary_color()
    mask1()
    mask2()
    metallic()
    gloss()
    camo()
    special()


def draw_lut_row_legacy(layout: bpy.types.UILayout, bridge: BPYLUTBridge):
    def draw_lut_row(col: bpy.types.UILayout, row_index: int):
        x_dim,y = bridge.lut.dim()
        for x in range(x_dim):
            pixel_index = x_dim*row_index+x
            pixel = bridge.lut_property.lut[pixel_index]
            
            draw_lut_pixel(col, pixel, x+1)
            #draw_lut_color_with_alpha_slider(col, pixel)
    
    draw_lut_row(layout, bridge.lut_property.selected_row-1)

def draw_lut_pixel(col: bpy.types.UILayout, pixel: LUTPixelProperty, column_index: int):
    column_name_map: Dict[int, str] = {
        1: "Primary Color",
        2: "Bump Map Selection & Inversion Controls",
        3: "Bump Map Mask 1 Color",
        4: "Bump Map Mask 1",
        5: "Bump Map Mask 2",
        6: "Bump Map Mask 2 Inner Color",
        7: "Bump Map Mask 2 Outer Color",
        8: "Bump Map Metallic Mask (Mask 3)",
        # 9
        10: "Bump Map Gloss Mask (Mask 4)",
        11: "Roughness / Rim Brightening",
        # 12
        13: "Curvature Gradient",
        14: "Emissive",
        15: "Tint Override (Keep Zero)",
        # 16
        17: "Camo Color 1",
        18: "Camo Color 2",
        19: "Camo Color 3",
        20: "Camo Color 4",
        21: "Mask 5 Inversion Control",
        22: "Camo Controls",
        23: "Bump Map Scaling & Mask 1 Matte/Gloss"
    }

    column_title = column_name_map[column_index] if column_index in column_name_map else "Unknown"
    col.label(text=f"Column {column_index}: {column_title}")
    match column_index:
        case 1:
            draw_lut_color(col, pixel)
            col.prop(pixel, "col1_a")
        case 2:
            split = col.split(factor=0.8)
            split.column().prop(pixel, "bump_map_index_enum")
            split.column().prop(pixel, "bump_map_index_int", text="")
            #row = col.row()
            
            draw_lut_g_slider(col, pixel, text="Bump Map Red & Green Channel Intensity")
            draw_lut_b_slider(col, pixel, text="Column 4 Application Inversion")
            draw_lut_a_slider(col, pixel, text="Column 5 Application Inversion")
        case 3:
            draw_lut_color(col, pixel)
            # alpha disabled
            prev = col.enabled
            col.enabled = False
            draw_lut_a_slider(col, pixel, "N/A")
            col.enabled = prev
        case 4:
            draw_lut_rgba_sliders(col, pixel,
                "Bump Map Blue Channel Mask",
                "Bump Map Alpha Channel Mask",
                "Normal Map Alpha Channel Mask",
                "Normal Map Blue Channel Mask")
        case 5:
            draw_lut_rgba_sliders(col, pixel,
                "Bump Map Blue Channel Mask",
                "Bump Map Alpha Channel Mask",
                "Normal Map Alpha Channel Mask",
                "Normal Map Blue Channel Mask")
        case 6:
            draw_lut_color_with_alpha_slider(col, pixel, "Unknown")
        case 7:
            draw_lut_color_with_alpha_slider(col, pixel, "Column 8 Application Inversion")
        case 8:
            draw_lut_rgba_sliders(col, pixel,
                "Bump Map Blue Channel Metallic Mask",
                "Bump Map Alpha Channel Metallic Mask",
                "Normal Map Alpha Channel Metallic Mask",
                "Normal Map Blue Channel Metallic Mask")
        # 9 unknown
        case 10:
            draw_lut_rgba_sliders(col, pixel,
                "Bump Map Blue Channel Gloss Mask",
                "Bump map Alpha Channel Gloss Mask",
                "Normal Map Alpha Channel Gloss Mask",
                "Normal Map Blue Channel Gloss Mask")
        case 11:
            draw_lut_rgba_sliders(col, pixel,
                "Roughness [0 to 10]",
                "Unknown",
                "Rim Brightening",
                "Unknown")
        # 12 unknown
        case 13:
            draw_lut_color_with_alpha_slider(col, pixel, "Intensity [0 to 1]")
        case 14:
            draw_lut_rgba_sliders(col, pixel,
                "Emissive [0 to 0.06]",
                "Unknown",
                "Unknown",
                "Unknown")
        case 15:
            draw_lut_color_with_alpha_slider(col, pixel)
        case 16:
            draw_lut_rgba_sliders(col, pixel,
                "Unknown",
                "Unknown",
                "Unknown",
                "Unknown")
        case 17:
            draw_lut_color_with_alpha_slider(col, pixel, "Camo Roughness Inversion")
        case 18:
            draw_lut_color_with_alpha_slider(col, pixel, "Bump Map Blue Channel Mask 5")
        case 19:
            draw_lut_color_with_alpha_slider(col, pixel, "Bump Map Alpha Channel Mask 5")
        case 20:
            draw_lut_color_with_alpha_slider(col, pixel, "Normal Map Alpha Channel Mask 5")
        case 21:
            draw_lut_rgba_sliders(col, pixel,
                    "Unknown",
                    "Unknown",
                    "Unknown",
                    "Mask 5 Application Inversion")
        case 22:
            draw_lut_r_slider(col, pixel, "Camo Sharpness")
            draw_lut_g_slider(col, pixel, "Camo Green Channel Strength")
            draw_lut_b_slider(col, pixel, "Camo Size")
            col.prop(pixel, "camo_type")
        case 23:
            draw_lut_rgba_sliders(col, pixel,
                "Bump Map Scaling",
                "Bump Map Mask 1 Matte [0 to 1]",
                "Bump Map Mask 1 Gloss [-1 to 1]",
                "Camo Roughness")
        
        case _:
            draw_lut_rgba_sliders(col, pixel)
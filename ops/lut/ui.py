import bpy
from typing import Dict
from .properties import LUTPixelProperty

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
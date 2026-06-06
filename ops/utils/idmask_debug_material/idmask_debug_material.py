import bpy
import mathutils
import os
import typing


def onehot_8_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize onehot-8 node group"""
    onehot_8_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "onehot-8")

    onehot_8_1.color_tag = 'NONE'
    onehot_8_1.description = ""
    onehot_8_1.default_group_node_width = 140
    # onehot_8_1 interface

    # Socket 1
    _1_socket = onehot_8_1.interface.new_socket(name="1", in_out='OUTPUT', socket_type='NodeSocketFloat')
    _1_socket.default_value = 0.0
    _1_socket.min_value = -3.4028234663852886e+38
    _1_socket.max_value = 3.4028234663852886e+38
    _1_socket.subtype = 'NONE'
    _1_socket.attribute_domain = 'POINT'

    # Socket 2
    _2_socket = onehot_8_1.interface.new_socket(name="2", in_out='OUTPUT', socket_type='NodeSocketFloat')
    _2_socket.default_value = 0.0
    _2_socket.min_value = -3.4028234663852886e+38
    _2_socket.max_value = 3.4028234663852886e+38
    _2_socket.subtype = 'NONE'
    _2_socket.attribute_domain = 'POINT'

    # Socket 3
    _3_socket = onehot_8_1.interface.new_socket(name="3", in_out='OUTPUT', socket_type='NodeSocketFloat')
    _3_socket.default_value = 0.0
    _3_socket.min_value = -3.4028234663852886e+38
    _3_socket.max_value = 3.4028234663852886e+38
    _3_socket.subtype = 'NONE'
    _3_socket.attribute_domain = 'POINT'

    # Socket 4
    _4_socket = onehot_8_1.interface.new_socket(name="4", in_out='OUTPUT', socket_type='NodeSocketFloat')
    _4_socket.default_value = 0.0
    _4_socket.min_value = -3.4028234663852886e+38
    _4_socket.max_value = 3.4028234663852886e+38
    _4_socket.subtype = 'NONE'
    _4_socket.attribute_domain = 'POINT'

    # Socket 5
    _5_socket = onehot_8_1.interface.new_socket(name="5", in_out='OUTPUT', socket_type='NodeSocketFloat')
    _5_socket.default_value = 0.0
    _5_socket.min_value = -3.4028234663852886e+38
    _5_socket.max_value = 3.4028234663852886e+38
    _5_socket.subtype = 'NONE'
    _5_socket.attribute_domain = 'POINT'

    # Socket 6
    _6_socket = onehot_8_1.interface.new_socket(name="6", in_out='OUTPUT', socket_type='NodeSocketFloat')
    _6_socket.default_value = 0.0
    _6_socket.min_value = -3.4028234663852886e+38
    _6_socket.max_value = 3.4028234663852886e+38
    _6_socket.subtype = 'NONE'
    _6_socket.attribute_domain = 'POINT'

    # Socket 7
    _7_socket = onehot_8_1.interface.new_socket(name="7", in_out='OUTPUT', socket_type='NodeSocketFloat')
    _7_socket.default_value = 0.0
    _7_socket.min_value = -3.4028234663852886e+38
    _7_socket.max_value = 3.4028234663852886e+38
    _7_socket.subtype = 'NONE'
    _7_socket.attribute_domain = 'POINT'

    # Socket 8
    _8_socket = onehot_8_1.interface.new_socket(name="8", in_out='OUTPUT', socket_type='NodeSocketFloat')
    _8_socket.default_value = 0.0
    _8_socket.min_value = -3.4028234663852886e+38
    _8_socket.max_value = 3.4028234663852886e+38
    _8_socket.subtype = 'NONE'
    _8_socket.attribute_domain = 'POINT'

    # Socket 1
    _1_socket_1 = onehot_8_1.interface.new_socket(name="1", in_out='INPUT', socket_type='NodeSocketFloat')
    _1_socket_1.default_value = 0.5
    _1_socket_1.min_value = -10000.0
    _1_socket_1.max_value = 10000.0
    _1_socket_1.subtype = 'NONE'
    _1_socket_1.attribute_domain = 'POINT'

    # Socket 2
    _2_socket_1 = onehot_8_1.interface.new_socket(name="2", in_out='INPUT', socket_type='NodeSocketFloat')
    _2_socket_1.default_value = 0.5
    _2_socket_1.min_value = -10000.0
    _2_socket_1.max_value = 10000.0
    _2_socket_1.subtype = 'NONE'
    _2_socket_1.attribute_domain = 'POINT'

    # Socket 3
    _3_socket_1 = onehot_8_1.interface.new_socket(name="3", in_out='INPUT', socket_type='NodeSocketFloat')
    _3_socket_1.default_value = 0.5
    _3_socket_1.min_value = -10000.0
    _3_socket_1.max_value = 10000.0
    _3_socket_1.subtype = 'NONE'
    _3_socket_1.attribute_domain = 'POINT'

    # Socket 4
    _4_socket_1 = onehot_8_1.interface.new_socket(name="4", in_out='INPUT', socket_type='NodeSocketFloat')
    _4_socket_1.default_value = 0.5
    _4_socket_1.min_value = -10000.0
    _4_socket_1.max_value = 10000.0
    _4_socket_1.subtype = 'NONE'
    _4_socket_1.attribute_domain = 'POINT'

    # Socket 5
    _5_socket_1 = onehot_8_1.interface.new_socket(name="5", in_out='INPUT', socket_type='NodeSocketFloat')
    _5_socket_1.default_value = 0.5
    _5_socket_1.min_value = -10000.0
    _5_socket_1.max_value = 10000.0
    _5_socket_1.subtype = 'NONE'
    _5_socket_1.attribute_domain = 'POINT'

    # Socket 6
    _6_socket_1 = onehot_8_1.interface.new_socket(name="6", in_out='INPUT', socket_type='NodeSocketFloat')
    _6_socket_1.default_value = 0.5
    _6_socket_1.min_value = -10000.0
    _6_socket_1.max_value = 10000.0
    _6_socket_1.subtype = 'NONE'
    _6_socket_1.attribute_domain = 'POINT'

    # Socket 7
    _7_socket_1 = onehot_8_1.interface.new_socket(name="7", in_out='INPUT', socket_type='NodeSocketFloat')
    _7_socket_1.default_value = 0.5
    _7_socket_1.min_value = -10000.0
    _7_socket_1.max_value = 10000.0
    _7_socket_1.subtype = 'NONE'
    _7_socket_1.attribute_domain = 'POINT'

    # Socket 8
    _8_socket_1 = onehot_8_1.interface.new_socket(name="8", in_out='INPUT', socket_type='NodeSocketFloat')
    _8_socket_1.default_value = 0.5
    _8_socket_1.min_value = -10000.0
    _8_socket_1.max_value = 10000.0
    _8_socket_1.subtype = 'NONE'
    _8_socket_1.attribute_domain = 'POINT'

    # Initialize onehot_8_1 nodes

    # Node Group Output
    group_output = onehot_8_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.show_options = True
    group_output.is_active_output = True

    # Node Group Input
    group_input = onehot_8_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.show_options = True

    # Node Math
    math = onehot_8_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.hide = True
    math.show_options = True
    math.operation = 'MAXIMUM'
    math.use_clamp = False

    # Node Math.001
    math_001 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.hide = True
    math_001.show_options = True
    math_001.operation = 'MAXIMUM'
    math_001.use_clamp = False

    # Node Math.002
    math_002 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.hide = True
    math_002.show_options = True
    math_002.operation = 'MAXIMUM'
    math_002.use_clamp = False

    # Node Math.003
    math_003 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.hide = True
    math_003.show_options = True
    math_003.operation = 'MAXIMUM'
    math_003.use_clamp = False

    # Node Math.004
    math_004 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.hide = True
    math_004.show_options = True
    math_004.operation = 'MAXIMUM'
    math_004.use_clamp = False

    # Node Math.005
    math_005 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.hide = True
    math_005.show_options = True
    math_005.operation = 'MAXIMUM'
    math_005.use_clamp = False

    # Node Math.006
    math_006 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.hide = True
    math_006.show_options = True
    math_006.operation = 'MAXIMUM'
    math_006.use_clamp = False

    # Node Math.008
    math_008 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.hide = True
    math_008.show_options = True
    math_008.operation = 'SUBTRACT'
    math_008.use_clamp = False

    # Node Math.007
    math_007 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.hide = True
    math_007.show_options = True
    math_007.operation = 'SIGN'
    math_007.use_clamp = False

    # Node Math.016
    math_016 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_016.name = "Math.016"
    math_016.hide = True
    math_016.show_options = True
    math_016.operation = 'ADD'
    math_016.use_clamp = True
    # Value
    math_016.inputs[0].default_value = 1.0

    # Node Reroute
    reroute = onehot_8_1.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.show_options = True
    reroute.socket_idname = "NodeSocketFloat"
    # Node Math.017
    math_017 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_017.name = "Math.017"
    math_017.hide = True
    math_017.show_options = True
    math_017.operation = 'MULTIPLY'
    math_017.use_clamp = True

    # Node Math.009
    math_009 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.hide = True
    math_009.show_options = True
    math_009.operation = 'SUBTRACT'
    math_009.use_clamp = False

    # Node Math.010
    math_010 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.hide = True
    math_010.show_options = True
    math_010.operation = 'SIGN'
    math_010.use_clamp = False

    # Node Math.018
    math_018 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_018.name = "Math.018"
    math_018.hide = True
    math_018.show_options = True
    math_018.operation = 'ADD'
    math_018.use_clamp = True
    # Value
    math_018.inputs[0].default_value = 1.0

    # Node Reroute.001
    reroute_001 = onehot_8_1.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.show_options = True
    reroute_001.socket_idname = "NodeSocketFloat"
    # Node Math.019
    math_019 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_019.name = "Math.019"
    math_019.hide = True
    math_019.show_options = True
    math_019.operation = 'MULTIPLY'
    math_019.use_clamp = True

    # Node Math.011
    math_011 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.hide = True
    math_011.show_options = True
    math_011.operation = 'SUBTRACT'
    math_011.use_clamp = False

    # Node Math.012
    math_012 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.hide = True
    math_012.show_options = True
    math_012.operation = 'SIGN'
    math_012.use_clamp = False

    # Node Math.020
    math_020 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_020.name = "Math.020"
    math_020.hide = True
    math_020.show_options = True
    math_020.operation = 'ADD'
    math_020.use_clamp = True
    # Value
    math_020.inputs[0].default_value = 1.0

    # Node Reroute.002
    reroute_002 = onehot_8_1.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.show_options = True
    reroute_002.socket_idname = "NodeSocketFloat"
    # Node Math.021
    math_021 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_021.name = "Math.021"
    math_021.hide = True
    math_021.show_options = True
    math_021.operation = 'MULTIPLY'
    math_021.use_clamp = True

    # Node Math.013
    math_013 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_013.name = "Math.013"
    math_013.hide = True
    math_013.show_options = True
    math_013.operation = 'SUBTRACT'
    math_013.use_clamp = False

    # Node Math.014
    math_014 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.hide = True
    math_014.show_options = True
    math_014.operation = 'SIGN'
    math_014.use_clamp = False

    # Node Math.022
    math_022 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_022.name = "Math.022"
    math_022.hide = True
    math_022.show_options = True
    math_022.operation = 'ADD'
    math_022.use_clamp = True
    # Value
    math_022.inputs[0].default_value = 1.0

    # Node Reroute.003
    reroute_003 = onehot_8_1.nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.show_options = True
    reroute_003.socket_idname = "NodeSocketFloat"
    # Node Math.023
    math_023 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_023.name = "Math.023"
    math_023.hide = True
    math_023.show_options = True
    math_023.operation = 'MULTIPLY'
    math_023.use_clamp = True

    # Node Math.015
    math_015 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_015.name = "Math.015"
    math_015.hide = True
    math_015.show_options = True
    math_015.operation = 'SUBTRACT'
    math_015.use_clamp = False

    # Node Math.024
    math_024 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_024.name = "Math.024"
    math_024.hide = True
    math_024.show_options = True
    math_024.operation = 'SIGN'
    math_024.use_clamp = False

    # Node Math.025
    math_025 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_025.name = "Math.025"
    math_025.hide = True
    math_025.show_options = True
    math_025.operation = 'ADD'
    math_025.use_clamp = True
    # Value
    math_025.inputs[0].default_value = 1.0

    # Node Reroute.004
    reroute_004 = onehot_8_1.nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    reroute_004.show_options = True
    reroute_004.socket_idname = "NodeSocketFloat"
    # Node Math.026
    math_026 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_026.name = "Math.026"
    math_026.hide = True
    math_026.show_options = True
    math_026.operation = 'MULTIPLY'
    math_026.use_clamp = True

    # Node Math.027
    math_027 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_027.name = "Math.027"
    math_027.hide = True
    math_027.show_options = True
    math_027.operation = 'SUBTRACT'
    math_027.use_clamp = False

    # Node Math.028
    math_028 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_028.name = "Math.028"
    math_028.hide = True
    math_028.show_options = True
    math_028.operation = 'SIGN'
    math_028.use_clamp = False

    # Node Math.029
    math_029 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_029.name = "Math.029"
    math_029.hide = True
    math_029.show_options = True
    math_029.operation = 'ADD'
    math_029.use_clamp = True
    # Value
    math_029.inputs[0].default_value = 1.0

    # Node Reroute.005
    reroute_005 = onehot_8_1.nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    reroute_005.show_options = True
    reroute_005.socket_idname = "NodeSocketFloat"
    # Node Math.030
    math_030 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_030.name = "Math.030"
    math_030.hide = True
    math_030.show_options = True
    math_030.operation = 'MULTIPLY'
    math_030.use_clamp = True

    # Node Math.031
    math_031 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_031.name = "Math.031"
    math_031.hide = True
    math_031.show_options = True
    math_031.operation = 'SUBTRACT'
    math_031.use_clamp = False

    # Node Math.032
    math_032 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_032.name = "Math.032"
    math_032.hide = True
    math_032.show_options = True
    math_032.operation = 'SIGN'
    math_032.use_clamp = False

    # Node Math.033
    math_033 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_033.name = "Math.033"
    math_033.hide = True
    math_033.show_options = True
    math_033.operation = 'ADD'
    math_033.use_clamp = True
    # Value
    math_033.inputs[0].default_value = 1.0

    # Node Reroute.006
    reroute_006 = onehot_8_1.nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    reroute_006.show_options = True
    reroute_006.socket_idname = "NodeSocketFloat"
    # Node Math.034
    math_034 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_034.name = "Math.034"
    math_034.hide = True
    math_034.show_options = True
    math_034.operation = 'MULTIPLY'
    math_034.use_clamp = True

    # Node Math.035
    math_035 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_035.name = "Math.035"
    math_035.hide = True
    math_035.show_options = True
    math_035.operation = 'SUBTRACT'
    math_035.use_clamp = False

    # Node Math.036
    math_036 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_036.name = "Math.036"
    math_036.hide = True
    math_036.show_options = True
    math_036.operation = 'SIGN'
    math_036.use_clamp = False

    # Node Math.037
    math_037 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_037.name = "Math.037"
    math_037.hide = True
    math_037.show_options = True
    math_037.operation = 'ADD'
    math_037.use_clamp = True
    # Value
    math_037.inputs[0].default_value = 1.0

    # Node Reroute.007
    reroute_007 = onehot_8_1.nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    reroute_007.show_options = True
    reroute_007.socket_idname = "NodeSocketFloat"
    # Node Math.038
    math_038 = onehot_8_1.nodes.new("ShaderNodeMath")
    math_038.name = "Math.038"
    math_038.hide = True
    math_038.show_options = True
    math_038.operation = 'MULTIPLY'
    math_038.use_clamp = True

    # Node Reroute.008
    reroute_008 = onehot_8_1.nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    reroute_008.show_options = True
    reroute_008.socket_idname = "NodeSocketFloat"
    # Node Reroute.009
    reroute_009 = onehot_8_1.nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    reroute_009.show_options = True
    reroute_009.socket_idname = "NodeSocketFloat"
    # Node Reroute.010
    reroute_010 = onehot_8_1.nodes.new("NodeReroute")
    reroute_010.name = "Reroute.010"
    reroute_010.show_options = True
    reroute_010.socket_idname = "NodeSocketFloat"
    # Node Reroute.011
    reroute_011 = onehot_8_1.nodes.new("NodeReroute")
    reroute_011.name = "Reroute.011"
    reroute_011.show_options = True
    reroute_011.socket_idname = "NodeSocketFloat"
    # Node Reroute.012
    reroute_012 = onehot_8_1.nodes.new("NodeReroute")
    reroute_012.name = "Reroute.012"
    reroute_012.show_options = True
    reroute_012.socket_idname = "NodeSocketFloat"
    # Node Reroute.013
    reroute_013 = onehot_8_1.nodes.new("NodeReroute")
    reroute_013.name = "Reroute.013"
    reroute_013.show_options = True
    reroute_013.socket_idname = "NodeSocketFloat"
    # Node Reroute.014
    reroute_014 = onehot_8_1.nodes.new("NodeReroute")
    reroute_014.name = "Reroute.014"
    reroute_014.show_options = True
    reroute_014.socket_idname = "NodeSocketFloat"
    # Node Reroute.015
    reroute_015 = onehot_8_1.nodes.new("NodeReroute")
    reroute_015.name = "Reroute.015"
    reroute_015.show_options = True
    reroute_015.socket_idname = "NodeSocketFloat"
    # Set locations
    onehot_8_1.nodes["Group Output"].location = (1511.240234375, -332.15655517578125)
    onehot_8_1.nodes["Group Input"].location = (-899.4000854492188, 35.87530517578125)
    onehot_8_1.nodes["Math"].location = (-199.48587036132812, 212.14541625976562)
    onehot_8_1.nodes["Math.001"].location = (-201.21881103515625, 174.23800659179688)
    onehot_8_1.nodes["Math.002"].location = (-204.28018188476562, 136.93887329101562)
    onehot_8_1.nodes["Math.003"].location = (-204.65756225585938, 89.59414672851562)
    onehot_8_1.nodes["Math.004"].location = (-11.254947662353516, 176.30532836914062)
    onehot_8_1.nodes["Math.005"].location = (-12.82668685913086, 134.21926879882812)
    onehot_8_1.nodes["Math.006"].location = (168.00811767578125, 154.26168823242188)
    onehot_8_1.nodes["Math.008"].location = (475.980224609375, -90.90531921386719)
    onehot_8_1.nodes["Math.007"].location = (651.24072265625, -88.51588439941406)
    onehot_8_1.nodes["Math.016"].location = (817.7982788085938, -80.89851379394531)
    onehot_8_1.nodes["Reroute"].location = (426.6762390136719, -130.55538940429688)
    onehot_8_1.nodes["Math.017"].location = (980.9296264648438, -122.63513946533203)
    onehot_8_1.nodes["Math.009"].location = (472.8122253417969, -183.9191436767578)
    onehot_8_1.nodes["Math.010"].location = (648.07275390625, -181.5297088623047)
    onehot_8_1.nodes["Math.018"].location = (814.6302490234375, -173.91233825683594)
    onehot_8_1.nodes["Reroute.001"].location = (426.6762390136719, -226.42422485351562)
    onehot_8_1.nodes["Math.019"].location = (977.7615966796875, -215.6489715576172)
    onehot_8_1.nodes["Math.011"].location = (474.072021484375, -265.87744140625)
    onehot_8_1.nodes["Math.012"].location = (649.33251953125, -263.48797607421875)
    onehot_8_1.nodes["Math.020"].location = (815.8900756835938, -255.87062072753906)
    onehot_8_1.nodes["Reroute.002"].location = (426.6762390136719, -315.40374755859375)
    onehot_8_1.nodes["Math.021"].location = (979.0214233398438, -297.60723876953125)
    onehot_8_1.nodes["Math.013"].location = (469.03271484375, -364.2273864746094)
    onehot_8_1.nodes["Math.014"].location = (644.293212890625, -361.8379211425781)
    onehot_8_1.nodes["Math.022"].location = (810.8507690429688, -354.2205505371094)
    onehot_8_1.nodes["Reroute.003"].location = (426.6762390136719, -407.82794189453125)
    onehot_8_1.nodes["Math.023"].location = (973.9821166992188, -395.9571838378906)
    onehot_8_1.nodes["Math.015"].location = (466.92462158203125, -463.76739501953125)
    onehot_8_1.nodes["Math.024"].location = (642.1851196289062, -461.3779296875)
    onehot_8_1.nodes["Math.025"].location = (808.74267578125, -453.76055908203125)
    onehot_8_1.nodes["Reroute.004"].location = (426.6762390136719, -508.86376953125)
    onehot_8_1.nodes["Math.026"].location = (971.8740234375, -495.4971923828125)
    onehot_8_1.nodes["Math.027"].location = (463.7410583496094, -540.2384033203125)
    onehot_8_1.nodes["Math.028"].location = (639.0015869140625, -537.8489379882812)
    onehot_8_1.nodes["Math.029"].location = (805.5591430664062, -530.2315673828125)
    onehot_8_1.nodes["Reroute.005"].location = (426.6762390136719, -578.8975830078125)
    onehot_8_1.nodes["Math.030"].location = (968.6904907226562, -571.9682006835938)
    onehot_8_1.nodes["Math.031"].location = (457.37384033203125, -615.1162719726562)
    onehot_8_1.nodes["Math.032"].location = (632.6343383789062, -612.726806640625)
    onehot_8_1.nodes["Math.033"].location = (799.19189453125, -605.1094360351562)
    onehot_8_1.nodes["Reroute.006"].location = (426.6762390136719, -657.5430297851562)
    onehot_8_1.nodes["Math.034"].location = (962.3232421875, -646.8460693359375)
    onehot_8_1.nodes["Math.035"].location = (454.1903076171875, -696.36669921875)
    onehot_8_1.nodes["Math.036"].location = (629.4508056640625, -693.977294921875)
    onehot_8_1.nodes["Math.037"].location = (796.0083618164062, -686.35986328125)
    onehot_8_1.nodes["Reroute.007"].location = (426.6762390136719, -746.5225219726562)
    onehot_8_1.nodes["Math.038"].location = (959.1397094726562, -728.0965576171875)
    onehot_8_1.nodes["Reroute.008"].location = (355.5816650390625, -697.1804809570312)
    onehot_8_1.nodes["Reroute.009"].location = (354.3686218261719, -618.709716796875)
    onehot_8_1.nodes["Reroute.010"].location = (353.7618103027344, -543.3388671875)
    onehot_8_1.nodes["Reroute.011"].location = (352.87469482421875, -472.09112548828125)
    onehot_8_1.nodes["Reroute.012"].location = (353.0126037597656, -372.45037841796875)
    onehot_8_1.nodes["Reroute.013"].location = (354.14349365234375, -272.3766174316406)
    onehot_8_1.nodes["Reroute.014"].location = (355.3126525878906, -188.59765625)
    onehot_8_1.nodes["Reroute.015"].location = (354.1473388671875, -94.12455749511719)

    # Set dimensions
    onehot_8_1.nodes["Group Output"].width  = 140.0
    onehot_8_1.nodes["Group Output"].height = 100.0

    onehot_8_1.nodes["Group Input"].width  = 140.0
    onehot_8_1.nodes["Group Input"].height = 100.0

    onehot_8_1.nodes["Math"].width  = 140.0
    onehot_8_1.nodes["Math"].height = 100.0

    onehot_8_1.nodes["Math.001"].width  = 140.0
    onehot_8_1.nodes["Math.001"].height = 100.0

    onehot_8_1.nodes["Math.002"].width  = 140.0
    onehot_8_1.nodes["Math.002"].height = 100.0

    onehot_8_1.nodes["Math.003"].width  = 140.0
    onehot_8_1.nodes["Math.003"].height = 100.0

    onehot_8_1.nodes["Math.004"].width  = 140.0
    onehot_8_1.nodes["Math.004"].height = 100.0

    onehot_8_1.nodes["Math.005"].width  = 140.0
    onehot_8_1.nodes["Math.005"].height = 100.0

    onehot_8_1.nodes["Math.006"].width  = 140.0
    onehot_8_1.nodes["Math.006"].height = 100.0

    onehot_8_1.nodes["Math.008"].width  = 140.0
    onehot_8_1.nodes["Math.008"].height = 100.0

    onehot_8_1.nodes["Math.007"].width  = 140.0
    onehot_8_1.nodes["Math.007"].height = 100.0

    onehot_8_1.nodes["Math.016"].width  = 140.0
    onehot_8_1.nodes["Math.016"].height = 100.0

    onehot_8_1.nodes["Reroute"].width  = 16.0
    onehot_8_1.nodes["Reroute"].height = 100.0

    onehot_8_1.nodes["Math.017"].width  = 140.0
    onehot_8_1.nodes["Math.017"].height = 100.0

    onehot_8_1.nodes["Math.009"].width  = 140.0
    onehot_8_1.nodes["Math.009"].height = 100.0

    onehot_8_1.nodes["Math.010"].width  = 140.0
    onehot_8_1.nodes["Math.010"].height = 100.0

    onehot_8_1.nodes["Math.018"].width  = 140.0
    onehot_8_1.nodes["Math.018"].height = 100.0

    onehot_8_1.nodes["Reroute.001"].width  = 16.0
    onehot_8_1.nodes["Reroute.001"].height = 100.0

    onehot_8_1.nodes["Math.019"].width  = 140.0
    onehot_8_1.nodes["Math.019"].height = 100.0

    onehot_8_1.nodes["Math.011"].width  = 140.0
    onehot_8_1.nodes["Math.011"].height = 100.0

    onehot_8_1.nodes["Math.012"].width  = 140.0
    onehot_8_1.nodes["Math.012"].height = 100.0

    onehot_8_1.nodes["Math.020"].width  = 140.0
    onehot_8_1.nodes["Math.020"].height = 100.0

    onehot_8_1.nodes["Reroute.002"].width  = 16.0
    onehot_8_1.nodes["Reroute.002"].height = 100.0

    onehot_8_1.nodes["Math.021"].width  = 140.0
    onehot_8_1.nodes["Math.021"].height = 100.0

    onehot_8_1.nodes["Math.013"].width  = 140.0
    onehot_8_1.nodes["Math.013"].height = 100.0

    onehot_8_1.nodes["Math.014"].width  = 140.0
    onehot_8_1.nodes["Math.014"].height = 100.0

    onehot_8_1.nodes["Math.022"].width  = 140.0
    onehot_8_1.nodes["Math.022"].height = 100.0

    onehot_8_1.nodes["Reroute.003"].width  = 16.0
    onehot_8_1.nodes["Reroute.003"].height = 100.0

    onehot_8_1.nodes["Math.023"].width  = 140.0
    onehot_8_1.nodes["Math.023"].height = 100.0

    onehot_8_1.nodes["Math.015"].width  = 140.0
    onehot_8_1.nodes["Math.015"].height = 100.0

    onehot_8_1.nodes["Math.024"].width  = 140.0
    onehot_8_1.nodes["Math.024"].height = 100.0

    onehot_8_1.nodes["Math.025"].width  = 140.0
    onehot_8_1.nodes["Math.025"].height = 100.0

    onehot_8_1.nodes["Reroute.004"].width  = 16.0
    onehot_8_1.nodes["Reroute.004"].height = 100.0

    onehot_8_1.nodes["Math.026"].width  = 140.0
    onehot_8_1.nodes["Math.026"].height = 100.0

    onehot_8_1.nodes["Math.027"].width  = 140.0
    onehot_8_1.nodes["Math.027"].height = 100.0

    onehot_8_1.nodes["Math.028"].width  = 140.0
    onehot_8_1.nodes["Math.028"].height = 100.0

    onehot_8_1.nodes["Math.029"].width  = 140.0
    onehot_8_1.nodes["Math.029"].height = 100.0

    onehot_8_1.nodes["Reroute.005"].width  = 16.0
    onehot_8_1.nodes["Reroute.005"].height = 100.0

    onehot_8_1.nodes["Math.030"].width  = 140.0
    onehot_8_1.nodes["Math.030"].height = 100.0

    onehot_8_1.nodes["Math.031"].width  = 140.0
    onehot_8_1.nodes["Math.031"].height = 100.0

    onehot_8_1.nodes["Math.032"].width  = 140.0
    onehot_8_1.nodes["Math.032"].height = 100.0

    onehot_8_1.nodes["Math.033"].width  = 140.0
    onehot_8_1.nodes["Math.033"].height = 100.0

    onehot_8_1.nodes["Reroute.006"].width  = 16.0
    onehot_8_1.nodes["Reroute.006"].height = 100.0

    onehot_8_1.nodes["Math.034"].width  = 140.0
    onehot_8_1.nodes["Math.034"].height = 100.0

    onehot_8_1.nodes["Math.035"].width  = 140.0
    onehot_8_1.nodes["Math.035"].height = 100.0

    onehot_8_1.nodes["Math.036"].width  = 140.0
    onehot_8_1.nodes["Math.036"].height = 100.0

    onehot_8_1.nodes["Math.037"].width  = 140.0
    onehot_8_1.nodes["Math.037"].height = 100.0

    onehot_8_1.nodes["Reroute.007"].width  = 16.0
    onehot_8_1.nodes["Reroute.007"].height = 100.0

    onehot_8_1.nodes["Math.038"].width  = 140.0
    onehot_8_1.nodes["Math.038"].height = 100.0

    onehot_8_1.nodes["Reroute.008"].width  = 16.0
    onehot_8_1.nodes["Reroute.008"].height = 100.0

    onehot_8_1.nodes["Reroute.009"].width  = 16.0
    onehot_8_1.nodes["Reroute.009"].height = 100.0

    onehot_8_1.nodes["Reroute.010"].width  = 16.0
    onehot_8_1.nodes["Reroute.010"].height = 100.0

    onehot_8_1.nodes["Reroute.011"].width  = 16.0
    onehot_8_1.nodes["Reroute.011"].height = 100.0

    onehot_8_1.nodes["Reroute.012"].width  = 16.0
    onehot_8_1.nodes["Reroute.012"].height = 100.0

    onehot_8_1.nodes["Reroute.013"].width  = 16.0
    onehot_8_1.nodes["Reroute.013"].height = 100.0

    onehot_8_1.nodes["Reroute.014"].width  = 16.0
    onehot_8_1.nodes["Reroute.014"].height = 100.0

    onehot_8_1.nodes["Reroute.015"].width  = 16.0
    onehot_8_1.nodes["Reroute.015"].height = 100.0


    # Initialize onehot_8_1 links

    # group_input.1 -> math.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[0],
        onehot_8_1.nodes["Math"].inputs[0]
    )
    # group_input.2 -> math.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[1],
        onehot_8_1.nodes["Math"].inputs[1]
    )
    # group_input.3 -> math_001.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[2],
        onehot_8_1.nodes["Math.001"].inputs[0]
    )
    # group_input.4 -> math_001.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[3],
        onehot_8_1.nodes["Math.001"].inputs[1]
    )
    # group_input.5 -> math_002.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[4],
        onehot_8_1.nodes["Math.002"].inputs[0]
    )
    # group_input.6 -> math_002.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[5],
        onehot_8_1.nodes["Math.002"].inputs[1]
    )
    # group_input.7 -> math_003.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[6],
        onehot_8_1.nodes["Math.003"].inputs[0]
    )
    # group_input.8 -> math_003.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[7],
        onehot_8_1.nodes["Math.003"].inputs[1]
    )
    # math.Value -> math_004.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math"].outputs[0],
        onehot_8_1.nodes["Math.004"].inputs[0]
    )
    # math_001.Value -> math_004.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.001"].outputs[0],
        onehot_8_1.nodes["Math.004"].inputs[1]
    )
    # math_002.Value -> math_005.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.002"].outputs[0],
        onehot_8_1.nodes["Math.005"].inputs[0]
    )
    # math_003.Value -> math_005.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.003"].outputs[0],
        onehot_8_1.nodes["Math.005"].inputs[1]
    )
    # math_005.Value -> math_006.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.005"].outputs[0],
        onehot_8_1.nodes["Math.006"].inputs[1]
    )
    # math_004.Value -> math_006.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.004"].outputs[0],
        onehot_8_1.nodes["Math.006"].inputs[0]
    )
    # math_008.Value -> math_007.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.008"].outputs[0],
        onehot_8_1.nodes["Math.007"].inputs[0]
    )
    # math_007.Value -> math_016.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.007"].outputs[0],
        onehot_8_1.nodes["Math.016"].inputs[1]
    )
    # reroute.Output -> math_017.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute"].outputs[0],
        onehot_8_1.nodes["Math.017"].inputs[1]
    )
    # math_016.Value -> math_017.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.016"].outputs[0],
        onehot_8_1.nodes["Math.017"].inputs[0]
    )
    # math_017.Value -> group_output.1
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.017"].outputs[0],
        onehot_8_1.nodes["Group Output"].inputs[0]
    )
    # math_009.Value -> math_010.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.009"].outputs[0],
        onehot_8_1.nodes["Math.010"].inputs[0]
    )
    # math_010.Value -> math_018.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.010"].outputs[0],
        onehot_8_1.nodes["Math.018"].inputs[1]
    )
    # reroute_001.Output -> math_019.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.001"].outputs[0],
        onehot_8_1.nodes["Math.019"].inputs[1]
    )
    # math_018.Value -> math_019.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.018"].outputs[0],
        onehot_8_1.nodes["Math.019"].inputs[0]
    )
    # math_011.Value -> math_012.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.011"].outputs[0],
        onehot_8_1.nodes["Math.012"].inputs[0]
    )
    # math_012.Value -> math_020.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.012"].outputs[0],
        onehot_8_1.nodes["Math.020"].inputs[1]
    )
    # reroute_002.Output -> math_021.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.002"].outputs[0],
        onehot_8_1.nodes["Math.021"].inputs[1]
    )
    # math_020.Value -> math_021.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.020"].outputs[0],
        onehot_8_1.nodes["Math.021"].inputs[0]
    )
    # math_013.Value -> math_014.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.013"].outputs[0],
        onehot_8_1.nodes["Math.014"].inputs[0]
    )
    # math_014.Value -> math_022.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.014"].outputs[0],
        onehot_8_1.nodes["Math.022"].inputs[1]
    )
    # reroute_003.Output -> math_023.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.003"].outputs[0],
        onehot_8_1.nodes["Math.023"].inputs[1]
    )
    # math_022.Value -> math_023.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.022"].outputs[0],
        onehot_8_1.nodes["Math.023"].inputs[0]
    )
    # math_015.Value -> math_024.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.015"].outputs[0],
        onehot_8_1.nodes["Math.024"].inputs[0]
    )
    # math_024.Value -> math_025.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.024"].outputs[0],
        onehot_8_1.nodes["Math.025"].inputs[1]
    )
    # reroute_004.Output -> math_026.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.004"].outputs[0],
        onehot_8_1.nodes["Math.026"].inputs[1]
    )
    # math_025.Value -> math_026.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.025"].outputs[0],
        onehot_8_1.nodes["Math.026"].inputs[0]
    )
    # math_027.Value -> math_028.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.027"].outputs[0],
        onehot_8_1.nodes["Math.028"].inputs[0]
    )
    # math_028.Value -> math_029.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.028"].outputs[0],
        onehot_8_1.nodes["Math.029"].inputs[1]
    )
    # reroute_005.Output -> math_030.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.005"].outputs[0],
        onehot_8_1.nodes["Math.030"].inputs[1]
    )
    # math_029.Value -> math_030.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.029"].outputs[0],
        onehot_8_1.nodes["Math.030"].inputs[0]
    )
    # math_031.Value -> math_032.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.031"].outputs[0],
        onehot_8_1.nodes["Math.032"].inputs[0]
    )
    # math_032.Value -> math_033.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.032"].outputs[0],
        onehot_8_1.nodes["Math.033"].inputs[1]
    )
    # reroute_006.Output -> math_034.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.006"].outputs[0],
        onehot_8_1.nodes["Math.034"].inputs[1]
    )
    # math_033.Value -> math_034.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.033"].outputs[0],
        onehot_8_1.nodes["Math.034"].inputs[0]
    )
    # math_035.Value -> math_036.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.035"].outputs[0],
        onehot_8_1.nodes["Math.036"].inputs[0]
    )
    # math_036.Value -> math_037.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.036"].outputs[0],
        onehot_8_1.nodes["Math.037"].inputs[1]
    )
    # reroute_007.Output -> math_038.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.007"].outputs[0],
        onehot_8_1.nodes["Math.038"].inputs[1]
    )
    # math_037.Value -> math_038.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.037"].outputs[0],
        onehot_8_1.nodes["Math.038"].inputs[0]
    )
    # reroute_009.Output -> reroute_008.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.009"].outputs[0],
        onehot_8_1.nodes["Reroute.008"].inputs[0]
    )
    # reroute_010.Output -> reroute_009.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.010"].outputs[0],
        onehot_8_1.nodes["Reroute.009"].inputs[0]
    )
    # reroute_011.Output -> reroute_010.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.011"].outputs[0],
        onehot_8_1.nodes["Reroute.010"].inputs[0]
    )
    # reroute_012.Output -> reroute_011.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.012"].outputs[0],
        onehot_8_1.nodes["Reroute.011"].inputs[0]
    )
    # reroute_013.Output -> reroute_012.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.013"].outputs[0],
        onehot_8_1.nodes["Reroute.012"].inputs[0]
    )
    # reroute_015.Output -> reroute_014.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.015"].outputs[0],
        onehot_8_1.nodes["Reroute.014"].inputs[0]
    )
    # reroute_014.Output -> reroute_013.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.014"].outputs[0],
        onehot_8_1.nodes["Reroute.013"].inputs[0]
    )
    # math_006.Value -> reroute_015.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.006"].outputs[0],
        onehot_8_1.nodes["Reroute.015"].inputs[0]
    )
    # group_input.1 -> reroute.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[0],
        onehot_8_1.nodes["Reroute"].inputs[0]
    )
    # group_input.2 -> reroute_001.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[1],
        onehot_8_1.nodes["Reroute.001"].inputs[0]
    )
    # group_input.3 -> reroute_002.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[2],
        onehot_8_1.nodes["Reroute.002"].inputs[0]
    )
    # group_input.4 -> reroute_003.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[3],
        onehot_8_1.nodes["Reroute.003"].inputs[0]
    )
    # group_input.5 -> reroute_004.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[4],
        onehot_8_1.nodes["Reroute.004"].inputs[0]
    )
    # group_input.6 -> reroute_005.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[5],
        onehot_8_1.nodes["Reroute.005"].inputs[0]
    )
    # group_input.7 -> reroute_006.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[6],
        onehot_8_1.nodes["Reroute.006"].inputs[0]
    )
    # group_input.8 -> reroute_007.Input
    onehot_8_1.links.new(
        onehot_8_1.nodes["Group Input"].outputs[7],
        onehot_8_1.nodes["Reroute.007"].inputs[0]
    )
    # math_019.Value -> group_output.2
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.019"].outputs[0],
        onehot_8_1.nodes["Group Output"].inputs[1]
    )
    # math_021.Value -> group_output.3
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.021"].outputs[0],
        onehot_8_1.nodes["Group Output"].inputs[2]
    )
    # math_023.Value -> group_output.4
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.023"].outputs[0],
        onehot_8_1.nodes["Group Output"].inputs[3]
    )
    # math_026.Value -> group_output.5
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.026"].outputs[0],
        onehot_8_1.nodes["Group Output"].inputs[4]
    )
    # math_030.Value -> group_output.6
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.030"].outputs[0],
        onehot_8_1.nodes["Group Output"].inputs[5]
    )
    # math_034.Value -> group_output.7
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.034"].outputs[0],
        onehot_8_1.nodes["Group Output"].inputs[6]
    )
    # math_038.Value -> group_output.8
    onehot_8_1.links.new(
        onehot_8_1.nodes["Math.038"].outputs[0],
        onehot_8_1.nodes["Group Output"].inputs[7]
    )
    # reroute.Output -> math_008.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute"].outputs[0],
        onehot_8_1.nodes["Math.008"].inputs[0]
    )
    # reroute_015.Output -> math_008.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.015"].outputs[0],
        onehot_8_1.nodes["Math.008"].inputs[1]
    )
    # reroute_001.Output -> math_009.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.001"].outputs[0],
        onehot_8_1.nodes["Math.009"].inputs[0]
    )
    # reroute_014.Output -> math_009.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.014"].outputs[0],
        onehot_8_1.nodes["Math.009"].inputs[1]
    )
    # reroute_002.Output -> math_011.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.002"].outputs[0],
        onehot_8_1.nodes["Math.011"].inputs[0]
    )
    # reroute_013.Output -> math_011.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.013"].outputs[0],
        onehot_8_1.nodes["Math.011"].inputs[1]
    )
    # reroute_003.Output -> math_013.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.003"].outputs[0],
        onehot_8_1.nodes["Math.013"].inputs[0]
    )
    # reroute_012.Output -> math_013.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.012"].outputs[0],
        onehot_8_1.nodes["Math.013"].inputs[1]
    )
    # reroute_004.Output -> math_015.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.004"].outputs[0],
        onehot_8_1.nodes["Math.015"].inputs[0]
    )
    # reroute_011.Output -> math_015.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.011"].outputs[0],
        onehot_8_1.nodes["Math.015"].inputs[1]
    )
    # reroute_005.Output -> math_027.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.005"].outputs[0],
        onehot_8_1.nodes["Math.027"].inputs[0]
    )
    # reroute_010.Output -> math_027.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.010"].outputs[0],
        onehot_8_1.nodes["Math.027"].inputs[1]
    )
    # reroute_007.Output -> math_035.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.007"].outputs[0],
        onehot_8_1.nodes["Math.035"].inputs[0]
    )
    # reroute_008.Output -> math_035.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.008"].outputs[0],
        onehot_8_1.nodes["Math.035"].inputs[1]
    )
    # reroute_006.Output -> math_031.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.006"].outputs[0],
        onehot_8_1.nodes["Math.031"].inputs[0]
    )
    # reroute_009.Output -> math_031.Value
    onehot_8_1.links.new(
        onehot_8_1.nodes["Reroute.009"].outputs[0],
        onehot_8_1.nodes["Math.031"].inputs[1]
    )

    return onehot_8_1


def debug_idmask_1_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize debug idmask node group"""
    debug_idmask_1 = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "debug idmask")

    debug_idmask_1.color_tag = 'NONE'
    debug_idmask_1.description = ""
    debug_idmask_1.default_group_node_width = 140
    # debug_idmask_1 interface

    # Socket color
    color_socket = debug_idmask_1.interface.new_socket(name="color", in_out='OUTPUT', socket_type='NodeSocketColor')
    color_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    color_socket.attribute_domain = 'POINT'

    # Socket 1
    _1_socket = debug_idmask_1.interface.new_socket(name="1", in_out='INPUT', socket_type='NodeSocketFloat')
    _1_socket.default_value = 0.5
    _1_socket.min_value = 0.0
    _1_socket.max_value = 1.0
    _1_socket.subtype = 'FACTOR'
    _1_socket.attribute_domain = 'POINT'

    # Socket 2
    _2_socket = debug_idmask_1.interface.new_socket(name="2", in_out='INPUT', socket_type='NodeSocketFloat')
    _2_socket.default_value = 0.5
    _2_socket.min_value = 0.0
    _2_socket.max_value = 1.0
    _2_socket.subtype = 'FACTOR'
    _2_socket.attribute_domain = 'POINT'

    # Socket 3
    _3_socket = debug_idmask_1.interface.new_socket(name="3", in_out='INPUT', socket_type='NodeSocketFloat')
    _3_socket.default_value = 0.5
    _3_socket.min_value = 0.0
    _3_socket.max_value = 1.0
    _3_socket.subtype = 'FACTOR'
    _3_socket.attribute_domain = 'POINT'

    # Socket 4
    _4_socket = debug_idmask_1.interface.new_socket(name="4", in_out='INPUT', socket_type='NodeSocketFloat')
    _4_socket.default_value = 0.5
    _4_socket.min_value = 0.0
    _4_socket.max_value = 1.0
    _4_socket.subtype = 'FACTOR'
    _4_socket.attribute_domain = 'POINT'

    # Socket 5
    _5_socket = debug_idmask_1.interface.new_socket(name="5", in_out='INPUT', socket_type='NodeSocketFloat')
    _5_socket.default_value = 0.5
    _5_socket.min_value = 0.0
    _5_socket.max_value = 1.0
    _5_socket.subtype = 'FACTOR'
    _5_socket.attribute_domain = 'POINT'

    # Socket 6
    _6_socket = debug_idmask_1.interface.new_socket(name="6", in_out='INPUT', socket_type='NodeSocketFloat')
    _6_socket.default_value = 0.5
    _6_socket.min_value = 0.0
    _6_socket.max_value = 1.0
    _6_socket.subtype = 'FACTOR'
    _6_socket.attribute_domain = 'POINT'

    # Socket 7
    _7_socket = debug_idmask_1.interface.new_socket(name="7", in_out='INPUT', socket_type='NodeSocketFloat')
    _7_socket.default_value = 0.5
    _7_socket.min_value = 0.0
    _7_socket.max_value = 1.0
    _7_socket.subtype = 'FACTOR'
    _7_socket.attribute_domain = 'POINT'

    # Socket 8
    _8_socket = debug_idmask_1.interface.new_socket(name="8", in_out='INPUT', socket_type='NodeSocketFloat')
    _8_socket.default_value = 0.5
    _8_socket.min_value = 0.0
    _8_socket.max_value = 1.0
    _8_socket.subtype = 'FACTOR'
    _8_socket.attribute_domain = 'POINT'

    # Socket pattern mask
    pattern_mask_socket = debug_idmask_1.interface.new_socket(name="pattern mask", in_out='INPUT', socket_type='NodeSocketFloat')
    pattern_mask_socket.default_value = 0.0
    pattern_mask_socket.min_value = -3.4028234663852886e+38
    pattern_mask_socket.max_value = 3.4028234663852886e+38
    pattern_mask_socket.subtype = 'NONE'
    pattern_mask_socket.attribute_domain = 'POINT'

    # Initialize debug_idmask_1 nodes

    # Node Group Output
    group_output = debug_idmask_1.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.show_options = True
    group_output.is_active_output = True

    # Node Group Input
    group_input = debug_idmask_1.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.show_options = True

    # Node RGB
    rgb = debug_idmask_1.nodes.new("ShaderNodeRGB")
    rgb.name = "RGB"
    rgb.show_options = True

    rgb.outputs[0].default_value = (1.0, 0.0, 0.0, 1.0)
    # Node RGB.001
    rgb_001 = debug_idmask_1.nodes.new("ShaderNodeRGB")
    rgb_001.name = "RGB.001"
    rgb_001.show_options = True

    rgb_001.outputs[0].default_value = (0.0, 0.0, 1.0, 1.0)
    # Node RGB.002
    rgb_002 = debug_idmask_1.nodes.new("ShaderNodeRGB")
    rgb_002.name = "RGB.002"
    rgb_002.show_options = True

    rgb_002.outputs[0].default_value = (0.0, 1.0, 0.0, 1.0)
    # Node RGB.003
    rgb_003 = debug_idmask_1.nodes.new("ShaderNodeRGB")
    rgb_003.name = "RGB.003"
    rgb_003.show_options = True

    rgb_003.outputs[0].default_value = (0.0, 1.0, 1.0, 1.0)
    # Node RGB.004
    rgb_004 = debug_idmask_1.nodes.new("ShaderNodeRGB")
    rgb_004.name = "RGB.004"
    rgb_004.show_options = True

    rgb_004.outputs[0].default_value = (1.0, 0.0, 1.0, 1.0)
    # Node RGB.005
    rgb_005 = debug_idmask_1.nodes.new("ShaderNodeRGB")
    rgb_005.name = "RGB.005"
    rgb_005.show_options = True

    rgb_005.outputs[0].default_value = (1.0, 1.0, 0.0, 1.0)
    # Node RGB.006
    rgb_006 = debug_idmask_1.nodes.new("ShaderNodeRGB")
    rgb_006.name = "RGB.006"
    rgb_006.show_options = True

    rgb_006.outputs[0].default_value = (1.0, 0.31052160263061523, 0.0, 1.0)
    # Node RGB.007
    rgb_007 = debug_idmask_1.nodes.new("ShaderNodeRGB")
    rgb_007.name = "RGB.007"
    rgb_007.show_options = True

    rgb_007.outputs[0].default_value = (0.34793248772621155, 0.0, 1.0, 1.0)
    # Node Mix
    mix = debug_idmask_1.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.show_options = True
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # A_Color
    mix.inputs[6].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Mix.001
    mix_001 = debug_idmask_1.nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.show_options = True
    mix_001.blend_type = 'MIX'
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    # A_Color
    mix_001.inputs[6].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Mix.002
    mix_002 = debug_idmask_1.nodes.new("ShaderNodeMix")
    mix_002.name = "Mix.002"
    mix_002.show_options = True
    mix_002.blend_type = 'MIX'
    mix_002.clamp_factor = True
    mix_002.clamp_result = False
    mix_002.data_type = 'RGBA'
    mix_002.factor_mode = 'UNIFORM'
    # A_Color
    mix_002.inputs[6].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Mix.003
    mix_003 = debug_idmask_1.nodes.new("ShaderNodeMix")
    mix_003.name = "Mix.003"
    mix_003.show_options = True
    mix_003.blend_type = 'MIX'
    mix_003.clamp_factor = True
    mix_003.clamp_result = False
    mix_003.data_type = 'RGBA'
    mix_003.factor_mode = 'UNIFORM'
    # A_Color
    mix_003.inputs[6].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Mix.004
    mix_004 = debug_idmask_1.nodes.new("ShaderNodeMix")
    mix_004.name = "Mix.004"
    mix_004.show_options = True
    mix_004.blend_type = 'MIX'
    mix_004.clamp_factor = True
    mix_004.clamp_result = False
    mix_004.data_type = 'RGBA'
    mix_004.factor_mode = 'UNIFORM'
    # A_Color
    mix_004.inputs[6].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Mix.005
    mix_005 = debug_idmask_1.nodes.new("ShaderNodeMix")
    mix_005.name = "Mix.005"
    mix_005.show_options = True
    mix_005.blend_type = 'MIX'
    mix_005.clamp_factor = True
    mix_005.clamp_result = False
    mix_005.data_type = 'RGBA'
    mix_005.factor_mode = 'UNIFORM'
    # A_Color
    mix_005.inputs[6].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Mix.006
    mix_006 = debug_idmask_1.nodes.new("ShaderNodeMix")
    mix_006.name = "Mix.006"
    mix_006.show_options = True
    mix_006.blend_type = 'MIX'
    mix_006.clamp_factor = True
    mix_006.clamp_result = False
    mix_006.data_type = 'RGBA'
    mix_006.factor_mode = 'UNIFORM'
    # A_Color
    mix_006.inputs[6].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Mix.007
    mix_007 = debug_idmask_1.nodes.new("ShaderNodeMix")
    mix_007.name = "Mix.007"
    mix_007.show_options = True
    mix_007.blend_type = 'MIX'
    mix_007.clamp_factor = True
    mix_007.clamp_result = False
    mix_007.data_type = 'RGBA'
    mix_007.factor_mode = 'UNIFORM'
    # A_Color
    mix_007.inputs[6].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Vector Math
    vector_math = debug_idmask_1.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.show_options = True
    vector_math.operation = 'ADD'

    # Node Vector Math.001
    vector_math_001 = debug_idmask_1.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.show_options = True
    vector_math_001.operation = 'ADD'

    # Node Vector Math.002
    vector_math_002 = debug_idmask_1.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.show_options = True
    vector_math_002.operation = 'ADD'

    # Node Vector Math.003
    vector_math_003 = debug_idmask_1.nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.show_options = True
    vector_math_003.operation = 'ADD'

    # Node Vector Math.004
    vector_math_004 = debug_idmask_1.nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.show_options = True
    vector_math_004.operation = 'ADD'

    # Node Vector Math.005
    vector_math_005 = debug_idmask_1.nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.show_options = True
    vector_math_005.operation = 'ADD'

    # Node Vector Math.006
    vector_math_006 = debug_idmask_1.nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.show_options = True
    vector_math_006.operation = 'ADD'

    # Node Group.004
    group_004 = debug_idmask_1.nodes.new("ShaderNodeGroup")
    group_004.name = "Group.004"
    group_004.show_options = True
    group_004.node_tree = bpy.data.node_groups[node_tree_names[onehot_8_1_node_group]]

    # Node Vector Math.007
    vector_math_007 = debug_idmask_1.nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.show_options = True
    vector_math_007.operation = 'ADD'

    # Node Reroute
    reroute = debug_idmask_1.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.show_options = True
    reroute.socket_idname = "NodeSocketFloat"
    # Node Reroute.001
    reroute_001 = debug_idmask_1.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.show_options = True
    reroute_001.socket_idname = "NodeSocketFloat"
    # Node Math
    math = debug_idmask_1.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.show_options = True
    math.operation = 'GREATER_THAN'
    math.use_clamp = True
    # Value_001
    math.inputs[1].default_value = 0.2

    # Node Separate XYZ
    separate_xyz = debug_idmask_1.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"
    separate_xyz.hide = True
    separate_xyz.show_options = True

    # Node Clamp
    clamp = debug_idmask_1.nodes.new("ShaderNodeClamp")
    clamp.name = "Clamp"
    clamp.hide = True
    clamp.show_options = True
    clamp.clamp_type = 'MINMAX'
    # Min
    clamp.inputs[1].default_value = 0.0
    # Max
    clamp.inputs[2].default_value = 1.0

    # Node Clamp.001
    clamp_001 = debug_idmask_1.nodes.new("ShaderNodeClamp")
    clamp_001.name = "Clamp.001"
    clamp_001.hide = True
    clamp_001.show_options = True
    clamp_001.clamp_type = 'MINMAX'
    # Min
    clamp_001.inputs[1].default_value = 0.0
    # Max
    clamp_001.inputs[2].default_value = 1.0

    # Node Clamp.002
    clamp_002 = debug_idmask_1.nodes.new("ShaderNodeClamp")
    clamp_002.name = "Clamp.002"
    clamp_002.hide = True
    clamp_002.show_options = True
    clamp_002.clamp_type = 'MINMAX'
    # Min
    clamp_002.inputs[1].default_value = 0.0
    # Max
    clamp_002.inputs[2].default_value = 1.0

    # Node Combine Color
    combine_color = debug_idmask_1.nodes.new("ShaderNodeCombineColor")
    combine_color.name = "Combine Color"
    combine_color.hide = True
    combine_color.show_options = True
    combine_color.mode = 'RGB'

    # Set locations
    debug_idmask_1.nodes["Group Output"].location = (2337.170166015625, -325.7985534667969)
    debug_idmask_1.nodes["Group Input"].location = (-1912.41845703125, -746.9465942382812)
    debug_idmask_1.nodes["RGB"].location = (-1684.8863525390625, 402.74151611328125)
    debug_idmask_1.nodes["RGB.001"].location = (-1685.8580322265625, 205.024658203125)
    debug_idmask_1.nodes["RGB.002"].location = (-1687.0228271484375, 0.98760986328125)
    debug_idmask_1.nodes["RGB.003"].location = (-1687.748779296875, -202.84844970703125)
    debug_idmask_1.nodes["RGB.004"].location = (-1691.197021484375, -1047.197021484375)
    debug_idmask_1.nodes["RGB.005"].location = (-1689.33740234375, -1259.3873291015625)
    debug_idmask_1.nodes["RGB.006"].location = (-1687.405517578125, -1468.687744140625)
    debug_idmask_1.nodes["RGB.007"].location = (-1685.5458984375, -1686.4620361328125)
    debug_idmask_1.nodes["Mix"].location = (230.5174560546875, 356.6974792480469)
    debug_idmask_1.nodes["Mix.001"].location = (232.400146484375, 131.09043884277344)
    debug_idmask_1.nodes["Mix.002"].location = (232.93540954589844, -103.75950622558594)
    debug_idmask_1.nodes["Mix.003"].location = (232.7082061767578, -342.2400207519531)
    debug_idmask_1.nodes["Mix.004"].location = (227.7820587158203, -567.8470458984375)
    debug_idmask_1.nodes["Mix.005"].location = (228.3173370361328, -802.697021484375)
    debug_idmask_1.nodes["Mix.006"].location = (227.65951538085938, -1042.0498046875)
    debug_idmask_1.nodes["Mix.007"].location = (222.73336791992188, -1267.6568603515625)
    debug_idmask_1.nodes["Vector Math"].location = (715.1749267578125, 267.9676513671875)
    debug_idmask_1.nodes["Vector Math.001"].location = (724.5809326171875, -141.25494384765625)
    debug_idmask_1.nodes["Vector Math.002"].location = (740.9089965820312, -436.42279052734375)
    debug_idmask_1.nodes["Vector Math.003"].location = (730.8616333007812, -872.6712646484375)
    debug_idmask_1.nodes["Vector Math.004"].location = (1030.158203125, 100.21028137207031)
    debug_idmask_1.nodes["Vector Math.005"].location = (1014.1272583007812, -577.3648681640625)
    debug_idmask_1.nodes["Vector Math.006"].location = (1265.3941650390625, -215.3646697998047)
    debug_idmask_1.nodes["Group.004"].location = (-1665.5142822265625, -535.1954956054688)
    debug_idmask_1.nodes["Vector Math.007"].location = (1571.558837890625, -335.2659606933594)
    debug_idmask_1.nodes["Reroute"].location = (268.774658203125, -1793.53955078125)
    debug_idmask_1.nodes["Reroute.001"].location = (1205.5809326171875, -1130.2900390625)
    debug_idmask_1.nodes["Math"].location = (1322.699951171875, -763.5423583984375)
    debug_idmask_1.nodes["Separate XYZ"].location = (1732.2579345703125, -360.2530212402344)
    debug_idmask_1.nodes["Clamp"].location = (1936.8973388671875, -311.0566711425781)
    debug_idmask_1.nodes["Clamp.001"].location = (1932.5565185546875, -351.4910583496094)
    debug_idmask_1.nodes["Clamp.002"].location = (1932.5565185546875, -393.26043701171875)
    debug_idmask_1.nodes["Combine Color"].location = (2120.27197265625, -351.560302734375)

    # Set dimensions
    debug_idmask_1.nodes["Group Output"].width  = 140.0
    debug_idmask_1.nodes["Group Output"].height = 100.0

    debug_idmask_1.nodes["Group Input"].width  = 140.0
    debug_idmask_1.nodes["Group Input"].height = 100.0

    debug_idmask_1.nodes["RGB"].width  = 140.0
    debug_idmask_1.nodes["RGB"].height = 100.0

    debug_idmask_1.nodes["RGB.001"].width  = 140.0
    debug_idmask_1.nodes["RGB.001"].height = 100.0

    debug_idmask_1.nodes["RGB.002"].width  = 140.0
    debug_idmask_1.nodes["RGB.002"].height = 100.0

    debug_idmask_1.nodes["RGB.003"].width  = 140.0
    debug_idmask_1.nodes["RGB.003"].height = 100.0

    debug_idmask_1.nodes["RGB.004"].width  = 140.0
    debug_idmask_1.nodes["RGB.004"].height = 100.0

    debug_idmask_1.nodes["RGB.005"].width  = 140.0
    debug_idmask_1.nodes["RGB.005"].height = 100.0

    debug_idmask_1.nodes["RGB.006"].width  = 140.0
    debug_idmask_1.nodes["RGB.006"].height = 100.0

    debug_idmask_1.nodes["RGB.007"].width  = 140.0
    debug_idmask_1.nodes["RGB.007"].height = 100.0

    debug_idmask_1.nodes["Mix"].width  = 140.0
    debug_idmask_1.nodes["Mix"].height = 100.0

    debug_idmask_1.nodes["Mix.001"].width  = 140.0
    debug_idmask_1.nodes["Mix.001"].height = 100.0

    debug_idmask_1.nodes["Mix.002"].width  = 140.0
    debug_idmask_1.nodes["Mix.002"].height = 100.0

    debug_idmask_1.nodes["Mix.003"].width  = 140.0
    debug_idmask_1.nodes["Mix.003"].height = 100.0

    debug_idmask_1.nodes["Mix.004"].width  = 140.0
    debug_idmask_1.nodes["Mix.004"].height = 100.0

    debug_idmask_1.nodes["Mix.005"].width  = 140.0
    debug_idmask_1.nodes["Mix.005"].height = 100.0

    debug_idmask_1.nodes["Mix.006"].width  = 140.0
    debug_idmask_1.nodes["Mix.006"].height = 100.0

    debug_idmask_1.nodes["Mix.007"].width  = 140.0
    debug_idmask_1.nodes["Mix.007"].height = 100.0

    debug_idmask_1.nodes["Vector Math"].width  = 140.0
    debug_idmask_1.nodes["Vector Math"].height = 100.0

    debug_idmask_1.nodes["Vector Math.001"].width  = 140.0
    debug_idmask_1.nodes["Vector Math.001"].height = 100.0

    debug_idmask_1.nodes["Vector Math.002"].width  = 140.0
    debug_idmask_1.nodes["Vector Math.002"].height = 100.0

    debug_idmask_1.nodes["Vector Math.003"].width  = 140.0
    debug_idmask_1.nodes["Vector Math.003"].height = 100.0

    debug_idmask_1.nodes["Vector Math.004"].width  = 140.0
    debug_idmask_1.nodes["Vector Math.004"].height = 100.0

    debug_idmask_1.nodes["Vector Math.005"].width  = 140.0
    debug_idmask_1.nodes["Vector Math.005"].height = 100.0

    debug_idmask_1.nodes["Vector Math.006"].width  = 140.0
    debug_idmask_1.nodes["Vector Math.006"].height = 100.0

    debug_idmask_1.nodes["Group.004"].width  = 140.0
    debug_idmask_1.nodes["Group.004"].height = 100.0

    debug_idmask_1.nodes["Vector Math.007"].width  = 140.0
    debug_idmask_1.nodes["Vector Math.007"].height = 100.0

    debug_idmask_1.nodes["Reroute"].width  = 16.0
    debug_idmask_1.nodes["Reroute"].height = 100.0

    debug_idmask_1.nodes["Reroute.001"].width  = 16.0
    debug_idmask_1.nodes["Reroute.001"].height = 100.0

    debug_idmask_1.nodes["Math"].width  = 140.0
    debug_idmask_1.nodes["Math"].height = 100.0

    debug_idmask_1.nodes["Separate XYZ"].width  = 140.0
    debug_idmask_1.nodes["Separate XYZ"].height = 100.0

    debug_idmask_1.nodes["Clamp"].width  = 140.0
    debug_idmask_1.nodes["Clamp"].height = 100.0

    debug_idmask_1.nodes["Clamp.001"].width  = 140.0
    debug_idmask_1.nodes["Clamp.001"].height = 100.0

    debug_idmask_1.nodes["Clamp.002"].width  = 140.0
    debug_idmask_1.nodes["Clamp.002"].height = 100.0

    debug_idmask_1.nodes["Combine Color"].width  = 140.0
    debug_idmask_1.nodes["Combine Color"].height = 100.0


    # Initialize debug_idmask_1 links

    # group_004.5 -> mix_004.Factor
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group.004"].outputs[4],
        debug_idmask_1.nodes["Mix.004"].inputs[0]
    )
    # group_004.7 -> mix_006.Factor
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group.004"].outputs[6],
        debug_idmask_1.nodes["Mix.006"].inputs[0]
    )
    # rgb.Color -> mix.B
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["RGB"].outputs[0],
        debug_idmask_1.nodes["Mix"].inputs[7]
    )
    # rgb_001.Color -> mix_001.B
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["RGB.001"].outputs[0],
        debug_idmask_1.nodes["Mix.001"].inputs[7]
    )
    # rgb_002.Color -> mix_002.B
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["RGB.002"].outputs[0],
        debug_idmask_1.nodes["Mix.002"].inputs[7]
    )
    # rgb_003.Color -> mix_003.B
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["RGB.003"].outputs[0],
        debug_idmask_1.nodes["Mix.003"].inputs[7]
    )
    # rgb_004.Color -> mix_004.B
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["RGB.004"].outputs[0],
        debug_idmask_1.nodes["Mix.004"].inputs[7]
    )
    # rgb_005.Color -> mix_005.B
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["RGB.005"].outputs[0],
        debug_idmask_1.nodes["Mix.005"].inputs[7]
    )
    # rgb_006.Color -> mix_006.B
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["RGB.006"].outputs[0],
        debug_idmask_1.nodes["Mix.006"].inputs[7]
    )
    # rgb_007.Color -> mix_007.B
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["RGB.007"].outputs[0],
        debug_idmask_1.nodes["Mix.007"].inputs[7]
    )
    # mix.Result -> vector_math.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Mix"].outputs[2],
        debug_idmask_1.nodes["Vector Math"].inputs[0]
    )
    # mix_001.Result -> vector_math.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Mix.001"].outputs[2],
        debug_idmask_1.nodes["Vector Math"].inputs[1]
    )
    # mix_002.Result -> vector_math_001.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Mix.002"].outputs[2],
        debug_idmask_1.nodes["Vector Math.001"].inputs[0]
    )
    # mix_003.Result -> vector_math_001.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Mix.003"].outputs[2],
        debug_idmask_1.nodes["Vector Math.001"].inputs[1]
    )
    # mix_004.Result -> vector_math_002.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Mix.004"].outputs[2],
        debug_idmask_1.nodes["Vector Math.002"].inputs[0]
    )
    # mix_005.Result -> vector_math_002.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Mix.005"].outputs[2],
        debug_idmask_1.nodes["Vector Math.002"].inputs[1]
    )
    # mix_007.Result -> vector_math_003.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Mix.007"].outputs[2],
        debug_idmask_1.nodes["Vector Math.003"].inputs[1]
    )
    # mix_006.Result -> vector_math_003.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Mix.006"].outputs[2],
        debug_idmask_1.nodes["Vector Math.003"].inputs[0]
    )
    # vector_math.Vector -> vector_math_004.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Vector Math"].outputs[0],
        debug_idmask_1.nodes["Vector Math.004"].inputs[0]
    )
    # vector_math_001.Vector -> vector_math_004.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Vector Math.001"].outputs[0],
        debug_idmask_1.nodes["Vector Math.004"].inputs[1]
    )
    # vector_math_003.Vector -> vector_math_005.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Vector Math.003"].outputs[0],
        debug_idmask_1.nodes["Vector Math.005"].inputs[1]
    )
    # vector_math_002.Vector -> vector_math_005.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Vector Math.002"].outputs[0],
        debug_idmask_1.nodes["Vector Math.005"].inputs[0]
    )
    # vector_math_004.Vector -> vector_math_006.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Vector Math.004"].outputs[0],
        debug_idmask_1.nodes["Vector Math.006"].inputs[0]
    )
    # vector_math_005.Vector -> vector_math_006.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Vector Math.005"].outputs[0],
        debug_idmask_1.nodes["Vector Math.006"].inputs[1]
    )
    # group_004.6 -> mix_005.Factor
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group.004"].outputs[5],
        debug_idmask_1.nodes["Mix.005"].inputs[0]
    )
    # group_004.8 -> mix_007.Factor
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group.004"].outputs[7],
        debug_idmask_1.nodes["Mix.007"].inputs[0]
    )
    # group_input.6 -> group_004.6
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group Input"].outputs[5],
        debug_idmask_1.nodes["Group.004"].inputs[5]
    )
    # group_input.8 -> group_004.8
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group Input"].outputs[7],
        debug_idmask_1.nodes["Group.004"].inputs[7]
    )
    # group_input.7 -> group_004.7
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group Input"].outputs[6],
        debug_idmask_1.nodes["Group.004"].inputs[6]
    )
    # group_input.1 -> group_004.1
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group Input"].outputs[0],
        debug_idmask_1.nodes["Group.004"].inputs[0]
    )
    # group_input.2 -> group_004.2
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group Input"].outputs[1],
        debug_idmask_1.nodes["Group.004"].inputs[1]
    )
    # group_input.3 -> group_004.3
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group Input"].outputs[2],
        debug_idmask_1.nodes["Group.004"].inputs[2]
    )
    # group_input.4 -> group_004.4
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group Input"].outputs[3],
        debug_idmask_1.nodes["Group.004"].inputs[3]
    )
    # group_input.5 -> group_004.5
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group Input"].outputs[4],
        debug_idmask_1.nodes["Group.004"].inputs[4]
    )
    # group_004.1 -> mix.Factor
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group.004"].outputs[0],
        debug_idmask_1.nodes["Mix"].inputs[0]
    )
    # group_004.2 -> mix_001.Factor
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group.004"].outputs[1],
        debug_idmask_1.nodes["Mix.001"].inputs[0]
    )
    # group_004.3 -> mix_002.Factor
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group.004"].outputs[2],
        debug_idmask_1.nodes["Mix.002"].inputs[0]
    )
    # group_004.4 -> mix_003.Factor
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group.004"].outputs[3],
        debug_idmask_1.nodes["Mix.003"].inputs[0]
    )
    # vector_math_006.Vector -> vector_math_007.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Vector Math.006"].outputs[0],
        debug_idmask_1.nodes["Vector Math.007"].inputs[0]
    )
    # group_input.pattern mask -> reroute.Input
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Group Input"].outputs[8],
        debug_idmask_1.nodes["Reroute"].inputs[0]
    )
    # reroute.Output -> reroute_001.Input
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Reroute"].outputs[0],
        debug_idmask_1.nodes["Reroute.001"].inputs[0]
    )
    # reroute_001.Output -> math.Value
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Reroute.001"].outputs[0],
        debug_idmask_1.nodes["Math"].inputs[0]
    )
    # math.Value -> vector_math_007.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Math"].outputs[0],
        debug_idmask_1.nodes["Vector Math.007"].inputs[1]
    )
    # vector_math_007.Vector -> separate_xyz.Vector
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Vector Math.007"].outputs[0],
        debug_idmask_1.nodes["Separate XYZ"].inputs[0]
    )
    # separate_xyz.X -> clamp.Value
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Separate XYZ"].outputs[0],
        debug_idmask_1.nodes["Clamp"].inputs[0]
    )
    # separate_xyz.Y -> clamp_001.Value
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Separate XYZ"].outputs[1],
        debug_idmask_1.nodes["Clamp.001"].inputs[0]
    )
    # separate_xyz.Z -> clamp_002.Value
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Separate XYZ"].outputs[2],
        debug_idmask_1.nodes["Clamp.002"].inputs[0]
    )
    # clamp.Result -> combine_color.Red
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Clamp"].outputs[0],
        debug_idmask_1.nodes["Combine Color"].inputs[0]
    )
    # clamp_001.Result -> combine_color.Green
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Clamp.001"].outputs[0],
        debug_idmask_1.nodes["Combine Color"].inputs[1]
    )
    # clamp_002.Result -> combine_color.Blue
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Clamp.002"].outputs[0],
        debug_idmask_1.nodes["Combine Color"].inputs[2]
    )
    # combine_color.Color -> group_output.color
    debug_idmask_1.links.new(
        debug_idmask_1.nodes["Combine Color"].outputs[0],
        debug_idmask_1.nodes["Group Output"].inputs[0]
    )

    return debug_idmask_1


def shader_nodetree_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    idmask_debug_material = bpy.data.materials.new(name = "IDMask Debug Material")
    if bpy.app.version < (5, 0, 0):
        idmask_debug_material.use_nodes = True
    shader_nodetree = idmask_debug_material.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.show_options = True
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 0.5
    # IOR
    principled_bsdf.inputs[3].default_value = 1.5
    # Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.show_options = True
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Group
    group = shader_nodetree.nodes.new("ShaderNodeGroup")
    group.name = "Group"
    group.show_options = True
    group.node_tree = bpy.data.node_groups[node_tree_names[debug_idmask_1_node_group]]

    # Node Image Texture
    image_texture = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.show_options = True
    image_texture.extension = 'REPEAT'
    image_texture.image_user.frame_current = 0
    image_texture.image_user.frame_duration = 100
    image_texture.image_user.frame_offset = 0
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Linear'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0
    # Vector
    image_texture.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Image Texture.001
    image_texture_001 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_001.name = "Image Texture.001"
    image_texture_001.show_options = True
    image_texture_001.extension = 'REPEAT'
    image_texture_001.image_user.frame_current = 0
    image_texture_001.image_user.frame_duration = 100
    image_texture_001.image_user.frame_offset = 0
    image_texture_001.image_user.frame_start = 1
    image_texture_001.image_user.tile = 0
    image_texture_001.image_user.use_auto_refresh = False
    image_texture_001.image_user.use_cyclic = False
    image_texture_001.interpolation = 'Linear'
    image_texture_001.projection = 'FLAT'
    image_texture_001.projection_blend = 0.0
    # Vector
    image_texture_001.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Image Texture.002
    image_texture_002 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_002.name = "Image Texture.002"
    image_texture_002.show_options = True
    image_texture_002.extension = 'REPEAT'
    image_texture_002.image_user.frame_current = 0
    image_texture_002.image_user.frame_duration = 100
    image_texture_002.image_user.frame_offset = 0
    image_texture_002.image_user.frame_start = 1
    image_texture_002.image_user.tile = 0
    image_texture_002.image_user.use_auto_refresh = False
    image_texture_002.image_user.use_cyclic = False
    image_texture_002.interpolation = 'Linear'
    image_texture_002.projection = 'FLAT'
    image_texture_002.projection_blend = 0.0
    # Vector
    image_texture_002.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Image Texture.003
    image_texture_003 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_003.name = "Image Texture.003"
    image_texture_003.show_options = True
    image_texture_003.extension = 'REPEAT'
    image_texture_003.image_user.frame_current = 0
    image_texture_003.image_user.frame_duration = 100
    image_texture_003.image_user.frame_offset = 0
    image_texture_003.image_user.frame_start = 1
    image_texture_003.image_user.tile = 0
    image_texture_003.image_user.use_auto_refresh = False
    image_texture_003.image_user.use_cyclic = False
    image_texture_003.interpolation = 'Linear'
    image_texture_003.projection = 'FLAT'
    image_texture_003.projection_blend = 0.0
    # Vector
    image_texture_003.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Image Texture.004
    image_texture_004 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_004.name = "Image Texture.004"
    image_texture_004.show_options = True
    image_texture_004.extension = 'REPEAT'
    image_texture_004.image_user.frame_current = 0
    image_texture_004.image_user.frame_duration = 100
    image_texture_004.image_user.frame_offset = 0
    image_texture_004.image_user.frame_start = 1
    image_texture_004.image_user.tile = 0
    image_texture_004.image_user.use_auto_refresh = False
    image_texture_004.image_user.use_cyclic = False
    image_texture_004.interpolation = 'Linear'
    image_texture_004.projection = 'FLAT'
    image_texture_004.projection_blend = 0.0
    # Vector
    image_texture_004.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Image Texture.005
    image_texture_005 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_005.name = "Image Texture.005"
    image_texture_005.show_options = True
    image_texture_005.extension = 'REPEAT'
    image_texture_005.image_user.frame_current = 0
    image_texture_005.image_user.frame_duration = 100
    image_texture_005.image_user.frame_offset = 0
    image_texture_005.image_user.frame_start = 1
    image_texture_005.image_user.tile = 0
    image_texture_005.image_user.use_auto_refresh = False
    image_texture_005.image_user.use_cyclic = False
    image_texture_005.interpolation = 'Linear'
    image_texture_005.projection = 'FLAT'
    image_texture_005.projection_blend = 0.0
    # Vector
    image_texture_005.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Image Texture.006
    image_texture_006 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_006.name = "Image Texture.006"
    image_texture_006.show_options = True
    image_texture_006.extension = 'REPEAT'
    image_texture_006.image_user.frame_current = 0
    image_texture_006.image_user.frame_duration = 100
    image_texture_006.image_user.frame_offset = 0
    image_texture_006.image_user.frame_start = 1
    image_texture_006.image_user.tile = 0
    image_texture_006.image_user.use_auto_refresh = False
    image_texture_006.image_user.use_cyclic = False
    image_texture_006.interpolation = 'Linear'
    image_texture_006.projection = 'FLAT'
    image_texture_006.projection_blend = 0.0
    # Vector
    image_texture_006.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Image Texture.007
    image_texture_007 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_007.name = "Image Texture.007"
    image_texture_007.show_options = True
    image_texture_007.extension = 'REPEAT'
    image_texture_007.image_user.frame_current = 0
    image_texture_007.image_user.frame_duration = 100
    image_texture_007.image_user.frame_offset = 0
    image_texture_007.image_user.frame_start = 1
    image_texture_007.image_user.tile = 0
    image_texture_007.image_user.use_auto_refresh = False
    image_texture_007.image_user.use_cyclic = False
    image_texture_007.interpolation = 'Linear'
    image_texture_007.projection = 'FLAT'
    image_texture_007.projection_blend = 0.0
    # Vector
    image_texture_007.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Node Image Texture.008
    image_texture_008 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_008.name = "Image Texture.008"
    image_texture_008.show_options = True
    image_texture_008.show_texture = True
    image_texture_008.extension = 'REPEAT'
    image_texture_008.image_user.frame_current = 0
    image_texture_008.image_user.frame_duration = 100
    image_texture_008.image_user.frame_offset = 0
    image_texture_008.image_user.frame_start = 1
    image_texture_008.image_user.tile = 0
    image_texture_008.image_user.use_auto_refresh = False
    image_texture_008.image_user.use_cyclic = False
    image_texture_008.interpolation = 'Linear'
    image_texture_008.projection = 'FLAT'
    image_texture_008.projection_blend = 0.0
    # Vector
    image_texture_008.inputs[0].default_value = (0.0, 0.0, 0.0)

    # Set locations
    shader_nodetree.nodes["Principled BSDF"].location = (10.0, 300.0)
    shader_nodetree.nodes["Material Output"].location = (319.84674072265625, 325.7060241699219)
    shader_nodetree.nodes["Group"].location = (-212.97793579101562, 278.209228515625)
    shader_nodetree.nodes["Image Texture"].location = (-748.80908203125, 688.9165649414062)
    shader_nodetree.nodes["Image Texture.001"].location = (-752.9381103515625, 483.716064453125)
    shader_nodetree.nodes["Image Texture.002"].location = (-750.770263671875, 268.232666015625)
    shader_nodetree.nodes["Image Texture.003"].location = (-754.8992919921875, 63.03216552734375)
    shader_nodetree.nodes["Image Texture.004"].location = (-754.7113037109375, -151.6060333251953)
    shader_nodetree.nodes["Image Texture.005"].location = (-758.84033203125, -356.8065185546875)
    shader_nodetree.nodes["Image Texture.006"].location = (-756.6724853515625, -572.2899169921875)
    shader_nodetree.nodes["Image Texture.007"].location = (-760.801513671875, -777.4904174804688)
    shader_nodetree.nodes["Image Texture.008"].location = (-761.4735717773438, -1014.4353637695312)

    # Set dimensions
    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Group"].width  = 140.0
    shader_nodetree.nodes["Group"].height = 100.0

    shader_nodetree.nodes["Image Texture"].width  = 240.0
    shader_nodetree.nodes["Image Texture"].height = 100.0

    shader_nodetree.nodes["Image Texture.001"].width  = 240.0
    shader_nodetree.nodes["Image Texture.001"].height = 100.0

    shader_nodetree.nodes["Image Texture.002"].width  = 240.0
    shader_nodetree.nodes["Image Texture.002"].height = 100.0

    shader_nodetree.nodes["Image Texture.003"].width  = 240.0
    shader_nodetree.nodes["Image Texture.003"].height = 100.0

    shader_nodetree.nodes["Image Texture.004"].width  = 240.0
    shader_nodetree.nodes["Image Texture.004"].height = 100.0

    shader_nodetree.nodes["Image Texture.005"].width  = 240.0
    shader_nodetree.nodes["Image Texture.005"].height = 100.0

    shader_nodetree.nodes["Image Texture.006"].width  = 240.0
    shader_nodetree.nodes["Image Texture.006"].height = 100.0

    shader_nodetree.nodes["Image Texture.007"].width  = 240.0
    shader_nodetree.nodes["Image Texture.007"].height = 100.0

    shader_nodetree.nodes["Image Texture.008"].width  = 240.0
    shader_nodetree.nodes["Image Texture.008"].height = 100.0


    # Initialize shader_nodetree links

    # principled_bsdf.BSDF -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # group.color -> principled_bsdf.Base Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Group"].outputs[0],
        shader_nodetree.nodes["Principled BSDF"].inputs[0]
    )
    # image_texture.Color -> group.1
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture"].outputs[0],
        shader_nodetree.nodes["Group"].inputs[0]
    )
    # image_texture_001.Color -> group.2
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.001"].outputs[0],
        shader_nodetree.nodes["Group"].inputs[1]
    )
    # image_texture_002.Color -> group.3
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.002"].outputs[0],
        shader_nodetree.nodes["Group"].inputs[2]
    )
    # image_texture_003.Color -> group.4
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.003"].outputs[0],
        shader_nodetree.nodes["Group"].inputs[3]
    )
    # image_texture_004.Color -> group.5
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.004"].outputs[0],
        shader_nodetree.nodes["Group"].inputs[4]
    )
    # image_texture_005.Color -> group.6
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.005"].outputs[0],
        shader_nodetree.nodes["Group"].inputs[5]
    )
    # image_texture_006.Color -> group.7
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.006"].outputs[0],
        shader_nodetree.nodes["Group"].inputs[6]
    )
    # image_texture_007.Color -> group.8
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.007"].outputs[0],
        shader_nodetree.nodes["Group"].inputs[7]
    )
    # image_texture_008.Color -> group.pattern mask
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.008"].outputs[0],
        shader_nodetree.nodes["Group"].inputs[8]
    )

    return idmask_debug_material


if __name__ == "__main__":
    # Maps node tree creation functions to the node tree 
    # name, such that we don't recreate node trees unnecessarily
    node_tree_names : dict[typing.Callable, str] = {}

    onehot_8 = onehot_8_1_node_group(node_tree_names)
    node_tree_names[onehot_8_1_node_group] = onehot_8.name

    debug_idmask = debug_idmask_1_node_group(node_tree_names)
    node_tree_names[debug_idmask_1_node_group] = debug_idmask.name

    shader_nodetree = shader_nodetree_node_group(node_tree_names)
    node_tree_names[shader_nodetree_node_group] = shader_nodetree.name


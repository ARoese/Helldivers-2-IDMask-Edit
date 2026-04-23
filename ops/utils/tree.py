import bpy
from typing import List, Tuple

def trace_to_textures(input: bpy.types.NodeSocket) -> List[bpy.types.ShaderNodeTexImage]:
    '''Recursively search the input node tree for all Texture shader nodes. Texture nodes are returned in-order.'''
    if input.links is None or len(input.links) == 0:
        return []
    
    source_node = input.links[0].from_node
    #print("source node:", source_node)

    if isinstance(source_node, bpy.types.ShaderNodeTexImage):
        return [source_node]
    
    if source_node is None or source_node.inputs is None:
        #print("inputs dead end")
        return []
    
    found_recurse = []
    for input in source_node.inputs:
        #print("recursing on input:", input)
        found_recurse.extend(trace_to_textures(input))
    
    return found_recurse

def tree_bounding_box(tree: bpy.types.ShaderNodeTree) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    '''computes and returns the bounding box of the given shader tree in top-left bottom-right form'''
    lx,hy = 0,0
    hx,ly = 0,0

    if len(tree.nodes) == 0:
        return (lx, hy), (hx, ly)
    
    lx,hy = tree.nodes[0].location.xy
    hx,ly = tree.nodes[0].location.xy

    for node in tree.nodes:
        x,y = node.location.xy

        lx = min(lx,x)
        hx = max(hx, x)

        ly = min(ly, y)
        hy = max(hy, y)
    
    return (lx, hy), (hx, ly)
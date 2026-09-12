import ast

# We don't have bpy access here, so we can't import the __init__ module to get the bl_info
# We can, however, crawl the file using ast and extract it that way. This is what blender does.

# Parse the source code into an AST
source = open("__init__.py", 'r').read()
#print("Source code:", source)
tree = ast.parse(source)

# Walk the ast for the __init__ file to extract bl_info, the same way blender does
bl_info = None
for node in ast.walk(tree):
  # find an assignment
  if isinstance(node, ast.Assign):
    for target in node.targets:
      # find target name 'bl_info'
      if isinstance(target, ast.Name) and target.id == 'bl_info':
        # eval what is being assigned to it. This is the bl_info dict
        bl_info = ast.literal_eval(node.value)

def get_version_string() -> str:
    if bl_info is not None:
        return ".".join(str(c) for c in bl_info["version"])
    else:
       return "unknown.unknown.unknown"

if __name__ == "__main__":
    print(get_version_string())
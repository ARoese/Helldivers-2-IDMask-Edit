bl_info = {
    "name": "HD2 LUT Visual Edit",
    "blender": (4, 3, 0),
    "version": (1, 3, 1),
    "category": "Material",
}

def get_version_string() -> str:
    return ".".join(str(c) for c in bl_info["version"])

if __name__ == "__main__":
    print(get_version_string())
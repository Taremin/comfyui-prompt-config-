import importlib
import os

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}


def get_files():
    dir = os.path.dirname(__file__)
    files = []
    for f in os.listdir(dir):
        path = os.path.join(dir, f)
        if os.path.isfile(path):
            files.append(path)
    return files


for path in get_files():
    filename = os.path.basename(path)
    if filename == "__init__.py":
        continue

    base, ext = os.path.splitext(filename)
    if ext != ".py":
        continue

    imported_module = importlib.import_module(".{}".format(base), __name__)

    if hasattr(imported_module, "NODE_CLASS_MAPPINGS") and hasattr(
        imported_module, "NODE_DISPLAY_NAME_MAPPINGS"
    ):
        NODE_CLASS_MAPPINGS = {
            **NODE_CLASS_MAPPINGS,
            **imported_module.NODE_CLASS_MAPPINGS,
        }
        NODE_DISPLAY_NAME_MAPPINGS = {
            **NODE_DISPLAY_NAME_MAPPINGS,
            **imported_module.NODE_DISPLAY_NAME_MAPPINGS,
        }
    else:
        raise ImportError(
            f"NODE_CLASS_MAPPINGS or NODE_DISPLAY_NAME_MAPPINGS not found in module: {path}"
        )

from importlib import import_module


def import_from_string(object_path):
    if not object_path:
        return
    module_path, object_name = object_path.rsplit(".", 1)
    module = import_module(module_path)
    obj = getattr(module, object_name)
    return obj

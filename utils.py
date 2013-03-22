import importlib


def load_from_string(full_string):
    """dynamically load a class or a function from a string"""
    class_data = full_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    return getattr(module, class_str)

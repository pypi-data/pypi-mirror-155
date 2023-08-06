from typing import Dict


def get_class_attributes(the_class) -> Dict:
    class_attributes = {}
    for name in vars(the_class):
        if name.startswith("__"):
            continue
        attr = getattr(the_class, name)
        if callable(attr):
            continue
        class_attributes[name] = attr
    return class_attributes

import importlib
from typing import Any


class Generator:
    def load_class(self, path: str) -> Any:
        """
        Load class type from string

        :param path: class path name
        :return: class type
        """
        modules = path.split('.')
        class_name = modules[-1]
        module_name = '.'.join(modules[:-1])

        module = importlib.import_module(module_name)

        return getattr(module, class_name)

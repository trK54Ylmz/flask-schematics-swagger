import importlib
from typing import Any, TypeVar
from fss.schema.rule import DocRuleSchema


T = TypeVar('T', bound=DocRuleSchema)


class RuleParser:
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

    def parse(self, definition: str) -> T:
        """
        Parse parameter or response definition in function pydoc

        :param definition: raw function pydoc line
        :return: parameter or response definition schema
        """
        raise NotImplementedError

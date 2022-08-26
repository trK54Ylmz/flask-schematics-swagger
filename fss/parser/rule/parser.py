from typing import Any, TypeVar

from schematics import Model
from fss.schema import Schema


T = TypeVar('T', bound=Model)


class RuleParser:
    def cast_default(self, value: str, type: str) -> Any:
        """
        Cast default type by given type definition

        :param value: default value as string
        :param type: expected default value type
        :return: new default value in given type
        """
        if type == Schema.FLOAT:
            return float(value)

        if type == Schema.INTEGER:
            return int(value)

        if type == Schema.BOOLEAN:
            return value in ['true', 'True', '1']

        return value

    def parse(self, definition: str) -> T:
        """
        Parse parameter or response definition in function pydoc

        :param definition: raw function pydoc line
        :return: parameter or response definition schema
        """
        raise NotImplementedError

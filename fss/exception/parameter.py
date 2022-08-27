from typing import Optional
from .rule import RuleException


class ParameterException(RuleException):
    parameter: Optional[str] = None

    def __init__(self, definition: str, parameter: Optional[str] = None, *args: object) -> None:
        self.parameter = parameter

        super().__init__(definition, *args)

    def __str__(self) -> str:
        msg = f'Invalid parameter definition "{self.definition}".'

        if self.parameter is not None:
            msg += f' Parameter type is "{self.parameter}"'

        return msg

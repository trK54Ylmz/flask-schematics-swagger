from typing import Optional, TypeVar

from fss.exception.rule import RuleException
from fss.parser.rule.parameter import DocParameterRuleParser
from .response import DocResponseRuleParser
from fss.schema.rule import DocRuleSchema

T = TypeVar('T', bound=DocRuleSchema)


class DocRuleParser:
    def __init__(self) -> None:
        """
        Parses endpoint definition
        """
        self.invalid_definitions = [':param ', ':return:', ':rtype:']

    def parse(self, definition: str) -> Optional[T]:
        """
        Parse parameter or response definition in function pydoc

        :param definition: raw function pydoc line
        :return: parameter or response definition schema
        """
        for invalid in self.invalid_definitions:
            if definition.startswith(invalid):
                return None

        if definition.startswith(':' + DocResponseRuleParser.prefix):
            parser = DocResponseRuleParser()
        elif definition.startswith(':' + DocParameterRuleParser.prefix):
            parser = DocParameterRuleParser()
        else:
            raise RuleException(definition)
        return parser.parse(definition)

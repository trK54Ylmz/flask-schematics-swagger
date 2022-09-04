from typing import Optional, TypeVar

from .parameter import DocParameterRuleParser
from .response import DocResponseRuleParser
from .tag import DocTagRuleParser
from fss.exception.rule import RuleException
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
        Parse parameter or response or tag definition in function pydoc

        :param definition: raw function pydoc line
        :return: parameter or response or tag definition schema
        """
        for invalid in self.invalid_definitions:
            if definition.startswith(invalid):
                return None

        if definition.startswith(':' + DocResponseRuleParser.prefix):
            parser = DocResponseRuleParser()
        elif definition.startswith(':' + DocParameterRuleParser.prefix):
            parser = DocParameterRuleParser()
        elif definition.startswith(':' + DocTagRuleParser.prefix):
            parser = DocTagRuleParser()
        else:
            raise RuleException(definition)
        return parser.parse(definition)

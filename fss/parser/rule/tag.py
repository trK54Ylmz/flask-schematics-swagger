import re

from .parser import RuleParser
from fss.exception import ParameterException
from fss.schema.rule import DocTagRuleSchema, DocRuleType


class DocTagRuleParser(RuleParser):
    prefix = 'tag'
    pattern = r'^:tag:(.*?)$'

    def parse(self, definition: str) -> DocTagRuleSchema:
        """
        Parse tag definition in function pydoc

        :param definition: raw function pydoc line
        :return: tag definition schema
        """
        match = re.match(self.pattern, definition, re.IGNORECASE)

        if not match:
            raise ParameterException(definition)

        name = match.group(1).strip()
        if len(name) == 0:
            raise ParameterException(definition)

        schema = DocTagRuleSchema()
        schema.kind = DocRuleType.TAG
        schema.name = name

        return schema

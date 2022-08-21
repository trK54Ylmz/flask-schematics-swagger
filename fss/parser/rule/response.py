import re
import importlib

from .parser import RuleParser
from fss.exception import RuleException
from fss.schema.rule import DocResponseRuleSchema, DocRuleType


class DocResponseRuleParser(RuleParser):
    prefix = 'response'
    pattern = r':response[\s]{1,}([0-9]{3})[\s]{1,}([a-zA-Z\_\.]+):(.*?)'

    def parse(self, definition: str) -> DocResponseRuleSchema:
        """
        Parse response definition in function pydoc

        :param definition: raw function pydoc line
        :return: response definition schema
        """
        match = re.match(self.pattern, definition)

        if not match:
            raise RuleException(definition)

        path = match.group(2)

        return DocResponseRuleSchema(
            kind=DocRuleType.RESPONSE,
            model_name=match.group(2),
            status_code=int(match.group(1)),
            description=match.group(3).strip(),
            model=self.load_class(path.strip()),
        )

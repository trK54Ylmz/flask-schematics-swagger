import re

from .parser import RuleParser
from fss.exception import RuleException
from fss.schema import Schema
from fss.schema.rule import DocResponseRuleSchema, DocRuleType


class DocResponseRuleParser(RuleParser):
    prefix = 'response'
    pattern = r':response[\s]{1,}([0-9]{3})[\s]{1,}([a-z\_\.\[\]]+):(.*?)'

    def parse(self, definition: str) -> DocResponseRuleSchema:
        """
        Parse response definition in function pydoc

        :param definition: raw function pydoc line
        :return: response definition schema
        """
        match = re.match(self.pattern, definition, re.IGNORECASE)

        if not match:
            raise RuleException(definition)

        description = match.group(3).strip()
        status_code = int(match.group(1).strip())
        type_definition = match.group(2).strip()

        type_model = None
        if type_definition.lower() == 'none':
            type_name = 'None'
            type_model = None
        elif type_definition in Schema.PRIMITIVES:
            type_name = type_definition
        elif type_definition.startswith('array[') and type_definition.endswith(']'):
            type_name = 'array'
            type_model = type_definition[6:-1]
        else:
            type_name = 'object'
            type_model = type_definition

        schema = DocResponseRuleSchema()
        schema.kind = DocRuleType.RESPONSE
        schema.type = type_model
        schema.type_name = type_name
        schema.description = description
        schema.status_code = status_code

        return schema

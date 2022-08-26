import re

from .parser import RuleParser
from fss.exception import ParameterException
from fss.schema import Schema
from fss.schema.rule import DocParameterRuleSchema, DocRuleType


class DocParameterRuleParser(RuleParser):
    prefix = 'parameter'
    allowed = ['query', 'header', 'body', 'path', 'formData']
    pattern = r'^:parameter[\s]{1,}([a-z]+)[\s]{1,}([a-z\_\.\[\]]+)[\s]{1,}([a-z\_]+):(.*?)$'
    default = r'^(.*?)([\s]{1,}(default:[\s]{1,}(.*?)))?$'

    def parse(self, definition: str) -> DocParameterRuleSchema:
        """
        Parse parameter definition in function pydoc

        :param definition: raw function pydoc line
        :return: parameter definition schema
        """
        match = re.match(self.pattern, definition, re.IGNORECASE)

        if not match:
            raise ParameterException(definition)

        in_name = match.group(1).strip()
        if in_name not in self.allowed:
            raise ParameterException(definition, parameter=in_name)

        name = match.group(3).strip()
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

        default = None
        description = match.group(4).strip()
        if len(description) > 0:
            default_match = re.match(self.default, description)
            default_section = default_match.group(4)
            if default_section is not None:
                description = default_match.group(1).strip()
                if default_section.strip() == 'None':
                    default = 'null'
                elif type_name in Schema.PRIMITIVES:
                    default = self.cast_default(default_section, type_name)
                else:
                    default = default_section

        schema = DocParameterRuleSchema()
        schema.kind = DocRuleType.PARAMETER
        schema.name = name
        schema.in_name = in_name
        schema.type = type_model
        schema.type_name = type_name
        schema.description = description
        schema.default = default

        return schema

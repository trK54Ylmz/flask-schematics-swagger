import re
from typing import Any
from xmlrpc.client import boolean

from .parser import RuleParser
from fss.exception import ParameterException
from fss.schema.rule import DocParameterRuleSchema, DocRuleType


class DocParameterRuleParser(RuleParser):
    prefix = 'parameter'
    allowed = ['query', 'header', 'body', 'path', 'formData']
    primitives = ['string', 'float', 'integer', 'boolean']
    pattern = r'^:parameter[\s]{1,}([a-zA-Z]+)[\s]{1,}([a-zA-Z\_\.]+)[\s]{1,}([a-zA-Z\_]+):(.*?)$'
    default = r'^(.*?)([\s]{1,}(default:[\s]{1,}(.*?)))?$'

    def cast_default(self, value: str, type: str) -> Any:
        """
        Cast default type by given type definition

        :param value: default value as string
        :param type: expected default value type
        :return: new default value in given type
        """
        if type == self.primitives[0]:
            return value

        if type == self.primitives[1]:
            return float(value)

        if type == self.primitives[2]:
            return int(value)

        if type == self.primitives[3]:
            return value in ['true', 'True', '1']

    def parse(self, definition: str) -> DocParameterRuleSchema:
        """
        Parse parameter definition in function pydoc

        :param definition: raw function pydoc line
        :return: parameter definition schema
        """
        match = re.match(self.pattern, definition)

        if not match:
            raise ParameterException(definition)

        in_name = match.group(1).strip()
        if in_name not in self.allowed:
            raise ParameterException(definition, parameter=in_name)

        type_model = None
        type_definition = match.group(2).strip()
        if type_definition in self.primitives:
            type_name = type_definition
        elif type_definition.startswith('array[') and type_definition.endswith(']'):
            type_name = 'array'
            length = len(type_definition)
            type_model = self.load_class(type_definition[1:length - 1])
        else:
            type_name = 'object'
            type_model = self.load_class(type_definition)

        default = None
        description = match.group(4).strip()
        if len(description) > 0:
            default_match = re.match(self.default, description)
            default_section = default_match.group(4)
            if default_section is not None:
                description = default_match.group(1).strip()
                if default_section.strip() == 'None':
                    default = 'null'
                elif type_name in self.primitives:
                    default = self.cast_default(default_section, type_name)
                else:
                    default = default_section

        return DocParameterRuleSchema(
            kind=DocRuleType.PARAMETER,
            in_name=in_name,
            type=type_model,
            type_name=type_name,
            description=description,
            default=default,
            name=match.group(3).strip(),
        )

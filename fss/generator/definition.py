from typing import Dict, List, Tuple, Type, Union

from .generator import Generator
from .type import DocResponseTypeGenerator, DocParameterTypeGenerator
from fss.exception import ParameterException
from fss.schema import DocSchema, Schema
from fss.schema.openapi import OpenApiDefinitionSchema
from fss.schema.rule.parameter import DocParameterRuleSchema
from fss.schema.rule.response import DocResponseRuleSchema
from schematics import Model
from wtforms import Form


class DocDefinitionGeneator(Generator):
    def __init__(self, schema: DocSchema) -> None:
        """
        Generate definitions for parameters and responses of given endpoint schema

        :param schema: endpoint schema
        """
        self.schema = schema
        self.definitions = dict()

    def get_schema(
        self,
        type: Type,
        model: Union[Form, Model],
    ) -> List[Tuple[str, OpenApiDefinitionSchema]]:
        """
        Get model definition of schematics model

        :param model: schematics model
        :return: api model definition
        """
        generator = type(model)

        return generator.generate()

    def define_parameters(
        self,
        schema: Union[DocResponseRuleSchema, DocParameterRuleSchema],
    ) -> None:
        """
        Generate definition schemas by given parameter definition

        :param schema: paremeter schema definition
        """
        model = None
        type = DocParameterTypeGenerator

        if schema.type_name == 'array':
            if schema.type in Schema.PRIMITIVES:
                return

            model = self.load_class(schema.type)
            if Form not in model.__mro__:
                raise ParameterException(definition=schema.type)

        if schema.type_name == 'object':
            model = self.load_class(schema.type)
            if Form not in model.__mro__:
                raise ParameterException(definition=schema.type)

        if model is None:
            return

        definitions = self.get_schema(type, model)
        for definition in definitions:
            self.definitions[definition[0]] = definition[1]

    def define_responses(
        self,
        schema: Union[DocResponseRuleSchema, DocParameterRuleSchema],
    ) -> None:
        """
        Generate definition schemas by given response schema definitions

        :param schema: respones schema definition
        """
        model = None
        type = DocResponseTypeGenerator

        if schema.type_name == 'array':
            if schema.type in Schema.PRIMITIVES:
                return

            model = self.load_class(schema.type)
            if Model not in model.__mro__:
                raise ParameterException(definition=schema.type)

        if schema.type_name == 'object':
            model = self.load_class(schema.type)
            if Model not in model.__mro__:
                raise ParameterException(definition=schema.type)

        if model is None:
            return

        definitions = self.get_schema(type, model)
        for definition in definitions:
            self.definitions[definition[0]] = definition[1]

    def generate(self) -> Dict[str, OpenApiDefinitionSchema]:
        """
        Generate list of api model definitions

        :return: list of model definitions
        """
        for r in self.schema.parameters:
            self.define_parameters(r)

        for r in self.schema.responses:
            self.define_responses(r)

        return self.definitions

from typing import Dict, List, Tuple, Union

from .generator import Generator
from .type import DocTypeGenerator
from schematics import Model
from fss.exception import ParameterException
from fss.schema import DocSchema, Schema
from fss.schema.openapi import OpenApiDefinitionSchema
from fss.schema.rule.parameter import DocParameterRuleSchema
from fss.schema.rule.response import DocResponseRuleSchema


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
        model: Model,
    ) -> List[Tuple[str, OpenApiDefinitionSchema]]:
        """
        Get model definition of schematics model

        :param model: schematics model
        :return: api model definition
        """
        generator = DocTypeGenerator(model)

        return generator.generate()

    def define_schemas(
        self,
        schema: Union[DocResponseRuleSchema, DocParameterRuleSchema],
    ) -> None:
        """
        Generate definition schemas by given parameter or response schema definitions

        :param schema: paremeter or respones schema definition
        """
        model = None
        if schema.type_name == 'array':
            if schema.type in Schema.PRIMITIVES:
                return

            model = self.load_class(schema.type)
            if Model not in model.__bases__:
                raise ParameterException(definition=schema.type)

        if schema.type_name == 'object':
            model = self.load_class(schema.type)
            if Model not in model.__bases__:
                raise ParameterException(definition=schema.type)

        if model is None:
            return

        definitions = self.get_schema(model)
        for definition in definitions:
            self.definitions[definition[0]] = definition[1]

    def generate(self) -> Dict[str, OpenApiDefinitionSchema]:
        """
        Generate list of api model definitions

        :return: list of model definitions
        """
        for r in self.schema.parameters:
            self.define_schemas(r)

        for r in self.schema.responses:
            self.define_schemas(r)

        return self.definitions

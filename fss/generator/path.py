from typing import Dict, List

from fss.schema import DocSchema, Method, Schema
from fss.exception import ParameterException
from fss.schema.rule import DocResponseRuleSchema
from fss.schema.openapi import (
    OpenApiDefinitionSchema, OpenApiMethodSchema, OpenApiResponseSchema,
    OpenApiRouteSchema, OpenApiItemSchema, OpenApiParameterSchema, OpenApiSchemaSchema
)


class DocPathGeneator:
    def __init__(
        self,
        schema: DocSchema,
        definitions: Dict[str, OpenApiDefinitionSchema],
    ) -> None:
        """
        Create path definition of the given endpoint schema and model definitions

        :param schema: endpoint schema
        :param definitions: list of model definitions
        """
        self.schema = schema
        self.definitions = definitions

    def define_schemas(self, response: DocResponseRuleSchema) -> OpenApiItemSchema:
        """
        Generate definition schemas by given parameter or response schema definitions

        :param schema: paremeter or respones schema definition
        :return: response schema
        """
        compound = OpenApiItemSchema()

        if response.type_name in ['array', 'object']:
            if response.type not in self.definitions.keys():
                raise ParameterException(definition=response.type)

            compound.ref = '#/definitions/' + response.type

            if response.type_name == 'array':
                schema = OpenApiSchemaSchema()
                schema.type = 'array'
                schema.items = compound

                return schema

            return compound

        compound.type = response.type

        return compound

    def get_responses(self) -> Dict[str, OpenApiResponseSchema]:
        """
        Get response schema according to list of status types of endpoint

        :return: list of response schema
        """
        responses = dict()

        for response in self.schema.responses:
            res = OpenApiResponseSchema()
            res.description = response.description
            res.schema = self.define_schemas(response)

            responses[response.status_code] = res

        return responses

    def get_parameters(self) -> List[OpenApiParameterSchema]:
        """
        Get parameter schemas according to list of parameters

        :return: list of request parameters schema
        """
        parameters = []

        for parameter in self.schema.parameters:
            param = OpenApiParameterSchema()
            param.name = parameter.name
            param.required = False
            param.type = parameter.type_name
            param.description = parameter.description

            if parameter.type_name in ['array', 'object']:
                item = OpenApiItemSchema()

                if parameter.type in Schema.PRIMITIVES:
                    item.type = parameter.type
                else:
                    item.ref = '#/definitions/' + parameter.type

                param.items = item

            parameters.append(param)

        return parameters

    def generate_model(self) -> OpenApiRouteSchema:
        """
        Generate endpoint definition

        :return: Swagger endpoint route definition
        """
        route = OpenApiRouteSchema()
        route.summary = self.schema.summary
        route.operation_id = self.schema.name
        route.description = self.schema.description
        route.parameters = self.get_parameters()
        route.responses = self.get_responses()

        return route

    def generate(self) -> OpenApiMethodSchema:
        """
        Generate request path definition

        :return: request path definition by status code
        """
        method = OpenApiMethodSchema()
        method_name = self.schema.method.lower()

        if method_name == Method.GET:
            method.get_method = self.generate_model()
        elif method_name == Method.POST:
            method.post_method = self.generate_model()
        elif method_name == Method.DELETE:
            method.delete_method = self.generate_model()

        return method

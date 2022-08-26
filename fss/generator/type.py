from typing import List, Tuple

from schematics import Model
from schematics.types import BaseType, ModelType
from fss.schema import Schema
from fss.schema.openapi import OpenApiDefinitionSchema
from fss.schema.openapi.item import OpenApiItemSchema
from fss.schema.openapi.schema import OpenApiSchemaSchema


class DocTypeGenerator:
    def __init__(self, model: Model) -> None:
        """
        Create list of api model definitions

        :param model: api model
        """
        self.model = model
        self.name = self.get_name(self.model)
        self.models = []

    def get_name(self, model: Model) -> str:
        """
        Get model name

        :param model: api model
        :return: model name
        """
        return model.__module__ + '.' + model.__name__

    def get_type(self, type: BaseType) -> str:
        """
        Get OpenApi type name of model field

        :param type: model field type
        :return: OpenApi type name
        """
        if type.native_type is str:
            return Schema.STRING

        if type.native_type is int:
            return Schema.INTEGER

        if type.native_type is float:
            return Schema.NUMBER

        if type.native_type is bool:
            return Schema.BOOLEAN

        if type.native_type is list:
            return Schema.ARRAY

        if type.native_type is dict:
            return Schema.OBJECT

        return Schema.OBJECT

    def get_model_type(self, field: BaseType) -> OpenApiItemSchema:
        """
        Get model field OpenApi schema

        :param field: model field
        :return: OpenApi field definition
        """
        generator = DocTypeGenerator(field.native_type)

        items = generator.generate()
        if len(items) > 0:
            for item in items:
                self.models.append(item)

        compound = OpenApiItemSchema()
        compound.ref = '#/definitions/' + self.get_name(field.native_type)

        return compound

    def get_compound_type(self, field: BaseType) -> OpenApiItemSchema:
        """
        Get OpenApi model reference of the model field

        :param field: model field
        :return: model field reference
        """
        compound = OpenApiItemSchema()
        compound.ref = self.get_type(field.field)

        return compound

    def get_object_type(self, field: BaseType) -> OpenApiItemSchema:
        """
        Get model reference of model field

        :param field: model field
        :return: model reference
        """
        generator = DocTypeGenerator(field.field.native_type)

        items = generator.generate()
        if len(items) > 0:
            for item in items:
                self.models.append(item)

        if field.native_type is list:
            compound = OpenApiItemSchema()
            compound.type = self.get_type(field.field)
            compound.ref = '#/definitions/' + self.get_name(field.field.native_type)
        elif field.native_type is dict:
            compound = OpenApiItemSchema()
            compound.ref = '#/definitions/' + self.get_name(field.field.native_type)

        return compound

    def generate(self) -> List[Tuple[str, OpenApiDefinitionSchema]]:
        """
        Generate list of model definitions according to model name

        :return: list of models definitions
        """
        schema = OpenApiDefinitionSchema()
        schema.properties = dict()
        schema.type = 'object'

        required = []
        for name in self.model.fields:
            field = getattr(self.model, name)

            property = OpenApiSchemaSchema()

            if field.required:
                required.append(name)

            property.type = self.get_type(field)

            if isinstance(field, ModelType):
                property.items = self.get_model_type(field)
            elif field.is_compound:
                if field.field.is_compound:
                    property.items = self.get_object_type(field)
                else:
                    property.items = self.get_compound_type(field)

            schema.properties[name] = property

        schema.required = required

        pairs = (self.name, schema)

        self.models.append(pairs)

        return self.models

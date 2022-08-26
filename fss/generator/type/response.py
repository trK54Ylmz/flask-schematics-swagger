from datetime import datetime, date
from typing import List, Optional, Tuple

from .type import DocTypeGenerator
from schematics import Model
from schematics.types import BaseType, ModelType
from fss.schema import Schema
from fss.schema.openapi import OpenApiDefinitionSchema
from fss.schema.openapi.item import OpenApiItemSchema
from fss.schema.openapi.schema import OpenApiSchemaSchema


class DocResponseTypeGenerator(DocTypeGenerator):
    def __init__(self, model: Model) -> None:
        """
        Create list of api model definitions

        :param model: api model
        """
        self.model = model
        self.name = self.get_name(self.model)
        self.models = []

    def get_type(self, type: BaseType) -> Tuple[str, Optional[str]]:
        """
        Get OpenApi type name of model field

        :param type: model field type
        :return: OpenApi type name
        """
        if type.native_type is str:
            return Schema.STRING, None

        if type.native_type is datetime:
            return Schema.STRING, Schema.DATETIME

        if type.native_type is date:
            return Schema.STRING, Schema.DATE

        if type.native_type is int:
            return Schema.INTEGER, None

        if type.native_type is float:
            return Schema.NUMBER, None

        if type.native_type is bool:
            return Schema.BOOLEAN, None

        if type.native_type is list:
            return Schema.ARRAY, None

        if type.native_type is dict:
            return Schema.OBJECT, None

        return Schema.OBJECT, None

    def get_model_type(self, field: BaseType) -> OpenApiItemSchema:
        """
        Get model field OpenApi schema

        :param field: model field
        :return: OpenApi field definition
        """
        generator = DocResponseTypeGenerator(field.native_type)

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
        type = self.get_type(field.field)

        compound = OpenApiItemSchema()
        compound.type = type[0]
        compound.format = type[1]

        return compound

    def get_object_type(self, field: BaseType) -> OpenApiItemSchema:
        """
        Get model reference of model field

        :param field: model field
        :return: model reference
        """
        generator = DocResponseTypeGenerator(field.field.native_type)

        items = generator.generate()
        if len(items) > 0:
            for item in items:
                self.models.append(item)

        if field.native_type is list:
            type = self.get_type(field.field)

            compound = OpenApiItemSchema()
            compound.type = type[0]
            compound.format = type[1]
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

            type = self.get_type(field)
            property.type = type[0]
            property.format = type[1]

            if isinstance(field, ModelType):
                property = self.get_model_type(field)
                property.type = type[0]
                property.format = type[1]
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

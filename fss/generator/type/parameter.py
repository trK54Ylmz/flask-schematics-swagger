from typing import List, Optional, Tuple, Union

from .type import DocTypeGenerator
from fss.schema import Schema
from fss.schema.openapi import OpenApiDefinitionSchema
from fss.schema.openapi.item import OpenApiItemSchema
from fss.schema.openapi.schema import OpenApiSchemaSchema
from wtforms import Form, Field
from wtforms.fields.core import UnboundField
from wtforms.validators import DataRequired, InputRequired
from wtforms.fields import (
    BooleanField, IntegerField, StringField, DateTimeField, DateField, FloatField,
    FieldList, FormField
)


class DocParameterTypeGenerator(DocTypeGenerator):
    def __init__(self, model: Form) -> None:
        """
        Create list of api model definitions

        :param model: api model
        """
        self.models = []
        self.model = model
        self.name = self.get_name(self.model)

    def get_type(
        self,
        type: Union[Field, UnboundField],
    ) -> Tuple[str, Optional[str]]:
        """
        Get OpenApi type name of model field

        :param type: model field type
        :return: OpenApi type name
        """
        if type is UnboundField:
            type = type.field_class

        if type is StringField:
            return Schema.STRING, None

        if type is DateTimeField:
            return Schema.STRING, Schema.DATETIME

        if type is DateField:
            return Schema.STRING, Schema.DATE

        if type is IntegerField:
            return Schema.INTEGER, None

        if type is FloatField:
            return Schema.NUMBER, None

        if type is BooleanField:
            return Schema.BOOLEAN, None

        if type is FieldList:
            return Schema.ARRAY, None

        if type is FormField:
            return Schema.OBJECT, None

        return Schema.OBJECT, None

    def get_model_type(self, field: Form) -> OpenApiItemSchema:
        """
        Get model field OpenApi schema

        :param field: model field
        :return: OpenApi field definition
        """
        generator = DocParameterTypeGenerator(field)

        items = generator.generate()
        if len(items) > 0:
            for item in items:
                self.models.append(item)

        compound = OpenApiItemSchema()
        compound.ref = '#/definitions/' + self.get_name(field)

        return compound

    def get_compound_type(self, field: Field) -> OpenApiItemSchema:
        """
        Get OpenApi model reference of the model field

        :param field: model field
        :return: model field reference
        """
        type = self.get_type(field)

        compound = OpenApiItemSchema()
        compound.type = type[0]
        compound.format = type[1]

        return compound

    def get_object_type(self, field: Form) -> OpenApiItemSchema:
        """
        Get model reference of model field

        :param field: model field
        :return: model reference
        """
        generator = DocParameterTypeGenerator(field)

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
        for name, field in vars(self.model).items():
            if not isinstance(field, UnboundField):
                continue

            if len(field.args) > 0:
                name = field.args[0]

            if 'name' in field.kwargs:
                name = field.kwargs['name']

            property = OpenApiSchemaSchema()

            if len(field.field_class.validators) > 0:
                for validator in field.field_class.validators:
                    if isinstance(validator, (DataRequired, InputRequired)):
                        required.append(name)

            type = self.get_type(field)
            property.type = type[0]
            property.format = type[1]

            if field.field_class is FormField or field.field_class in FormField.__mro__:
                property = self.get_model_type(field.args[0])
                property.type = type[0]
                property.format = type[1]
            elif field.field_class is FieldList or field.field_class in FieldList.__mro__:
                child = field.args[0]
                if child is not UnboundField:
                    property.items = self.get_compound_type(child)
                elif child.field_class is FormField or child.field_class in FormField.__mro__:
                    property.items = self.get_object_type(child.args[0])
            else:
                type = self.get_type(field.field_class)
                property.type = type[0]
                property.format = type[1]

            schema.properties[name] = property

        schema.required = required

        pairs = (self.name, schema)

        self.models.append(pairs)

        return self.models

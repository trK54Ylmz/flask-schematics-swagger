from typing import Any, List, Optional, Tuple

from fss.schema.openapi import OpenApiDefinitionSchema
from fss.schema.openapi.item import OpenApiItemSchema


class DocTypeGenerator:
    def get_name(self, model: Any) -> str:
        """
        Get model name

        :param model: api model
        :return: model name
        """
        return model.__module__ + '.' + model.__name__

    def get_type(self, type: Any) -> Tuple[str, Optional[str]]:
        """
        Get OpenApi type name of model field

        :param type: model field type
        :return: OpenApi type name and format
        """
        raise NotImplementedError

    def get_model_type(self, field: Any) -> OpenApiItemSchema:
        """
        Get model field OpenApi schema

        :param field: model field
        :return: OpenApi field definition
        """
        raise NotImplementedError

    def get_compound_type(self, field: Any) -> OpenApiItemSchema:
        """
        Get OpenApi model reference of the model field

        :param field: model field
        :return: model field reference
        """
        raise NotImplementedError

    def get_object_type(self, field: Any) -> OpenApiItemSchema:
        """
        Get model reference of model field

        :param field: model field
        :return: model reference
        """
        raise NotImplementedError

    def generate(self) -> List[Tuple[str, OpenApiDefinitionSchema]]:
        """
        Generate list of model definitions according to model name

        :return: list of models definitions
        """
        raise NotImplementedError

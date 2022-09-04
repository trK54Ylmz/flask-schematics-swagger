from typing_extensions import Self

from fss.exception import ParameterException
from fss.schema.openapi import OpenApiSecurityDefinitionSchema


class SecurityDefinition:
    def __init__(self, name: str) -> None:
        """
        Define security schema

        :param str name: secuity name
        """
        self.name = name
        self.schema = None

    def basic(self) -> Self:
        """
        Create basic authntication definition
        """
        schema = OpenApiSecurityDefinitionSchema()
        schema.type = 'basic'

        self.schema = schema

        return self

    def api_key(self, in_name: str, name: str) -> Self:
        """
        Create api key security definition
        """
        if in_name not in ['query', 'header']:
            raise ParameterException(definition=in_name)

        schema = OpenApiSecurityDefinitionSchema()
        schema.name = name
        schema.type = 'apiKey'
        schema.in_name = in_name

        self.schema = schema

        return self

    def oauth2(self) -> None:
        raise Exception('Not supported yet.')

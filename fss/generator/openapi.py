from typing import List, Optional

from .definition import DocDefinitionGeneator
from .path import DocPathGeneator
from fss.parser import DocParser
from fss.security import SecurityDefinition
from fss.schema import DocSchema
from fss.schema.openapi import OpenApiSchema, OpenApiInfoSchema


class OpenApiGenerator:
    def __init__(
        self,
        base: Optional[str] = None,
        host: Optional[str] = None,
        version: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        security: Optional[SecurityDefinition] = None,
        route: Optional[str] = None,
        produces: Optional[List[str]] = None,
        consumes: Optional[List[str]] = None,
    ) -> None:
        """
        OpenApi generator by info parameters

        :param base: api base path
        :param host: api host name
        :param version: api version
        :param route: request base path
        :param title: OpenApi definition title
        :param security: OpenApi security definition
        :param description: OpenApi definition description
        :param produces: OpenApi default response body type
        :param consumes: OpenApi default request body type
        """
        self.base = base
        self.host = host
        self.route = route
        self.security = security
        self.schemas: List[DocSchema] = []
        self.version = version or '0.1'
        self.title = title or 'api title'
        self.description = description or 'api description'
        self.consumes = consumes or ['application/json']
        self.produces = produces or ['application/json']

    def add(self, parser: DocParser) -> None:
        """
        Add pydoc definition parser schema

        :param parser: doc parser
        """
        schema = parser.parse()
        if schema is None:
            return

        self.schemas.append(schema)

    def generate(self) -> OpenApiSchema:
        """
        Generate OpenApi schema

        :return: OpenApi schema definition
        """
        info = OpenApiInfoSchema()
        info.version = self.version
        info.title = self.title
        info.description = self.description

        schema = OpenApiSchema()
        schema.tags = []
        schema.info = info
        schema.paths = dict()
        schema.definitions = dict()
        schema.base_path = self.base
        schema.consumes = self.consumes
        schema.produces = self.produces

        if self.security is not None:
            schema.security = [dict()]
            schema.security[0][self.security.name] = ['']
            schema.security_definition = dict()
            schema.security_definition[self.security.name] = self.security.schema

        for s in self.schemas:
            generator = DocDefinitionGeneator(s)
            definition = generator.generate()

            for key, value in definition.items():
                schema.definitions[key] = value

            generator = DocPathGeneator(s, schema.definitions)
            path = generator.generate()

            schema.paths[s.url] = path

            if s.tag is not None:
                schema.tags.append(s.tag)

        return schema

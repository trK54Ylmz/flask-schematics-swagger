from typing import List, Optional

from .definition import DocDefinitionGeneator
from .path import DocPathGeneator
from fss.parser import DocParser
from fss.schema import DocSchema
from fss.schema.openapi import OpenApiSchema, OpenApiInfoSchema


class OpenApiGenerator:
    def __init__(
        self,
        host: Optional[str] = None,
        version: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        route: Optional[str] = None,
        produces: Optional[List[str]] = None,
        consumes: Optional[List[str]] = None,
    ) -> None:
        """
        OpenApi generator by info parameters

        :param host: api host name
        :param version: api version
        :param route: request base path
        :param title: OpenApi definition title
        :param description: OpenApi definition description
        :param produces: OpenApi default response body type
        :param consumes: OpenApi default request body type
        """
        self.host = host
        self.version = version
        self.route = route
        self.title = title
        self.description = description
        self.schemas: List[DocSchema] = []
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
        schema.consumes = self.consumes
        schema.produces = self.produces
        schema.info = info
        schema.paths = dict()
        schema.definitions = dict()

        for s in self.schemas:
            generator = DocDefinitionGeneator(s)
            definition = generator.generate()

            for key, value in definition.items():
                schema.definitions[key] = value

            generator = DocPathGeneator(s, schema.definitions)
            path = generator.generate()

            schema.paths[s.url] = path

        return schema

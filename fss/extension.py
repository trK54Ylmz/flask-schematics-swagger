from typing import Optional
from flask import Flask
from fss.generator import OpenApiGenerator, DocSchemaGeneator


class FlaskSchematicsSwagger:
    def __init__(
        self,
        app: Flask,
        host: Optional[str] = None,
        version: Optional[str] = None,
        route: Optional[str] = None,
    ) -> None:
        """
        Initialize swagger documentation for Flask with Schematics

        :param app: flask app
        :param host: host name with or without port
        :param version: api version
        :param route: path for swagger documentation
        """
        self.app = app
        self.host = host
        self.version = version
        self.route = route or '/documentation'

    def add_route(self) -> None:
        """
        Parse documents and add routing on the flask route map
        """
        openapi = OpenApiGenerator(self.host, self.version, self.route)

        for item in self.app.url_map.iter_rules():
            doc = DocSchemaGeneator(self.app, item)

            openapi.add(doc)

        openapi.generate()

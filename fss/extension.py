from .security import SecurityDefinition
from typing import Optional
from flask import Flask
from fss.parser import DocParser
from fss.generator import OpenApiGenerator
from fss.view import FlaskView


class FlaskSchematicsSwagger:
    def __init__(
        self,
        app: Flask,
        host: Optional[str] = None,
        version: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        route: Optional[str] = None,
        security: Optional[SecurityDefinition] = None,
    ) -> None:
        """
        Initialize swagger documentation for Flask with Schematics

        :param app: flask app
        :param host: host name with or without port
        :param version: api version
        :param route: path for swagger documentation
        """
        self.app = app
        self.route = route or '/documentation'
        self.openapi = OpenApiGenerator(host, version, title, description, security, self.route)
        self.view = FlaskView(self.app, self.route, self.openapi)

    def add_route(self) -> None:
        """
        Parse documents and add routing on the flask route map
        """
        for item in self.app.url_map.iter_rules():
            parser = DocParser(self.app, item)

            self.openapi.add(parser)

        self.view.register()

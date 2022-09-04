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
        security: Optional[SecurityDefinition] = None,
        base: Optional[str] = None,
        route: Optional[str] = None,
    ) -> None:
        """
        Initialize swagger documentation for Flask with Schematics

        :param app: flask app
        :param host: host name with or without port
        :param version: api version
        :param security: api security definition
        :param base: flask base app route
        :param route: path for swagger documentation
        """
        route = route or '/documentation'
        base = base or '/'

        self.app = app
        self.base = base
        self.route = route
        self.openapi = OpenApiGenerator(base, host, version, title, description, security, route)
        self.view = FlaskView(self.app, self.route, self.base, self.openapi)

    def add_route(self) -> None:
        """
        Parse documents and add routing on the flask route map
        """
        for item in self.app.url_map.iter_rules():
            parser = DocParser(self.app, item, self.base)

            self.openapi.add(parser)

        self.view.register()

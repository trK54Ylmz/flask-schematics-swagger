import json
from pathlib import Path
from typing import Optional

from flask import Flask, Response, make_response, render_template_string, send_from_directory
from fss.generator import OpenApiGenerator
from fss.util import CustomEncoder


class FlaskView:
    def __init__(self, app: Flask, route: str, base: str, openapi: OpenApiGenerator) -> None:
        """
        Create and register flask routes for Swagger UI

        :param app: active flask app
        :param base: api base route
        :param route: base route name for Swagger UI
        """
        self.app = app
        self.openapi = openapi
        self.current = Path(__file__).parent.parent.absolute()
        self.route = (base + route).replace('//', '/')

    def html(self) -> Response:
        """
        Returns Swagger UI html file(s)

        :param name: requested html file
        :return: swagger html file as response
        """
        path = self.route + '/swagger.json'
        content = self.current / 'static' / 'index.html'

        return render_template_string(content.read_text(encoding='utf-8'), url=str(path))

    def static(self, name: Optional[str] = None) -> Response:
        """
        Returns Swagger UI static files

        :param name: request swagger file
        :return: swagger file as response
        """
        return send_from_directory(self.current / 'static', name)

    def swagger(self) -> Response:
        """
        Returns Swagger document

        :return: swagger document as json response
        """
        schema = self.openapi.generate()
        output = json.dumps(schema, cls=CustomEncoder)

        response = make_response(output)
        response.headers['content-type'] = 'application/json; charset=utf-8'

        return response

    def register(self) -> None:
        """
        Register flask routes for Swagger UI and yaml file
        """
        self.app.add_url_rule(self.route + '/', 'fss_html', self.html)
        self.app.add_url_rule(self.route + '/<name>', 'fss_static', self.static)
        self.app.add_url_rule(self.route + '/swagger.json', 'fss_swagger', self.swagger)

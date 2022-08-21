from typing import Any
from flask import Flask
from fss.parser import DocParser
from werkzeug.routing import Rule


class DocSchemaGeneator:
    def __init__(self, app: Flask, rule: Rule) -> None:
        self.app = app
        self.rule = rule

    def generate(self) -> dict[str, Any]:
        function = self.app.view_functions.get(self.rule.endpoint)
        doc = function.__doc__
        if doc is None:
            return None

        parser = DocParser(doc)
        parser.parse()

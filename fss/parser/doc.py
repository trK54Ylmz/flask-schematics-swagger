import inspect
from typing import List, Optional
from flask import Flask
from fss.parser.rule import DocRuleParser
from fss.schema import DocSchema
from werkzeug.routing import Rule


class DocParser:
    def __init__(self, app: Flask, rule: Rule, base: Optional[str] = None) -> None:
        """
        Parses and generates document schema function definition

        :param app: flask app
        :param rule: flask endpoint rule
        :param base: flask base api route
        """
        self.app = app
        self.rule = rule
        self.base = base

    def extract_doc(self) -> str:
        '''
        Extract function pydoc definition

        :return: function pydoc
        '''
        function = self.app.view_functions.get(self.rule.endpoint)

        return function.__doc__

    def extract_method(self, methods: List[str]) -> str:
        '''
        Extract endpoint HTTP method by given list of methods

        :param methods: list of methods accepted by the endpoint
        :return: main http method for the endpoint
        '''
        if len(methods) > 0:
            if 'POST' in methods:
                return 'POST'
            if 'DELETE' in methods:
                return 'DELETE'
            if 'PATCH' in methods:
                return 'PATCH'

        return 'GET'

    def parse(self) -> Optional[DocSchema]:
        """
        Parse function definition

        :return: endpoint schema definition, if exists
        """
        doc = self.extract_doc()
        if doc is None:
            return None

        doc = inspect.cleandoc(doc)

        lines = doc.splitlines()
        if len(lines) == 0:
            return None

        name = self.rule.endpoint
        method = self.extract_method(self.rule.methods)
        url = '/' + self.rule.rule.lstrip(self.base or '/')

        schema = DocSchema(name, url, method, doc)

        rule_def = None
        summary = None
        description = None

        for i, line in enumerate(lines):
            if line.startswith(':'):
                rule_def = line if rule_def is None else rule_def + ' ' + line

                if i + 1 == len(lines) or lines[i + 1].startswith(':'):
                    parser = DocRuleParser()
                    rule = parser.parse(rule_def)
                    if rule is None:
                        rule_def = None
                        continue

                    # add new rule
                    schema.add_rule(rule)
                    rule_def = None
                continue

            if schema.summary is None:
                if line != '':
                    summary = line if summary is None else summary + line.strip()
                    summary += '\n'
                else:
                    schema.summary = summary.strip()
                continue

            if schema.description is None:
                if line != '':
                    description = line if description is None else description + line.strip()
                    description += '\n'
                else:
                    schema.description = description.strip()
                    continue

        return schema

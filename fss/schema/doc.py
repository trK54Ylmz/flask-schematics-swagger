from typing import List, Optional
from fss.schema.rule import (
    DocParameterRuleSchema, DocResponseRuleSchema, DocRuleSchema, DocTagRuleSchema
)


class DocSchema:
    doc: str
    url: str
    method: str
    name: str
    tag: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    parameters: List[DocParameterRuleSchema] = []
    responses: List[DocResponseRuleSchema] = []

    def __init__(self, name: str, url: str, method: str, doc: str) -> None:
        """
        Create endpoint schema with given function documentation

        :param doc: function pydoc
        """
        self.doc = doc
        self.url = url
        self.name = name
        self.method = method
        self.responses = []
        self.parameters = []

    def add_tag(self, rule: DocTagRuleSchema) -> None:
        """
        Add tag definition for the endpoint

        :param rule: tag definition
        """
        self.tag = rule.name

    def add_parameter(self, rule: DocParameterRuleSchema) -> None:
        """
        Add parameter definition for the endpoint

        :param rule: parameter definition
        """
        self.parameters.append(rule)

    def add_response(self, rule: DocResponseRuleSchema) -> None:
        """
        Add response definition for the endpoint

        :param rule: response definition
        """
        self.responses.append(rule)

    def add_rule(self, rule: DocRuleSchema) -> None:
        """
        Add parameter or response definition for the endpoint

        :param rule: parameter or response definition
        """
        if isinstance(rule, DocParameterRuleSchema):
            self.add_parameter(rule)
        elif isinstance(rule, DocTagRuleSchema):
            self.add_tag(rule)
        else:
            self.add_response(rule)

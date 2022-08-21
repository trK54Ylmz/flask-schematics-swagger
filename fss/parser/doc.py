import inspect
from typing import Optional
from fss.parser.rule import DocRuleParser
from fss.schema import DocSchema


class DocParser:
    def __init__(self, doc: str) -> None:
        """
        Parses and generates document schema function definition

        :param doc: function pydoc
        """
        self.doc = doc

    def parse(self) -> Optional[DocSchema]:
        """
        Parse function definition

        :return: endpoint schema definition, if exists
        """
        doc = inspect.cleandoc(self.doc)

        lines = doc.splitlines()
        if len(lines) == 0:
            return None

        schema = DocSchema(doc)

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

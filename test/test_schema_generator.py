from flask import Flask
from fss.generator import DocSchemaGeneator
from fss.parser import DocParser
from test.endpoint import user_multi_summary


class TestSchemaGenerator:
    def setup_method(self, _):
        self.app = Flask('test')
        self.app.testing = True

    def teardown_method(self, _):
        self.app = None

    def test_simple_schema(self):
        self.app.add_url_rule('/example', view_func=user_multi_summary, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])
        content = parser.parse()

        generator = DocSchemaGeneator(content)
        schema = generator.generate()

        assert '/example' in schema.keys()
        assert 'get' in schema['/example'].keys()
        assert 'summary' in schema['/example']['get'].keys()
        assert schema['/example']['get']['summary'] == 'A\nB'
        assert schema['/example']['get']['description'] == 'Y\nZ'
        assert schema['/example']['get']['operationId'] == 'user_multi_summary'

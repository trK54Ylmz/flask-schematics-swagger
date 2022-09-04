from flask import Flask
from fss.parser import DocParser
from fss.schema.rule import DocRuleType
from test.endpoint import user_complex_type, user_single_summary, user_multi_summary, user_with_tag


class TestDocParser:
    def setup_method(self, _):
        self.app = Flask('test')
        self.app.testing = True

    def teardown_method(self, _):
        self.app = None

    def test_single_line_summary(self):
        self.app.add_url_rule('/example', view_func=user_single_summary, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])
        schema = parser.parse()

        assert schema.summary == 'A'

    def test_multi_line_summary(self):
        self.app.add_url_rule('/example', view_func=user_multi_summary, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])
        schema = parser.parse()

        assert schema.summary == 'A\nB'

    def test_single_line_description(self):
        self.app.add_url_rule('/example', view_func=user_single_summary, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])
        schema = parser.parse()

        assert schema.description == 'Z'

    def test_url_prefix(self):
        self.app.add_url_rule('/a/b/c/a', view_func=user_single_summary, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1], '/a/b')
        schema = parser.parse()

        assert schema.url == '/c/a'

    def test_multi_line_description(self):
        self.app.add_url_rule('/example', view_func=user_multi_summary, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])
        schema = parser.parse()

        assert schema.description == 'Y\nZ'

    def test_simple_response(self):
        self.app.add_url_rule('/example', view_func=user_multi_summary, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])
        schema = parser.parse()

        assert schema.responses[0].kind == DocRuleType.RESPONSE
        assert schema.responses[0].status_code == 200
        assert schema.responses[0].type_name == 'object'
        assert schema.responses[0].type == 'test.schema.response.UserSuccessResponse'
        assert schema.responses[1].kind == DocRuleType.RESPONSE
        assert schema.responses[1].status_code == 403
        assert schema.responses[1].type_name == 'object'
        assert schema.responses[1].type == 'test.schema.response.UserErrorResponse'

    def test_simple_parameter(self):
        self.app.add_url_rule('/example', view_func=user_multi_summary, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])
        schema = parser.parse()

        assert len(schema.parameters) == 2
        assert schema.parameters[0].kind == DocRuleType.PARAMETER
        assert schema.parameters[0].name == 'user_id'
        assert schema.parameters[0].in_name == 'query'
        assert schema.parameters[0].type_name == 'integer'
        assert schema.parameters[0].description == 'the user id filter.'
        assert schema.parameters[0].default == 'null'
        assert schema.parameters[1].kind == DocRuleType.PARAMETER
        assert schema.parameters[1].name == 'user'
        assert schema.parameters[1].in_name == 'body'
        assert schema.parameters[1].type_name == 'object'
        assert schema.parameters[1].type == 'test.schema.request.UserRequest'
        assert schema.parameters[1].description == 'the user form'
        assert schema.parameters[1].default is None

    def test_complex_type(self):
        self.app.add_url_rule('/example', view_func=user_complex_type, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])
        schema = parser.parse()

        assert len(schema.parameters) == 2
        assert schema.parameters[0].kind == DocRuleType.PARAMETER
        assert schema.parameters[0].name == 'a'
        assert schema.parameters[0].in_name == 'query'
        assert schema.parameters[0].type_name == 'array'
        assert schema.parameters[0].description == 'b'
        assert schema.parameters[0].default is None
        assert schema.parameters[1].kind == DocRuleType.PARAMETER
        assert schema.parameters[1].name == 'b'
        assert schema.parameters[1].in_name == 'query'
        assert schema.parameters[1].type_name == 'float'
        assert schema.parameters[1].type is None
        assert schema.parameters[1].description == 'c'
        assert schema.parameters[1].default is None

    def test_user_with_tag(self):
        self.app.add_url_rule('/example', view_func=user_with_tag, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])
        schema = parser.parse()

        assert schema.tag == 'user'

import json
from flask import Flask
from fss.generator.openapi import OpenApiGenerator
from fss.parser import DocParser
from fss.security import SecurityDefinition
from test.endpoint import user_complex_type, user_multi_summary, user_with_tag
from fss.util import CustomEncoder


class TestSchemaGenerator:
    def setup_method(self, _):
        self.app = Flask('test')
        self.app.testing = True

    def teardown_method(self, _):
        self.app = None

    def test_multi_response(self):
        self.app.add_url_rule('/example', view_func=user_multi_summary, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])

        openapi = OpenApiGenerator()
        openapi.add(parser)

        openapi = openapi.generate()

        schema = openapi.paths
        output = json.dumps(schema, cls=CustomEncoder)
        schema = json.loads(output)

        assert '/example' in schema.keys()
        assert 'get' in schema['/example'].keys()
        assert 'summary' in schema['/example']['get'].keys()
        assert schema['/example']['get']['summary'] == 'A\nB'
        assert schema['/example']['get']['description'] == 'Y\nZ'
        assert schema['/example']['get']['operationId'] == 'user_multi_summary'
        assert 'responses' in schema['/example']['get']

    def test_simple_paths(self):
        self.app.add_url_rule('/example', view_func=user_complex_type, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])

        openapi = OpenApiGenerator()
        openapi.add(parser)

        openapi = openapi.generate()

        schema = openapi.paths
        output = json.dumps(schema, cls=CustomEncoder)
        schema = json.loads(output)

        ref = '#/definitions/test.schema.response.UserSuccessResponse'

        assert '/example' in schema.keys()
        assert 'get' in schema['/example'].keys()
        assert 'responses' in schema['/example']['get']
        assert '200' in schema['/example']['get']['responses']
        assert 'schema' in schema['/example']['get']['responses']['200']
        assert 'items' in schema['/example']['get']['responses']['200']['schema']
        assert schema['/example']['get']['responses']['200']['schema']['type'] == 'array'
        assert schema['/example']['get']['responses']['200']['schema']['items']['$ref'] == ref

    def test_simple_parameters(self):
        self.app.add_url_rule('/example', view_func=user_complex_type, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])

        openapi = OpenApiGenerator()
        openapi.add(parser)

        openapi = openapi.generate()

        schema = openapi.paths
        output = json.dumps(schema, cls=CustomEncoder)
        schema = json.loads(output)

        assert '/example' in schema.keys()
        assert 'get' in schema['/example'].keys()
        assert 'parameters' in schema['/example']['get'].keys()

        parameters = schema['/example']['get']['parameters']

        assert len(parameters) == 2
        assert parameters[0]['name'] == 'a'
        assert parameters[0]['description'] == 'b'
        assert parameters[0]['schema']['type'] == 'array'
        assert parameters[0]['schema']['items']['type'] == 'integer'
        assert parameters[1]['name'] == 'b'
        assert parameters[1]['description'] == 'c'
        assert parameters[1]['type'] == 'float'
        assert 'types' not in parameters[1]

    def test_security(self):
        self.app.add_url_rule('/example', view_func=user_complex_type, methods=['GET', 'HEAD'])

        security = SecurityDefinition('test')
        security.api_key('header', 'X-Test')

        parser = DocParser(self.app, self.app.url_map._rules[1])

        openapi = OpenApiGenerator(security=security)
        openapi.add(parser)

        openapi = openapi.generate()

        output = json.dumps(openapi, cls=CustomEncoder)
        schema = json.loads(output)

        assert 'security' in schema.keys()
        assert len(schema['security']) > 0
        assert 'test' in schema['security'][0].keys()

        assert 'securityDefinitions' in schema.keys()
        assert 'test' in schema['securityDefinitions'].keys()
        assert schema['securityDefinitions']['test']['type'] == 'apiKey'
        assert schema['securityDefinitions']['test']['name'] == 'X-Test'
        assert schema['securityDefinitions']['test']['in'] == 'header'

    def test_tag_list(self):
        self.app.add_url_rule('/example', view_func=user_with_tag, methods=['GET', 'HEAD'])

        parser = DocParser(self.app, self.app.url_map._rules[1])

        openapi = OpenApiGenerator()
        openapi.add(parser)

        openapi = openapi.generate()

        output = json.dumps(openapi, cls=CustomEncoder)
        schema = json.loads(output)

        assert 'tags' in schema
        assert schema['tags'] == ['user']

        assert 'paths' in schema.keys()
        assert '/example' in schema['paths'].keys()
        assert 'get' in schema['paths']['/example'].keys()
        assert 'tags' in schema['paths']['/example']['get'].keys()
        assert schema['paths']['/example']['get']['tags'] == ['user']

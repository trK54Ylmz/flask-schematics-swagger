from fss.parser import DocParser
from fss.schema.rule import DocRuleType
from test.schema import UserSuccessResponse, UserErrorResponse, UserModel


class TestDocParser:
    def test_single_line_summary(self):
        summary = 'Lorem Ipsum is simply dummy text of the printing'

        doc = f'''
        {summary}

        :return: flask response
        '''

        parser = DocParser(doc)
        schema = parser.parse()

        assert schema.summary == summary

    def test_multi_line_summary(self):
        summary = 'Lorem Ipsum is simply dummy.\nText of the printing.'

        doc = f'''
        {summary}

        :return: flask response
        '''

        parser = DocParser(doc)
        schema = parser.parse()

        assert schema.summary == summary

    def test_single_line_description(self):
        description = 'Lorem Ipsum is simply dummy text of the printing'

        doc = f'''
        Example title

        {description}

        :return: flask response
        '''

        parser = DocParser(doc)
        schema = parser.parse()

        assert schema.description == description

    def test_simple_response(self):
        doc = '''
        Example

        Example

        :response 200 test.schema.UserSuccessResponse: successful response
        :response 403 test.schema.UserErrorResponse: error response
        '''

        parser = DocParser(doc)
        schema = parser.parse()

        assert schema.responses[0].kind == DocRuleType.RESPONSE
        assert schema.responses[0].status_code == 200
        assert schema.responses[0].model == UserSuccessResponse
        assert schema.responses[0].model_name == 'test.schema.UserSuccessResponse'
        assert schema.responses[1].kind == DocRuleType.RESPONSE
        assert schema.responses[1].status_code == 403
        assert schema.responses[1].model == UserErrorResponse
        assert schema.responses[1].model_name == 'test.schema.UserErrorResponse'

    def test_simple_parameter(self):
        doc = '''
        Example

        Example

        :parameter query integer user_id: the user id filter. default: None
        :parameter body test.schema.UserModel user: the user model
        '''

        parser = DocParser(doc)
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
        assert schema.parameters[1].type == UserModel
        assert schema.parameters[1].description == 'the user model'
        assert schema.parameters[1].default is None

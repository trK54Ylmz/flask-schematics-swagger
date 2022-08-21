from fss.schema import DocSchema


class DocSchemaGeneator:
    def __init__(self, schema: DocSchema) -> None:
        self.schema = schema

    def generate(self) -> dict:
        parameters = []
        responses = dict()

        for p in self.schema.parameters:
            parameter = {
                'name': p.name,
                'in': p.in_name,
                'type': p.type_name,
                '__type__': p.type,
                'description': p.description,
                'default': None if p.default == 'null' else p.default,
            }
            parameters.append(parameter)

        for r in self.schema.responses:
            response = {
                'description': r.description,
                '__type__': r.model,
                '__name__': r.model_name,
            }
            responses[r.status_code] = response

        body = dict()
        body['operationId'] = self.schema.name
        body['summary'] = self.schema.summary
        body['description'] = self.schema.description
        body['parameters'] = parameters
        body['responses'] = responses

        method = dict()
        method[self.schema.method.lower()] = body

        schema = dict()
        schema[self.schema.url] = method

        return schema

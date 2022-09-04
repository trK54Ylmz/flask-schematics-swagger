from .parameter import OpenApiParameterSchema
from .response import OpenApiResponseSchema
from schematics import Model
from schematics.types import DictType, ListType, ModelType, StringType


class OpenApiRouteSchema(Model):
    summary = StringType()
    description = StringType()
    tags = ListType(StringType())
    operation_id = StringType(serialized_name='operationId')
    parameters = ListType(ModelType(OpenApiParameterSchema))
    responses = DictType(ModelType(OpenApiResponseSchema))

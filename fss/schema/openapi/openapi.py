from .definition import OpenApiDefinitionSchema
from .info import OpenApiInfoSchema
from .method import OpenApiMethodSchema
from schematics import Model
from schematics.types import ModelType, ListType, DictType, StringType


class OpenApiSchema(Model):
    info = ModelType(OpenApiInfoSchema)
    swagger = StringType(default='2.0')
    consumes = ListType(StringType)
    produces = ListType(StringType)
    paths = DictType(ModelType(OpenApiMethodSchema))
    definitions = DictType(ModelType(OpenApiDefinitionSchema))

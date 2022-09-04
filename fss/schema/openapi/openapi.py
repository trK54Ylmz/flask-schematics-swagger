from .definition import OpenApiDefinitionSchema
from .info import OpenApiInfoSchema
from .method import OpenApiMethodSchema
from .security import OpenApiSecurityDefinitionSchema
from schematics import Model
from schematics.types import ModelType, ListType, DictType, StringType


class OpenApiSchema(Model):
    info = ModelType(OpenApiInfoSchema)
    swagger = StringType(default='2.0')
    consumes = ListType(StringType)
    produces = ListType(StringType)
    tags = ListType(StringType)
    paths = DictType(ModelType(OpenApiMethodSchema))
    base_path = StringType(serialized_name='basePath')
    definitions = DictType(ModelType(OpenApiDefinitionSchema))
    security = ListType(DictType(ListType(StringType)))
    security_definition = DictType(
        ModelType(OpenApiSecurityDefinitionSchema),
        serialized_name='securityDefinitions',
    )

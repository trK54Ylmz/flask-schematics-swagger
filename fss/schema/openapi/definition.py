from .schema import OpenApiSchemaSchema
from schematics import Model
from schematics.types import DictType, ListType, ModelType, StringType


class OpenApiDefinitionSchema(Model):
    type = StringType()
    required = ListType(StringType())
    properties = DictType(ModelType(OpenApiSchemaSchema))

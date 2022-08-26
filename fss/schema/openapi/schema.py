from .item import OpenApiItemSchema
from schematics import Model
from schematics.types import ModelType, StringType


class OpenApiSchemaSchema(Model):
    type = StringType()
    format = StringType()
    items = ModelType(OpenApiItemSchema)
    ref = StringType(serialized_name='$ref')

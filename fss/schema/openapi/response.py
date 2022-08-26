from .schema import OpenApiSchemaSchema
from schematics import Model
from schematics.types import ModelType, StringType


class OpenApiResponseSchema(Model):
    description = StringType()
    schema = ModelType(OpenApiSchemaSchema)

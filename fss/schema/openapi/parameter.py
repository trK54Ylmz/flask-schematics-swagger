from .schema import OpenApiSchemaSchema
from schematics import Model
from schematics.types import BooleanType, ModelType, StringType


class OpenApiParameterSchema(Model):
    name = StringType()
    description = StringType()
    required = BooleanType()
    type = StringType()
    in_name = StringType(serialized_name='in')
    schema = ModelType(OpenApiSchemaSchema)

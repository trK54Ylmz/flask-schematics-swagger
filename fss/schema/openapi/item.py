from schematics import Model
from schematics.types import StringType


class OpenApiItemSchema(Model):
    type = StringType()
    format = StringType()
    ref = StringType(serialized_name='$ref')

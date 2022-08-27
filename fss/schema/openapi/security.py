from schematics import Model
from schematics.types import StringType


class OpenApiSecurityDefinitionSchema(Model):
    type = StringType()
    name = StringType()
    in_name = StringType(serialized_name='in')

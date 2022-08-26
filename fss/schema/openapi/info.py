from schematics import Model
from schematics.types import StringType


class OpenApiInfoSchema(Model):
    title = StringType()
    version = StringType()
    description = StringType()

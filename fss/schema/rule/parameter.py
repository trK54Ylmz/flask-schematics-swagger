from .rule import DocRuleSchema
from schematics.types import BaseType, StringType


class DocParameterRuleSchema(DocRuleSchema):
    in_name = StringType()
    type = StringType()
    type_name = StringType()
    name = StringType()
    description = StringType()
    default = BaseType(default=None)

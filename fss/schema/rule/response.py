from .rule import DocRuleSchema
from schematics.types import IntType, StringType


class DocResponseRuleSchema(DocRuleSchema):
    status_code = IntType()
    description = StringType()
    type = StringType()
    type_name = StringType()

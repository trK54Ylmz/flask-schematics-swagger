from .rule import DocRuleSchema
from schematics.types import StringType


class DocTagRuleSchema(DocRuleSchema):
    name = StringType()

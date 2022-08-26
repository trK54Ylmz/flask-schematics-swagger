from schematics import Model
from schematics.types import StringType


class DocRuleSchema(Model):
    kind = StringType()

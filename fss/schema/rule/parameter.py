from dataclasses import dataclass
from typing import Any, Optional, Type
from .rule import DocRuleSchema


@dataclass
class DocParameterRuleSchema(DocRuleSchema):
    in_name: str
    type: Type
    type_name: str
    name: str
    description: str
    default: Optional[Any] = None

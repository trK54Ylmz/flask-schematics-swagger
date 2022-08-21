from dataclasses import dataclass
from typing import TypeVar
from .rule import DocRuleSchema
from schematics import Model

T = TypeVar('T', bound=Model)


@dataclass
class DocResponseRuleSchema(DocRuleSchema):
    status_code: int
    description: str
    model_name: str
    model: T

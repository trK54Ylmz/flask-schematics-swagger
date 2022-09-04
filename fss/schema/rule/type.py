from dataclasses import dataclass


@dataclass
class DocRuleType:
    PARAMETER = 'parameter'
    RESPONSE = 'response'
    TAG = 'tag'

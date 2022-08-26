from dataclasses import dataclass


@dataclass(frozen=True)
class Schema:
    PRIMITIVES = ['string', 'float', 'integer', 'boolean']
    STRING = 'string'
    FLOAT = 'float'
    INTEGER = 'integer'
    BOOLEAN = 'boolean'
    NUMBER = 'number'
    OBJECT = 'object'
    ARRAY = 'array'
    NONE = 'none'

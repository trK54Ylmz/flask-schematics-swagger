from dataclasses import dataclass


@dataclass(frozen=True)
class Schema:
    PRIMITIVES = ['string', 'float', 'integer', 'boolean']
    STRING = 'string'
    DATE = 'date'
    DATETIME = 'datetime'
    FLOAT = 'float'
    INTEGER = 'integer'
    BOOLEAN = 'boolean'
    NUMBER = 'number'
    OBJECT = 'object'
    ARRAY = 'array'
    NONE = 'none'

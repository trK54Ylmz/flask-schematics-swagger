from dataclasses import dataclass


@dataclass(frozen=True)
class Method:
    GET = 'get'
    POST = 'post'
    DELETE = 'delete'

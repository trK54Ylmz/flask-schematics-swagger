from dataclasses import dataclass


@dataclass(frozen=True)
class Method:
    GET = 'get'
    POST = 'post'
    PATCH = 'path'
    DELETE = 'delete'

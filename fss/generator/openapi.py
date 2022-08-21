from typing import List, Optional

from fss.parser import DocParser
from fss.schema import DocSchema


class OpenApiGenerator:
    def __init__(
        self,
        host: Optional[str] = None,
        version: Optional[str] = None,
        base_path: Optional[str] = None,
        route: Optional[str] = None,
    ) -> None:
        self.host = host
        self.version = version
        self.route = route
        self.base_path = base_path
        self.schemas: List[DocSchema] = []

    def add(self, parser: DocParser) -> None:
        # parse function document
        schema = parser.parse()
        if schema is None:
            return

        self.schemas.append(schema)

    def generate(self) -> None:
        pass

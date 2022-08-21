from typing import List, Optional
from .schema import DocSchemaGeneator


class OpenApiGenerator:
    def __init__(
        self,
        host: Optional[str] = None,
        version: Optional[str] = None,
        route: Optional[str] = None,
    ) -> None:
        self.host = host
        self.version = version
        self.route = route
        self.schemas: List[DocSchemaGeneator] = []

    def add(self, schema: DocSchemaGeneator) -> None:
        schema.generate()

    def generate(self) -> None:
        pass

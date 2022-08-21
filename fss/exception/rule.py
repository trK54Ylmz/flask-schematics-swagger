class RuleException(Exception):
    definition: str

    def __init__(self, definition: str, *args: object) -> None:
        self.definition = definition

        super().__init__(*args)

    def __str__(self) -> str:
        return f'Invalid rule definition "{self.definition}"'

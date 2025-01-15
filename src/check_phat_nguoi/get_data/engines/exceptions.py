class ParsingDataWhileGettingDataException(Exception):
    def __init__(
        self, message: str = "Error when parsing data while getting data"
    ) -> None:
        super().__init__(message)
        self.message: str = message

    def __str__(self) -> str:
        return self.message

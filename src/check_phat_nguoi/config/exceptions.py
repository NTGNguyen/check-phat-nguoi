class NoConfigFoundException(Exception):
    def __init__(self, message: str = "No config file found") -> None:
        super().__init__(message)
        self.message: str = message

    def __str__(self) -> str:
        return self.message

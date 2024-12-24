from check_phat_nguoi.models.context import ContextModel


class Context:
    def __init__(self) -> None:
        self._context: ContextModel = ContextModel()

    # TODO: Lam di Nguyen hehe
    def insert_data(self, data) -> None:
        pass


__all__ = ["Context"]

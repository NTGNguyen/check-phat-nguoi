from check_phat_nguoi.models.context import ContextModel
from check_phat_nguoi.utils.singleton import Singleton


class Context(Singleton):
    def __init__(self) -> None:
        self._context: ContextModel = ContextModel()

    # TODO: Lam di Nguyen hehe
    def insert_data(self, data) -> None:
        pass


context: Context = Context()


__all__ = ["Context", "context"]

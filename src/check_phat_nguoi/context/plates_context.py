from check_phat_nguoi.models.context import PlatesContextModel
from check_phat_nguoi.utils.singleton import Singleton


class PlatesContext(Singleton, PlatesContextModel):
    # TODO: Lam di Nguyen hehe
    def insert_data(self, data) -> None:
        pass


plates_context: PlatesContext = PlatesContext()


__all__ = ["PlatesContext", "plates_context"]

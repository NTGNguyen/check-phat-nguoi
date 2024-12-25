from check_phat_nguoi.models.context import PlatesContextModel
from check_phat_nguoi.utils.singleton import Singleton


class PlatesContext(Singleton, PlatesContextModel):
    pass


plates_context: PlatesContext = PlatesContext()


__all__ = ["PlatesContext", "plates_context"]

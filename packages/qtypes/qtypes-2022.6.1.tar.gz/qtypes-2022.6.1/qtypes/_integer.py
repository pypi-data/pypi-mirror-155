__all__ = ["Integer"]


from ._base import Base


class Integer(Base):
    qtype = "integer"

    def __init__(self, label: str = "", value=0, minimum=-1e6, maximum=1e6, disabled=False):
        super().__init__(label=label, value=value, disabled=disabled)
        self._data["minimum"] = minimum
        self._data["maximum"] = maximum

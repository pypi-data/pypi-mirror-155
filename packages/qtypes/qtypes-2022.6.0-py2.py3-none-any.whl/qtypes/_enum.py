__all__ = ["Enum"]


from typing import Any, Dict

from ._base import Base


class Enum(Base):
    qtype = "enum"

    def __init__(self, label: str = "", value="", allowed=[""], disabled=False):
        super().__init__(label=label, value=value, disabled=disabled)
        self._data["allowed"] = allowed

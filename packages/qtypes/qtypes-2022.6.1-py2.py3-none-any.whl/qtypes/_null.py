__all__ = ["Null"]


from typing import Any, Dict

from ._base import Base


class Null(Base):
    qtype = "null"

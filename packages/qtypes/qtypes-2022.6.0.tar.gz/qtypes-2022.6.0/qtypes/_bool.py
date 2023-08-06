__all__ = ["Bool"]


from ._base import Base


class Bool(Base):
    qtype = "bool"

    def __init__(self, label: str = "", value=False, disabled=False):
        super().__init__(label=label, value=value, disabled=disabled)

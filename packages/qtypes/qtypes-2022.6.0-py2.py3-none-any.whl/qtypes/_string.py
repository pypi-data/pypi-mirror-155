__all__ = ["String"]


from ._base import Base


class String(Base):
    qtype = "string"

    def __init__(self, label: str = "", value="", disabled=False):
        super().__init__(label=label, value=value, disabled=disabled)

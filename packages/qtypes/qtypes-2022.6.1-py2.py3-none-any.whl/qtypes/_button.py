__all__ = ["Button"]


from typing import Any, Dict

from ._base import Base


class Button(Base):
    qtype = "button"

    def __init__(
        self,
        label: str = "",
        value=None,
        background_color=None,
        text="button",
        text_color=None,
        disabled=False,
    ):
        super().__init__(label=label, value=value, disabled=disabled)
        self._data["text"] = text
        self._data["text_color"] = text_color
        self._data["background_color"] = background_color

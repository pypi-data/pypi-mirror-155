__all__ = ["Float"]


import math
from dataclasses import dataclass
from typing import Any, Dict

from ._base import Base
from ._units import converter, get_valid_conversions


class Float(Base):
    qtype = "float"

    def __init__(
        self,
        label: str = "",
        value=float("nan"),
        units=None,
        minimum=float("-inf"),
        maximum=float("+inf"),
        decimals=6,
        disabled=False,
    ):
        super().__init__(label=label, value=value, disabled=disabled)
        self._data["units"] = units
        self._data["minimum"] = minimum
        self._data["maximum"] = maximum
        self._data["decimals"] = decimals

    @property
    def allowed_units(self):
        out = []
        for i in range(self._widget.combo_box.count()):
            out.append(self._widget.combo_box.itemText(i))
        return out

    def set(self, data: dict, *, from_widget=False):
        if all([self._data[k] == data[k] for k in data.keys()]):
            return
        if "units" in data:
            if not "value" in data:
                data["value"] = converter(self._data["value"], self._data["units"], data["units"])
            if not "minimum" in data:
                data["minimum"] = converter(
                    self._data["minimum"], self._data["units"], data["units"]
                )
            if not "maximum" in data:
                data["maximum"] = converter(
                    self._data["maximum"], self._data["units"], data["units"]
                )
            data["minimum"], data["maximum"] = [
                sort(data["minimum"], data["maximum"]) for sort in [min, max]
            ]
        self._data.update(data)
        for cb in self._updated_callbacks:
            cb(self._data)
        if from_widget:
            for cb in self._edited_callbacks:
                cb(self._data)

__all__ = ["Base"]


import collections
import collections.abc
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, List

import qtpy
from qtpy import QtCore, QtGui, QtWidgets


class Base(collections.abc.MutableSequence):
    qtype = "base"

    def __init__(self, label="", value=None, disabled=False):
        self._data = dict()
        self._data["value"] = value
        self._data["disabled"] = disabled
        self._data["label"] = label
        self.children = []
        self._updated_callbacks = []
        self._edited_callbacks = []
        self._restructured_callbacks = []
        self._suppress_restructure_callbacks = False

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.children[index]
        elif isinstance(index, str):
            for child in self.children:
                if child.get()["label"] == index:
                    return child
            raise KeyError(f"{index} not found in children of {self}")
        else:
            raise Exception(f"{index} invalid argument to __getitem__")

    def __setitem__(self, index, item):
        assert isinstance(index, int)
        self.children[index] = item
        self._restructured_emit()

    def __len__(self):
        return len(self.children)

    def __delitem__(self, index):
        assert isinstance(index, int)
        del self.children[index]
        self._restructured_emit()

    def __contains__(self, item):
        return item in self.children or item in self.keys()

    def clear(self):
        while self.children:
            self.children.pop(0)
        self._restructured_emit()

    def edited_connect(self, function):
        self._edited_callbacks.append(function)

    def edited_disconnect(self, function):
        idx = self._edited_callbacks.index(function)
        self._edited_callbacks.pop(idx)

    def _edited_emit(self):
        for cb in self._edited_callbacks:
            cb(self._data)

    def insert(self, index, item):
        self.children.insert(index, item)
        item.restructured_connect(self._restructured_emit)
        self._restructured_emit()

    def items(self):
        return collections.abc.ItemsView(list(zip(self.keys(), self.children)))

    def keys(self):
        return collections.abc.KeysView([c.get()["label"] for c in self.children])

    def get(self) -> dict:
        return self._data

    def get_value(self) -> object:
        return self._data["value"]

    def pop(self, index=-1):
        try:
            return super().pop(index)
        except AssertionError:
            return super().pop(self.index(self[index]))

    def popitem(self, item):
        return super().pop(self.index(item))

    def restructured_connect(self, function):
        self._restructured_callbacks.append(function)

    def restructured_disconnect(self, function):
        self._restructured_callbacks.pop(function)

    def _restructured_emit(self):
        if not self._suppress_restructure_callbacks:
            for cb in self._restructured_callbacks:
                cb()

    @contextmanager
    def suppress_restructured(self):
        self._suppress_restructure_callbacks = True
        yield
        self._suppress_restructure_callbacks = False
        self._restructured_emit()

    def set(self, value: dict, *, from_widget=False):
        # TODO: diff check
        self._data.update(value)
        self._updated_emit()
        if from_widget:
            self._edited_emit()

    def set_value(self, value: object):
        self.set({"value": value})

    def updated_connect(self, function):
        self._updated_callbacks.append(function)

    def updated_disconnect(self, function):
        idx = self._updated_callbacks.index(function)
        self._updated_callbacks.pop(idx)

    def _updated_emit(self):
        for cb in self._updated_callbacks:
            cb(self._data)

    def values(self):
        return collections.abc.ValuesView(self.children)

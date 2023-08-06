_all__ = ["TreeWidget"]


import sys
import pathlib
import collections
from dataclasses import dataclass

from qtpy import QtWidgets, QtGui, QtCore

from .._base import Base
from .._styles import styles
from ._bool import Widget as BoolWidget
from ._null import Widget as NullWidget
from ._button import Widget as ButtonWidget
from ._enum import Widget as EnumWidget
from ._float import Widget as FloatWidget
from ._integer import Widget as IntegerWidget
from ._string import Widget as StringWidget


__here__ = pathlib.Path(__file__).parent


widgets = dict()
widgets["bool"] = BoolWidget
widgets["null"] = NullWidget
widgets["button"] = ButtonWidget
widgets["enum"] = EnumWidget
widgets["float"] = FloatWidget
widgets["integer"] = IntegerWidget
widgets["string"] = StringWidget


class TreeStructureNode(collections.abc.Sequence):
    def __init__(self, model, tree_widget, parent=None, root=False):
        self.model = model
        self.parent = parent
        self.tree_widget = tree_widget
        self.root = root
        self.label = self.model.get()["label"]
        self.children = []

        if self.root:
            self.item = self.tree_widget.invisibleRootItem()
        elif self.parent is None and not self.tree_widget.include_root:
            pass
        else:
            self.item = QtWidgets.QTreeWidgetItem([self.model.get()["label"], ""])
            self.widget = widgets[model.qtype](parent=self.tree_widget, model=self.model)
            self.parent.item.addChild(self.item)
            self.tree_widget.setItemWidget(self.item, 1, self.widget)
            self.tree_widget.resizeColumnToContents(0)

        for m in self.model:
            self.append(TreeStructureNode(model=m, tree_widget=self.tree_widget, parent=self))

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.children[index]
        elif isinstance(index, str):
            for child in self.children:
                if child.label == index:
                    return child
            raise KeyError(f"{index} not found in children of {self}")
        else:
            raise Exception(f"{index} invalid argument to __getitem__")

    def __len__(self):
        return len(self.children)

    def __delitem__(self, index):
        assert isinstance(index, int)
        del self.children[index]
        self._restructured_emit()

    def append(self, child):
        self.children.append(child)

    def clear(self):
        while self.children:
            self.pop(0)

    def collapse(self, depth=0):
        self.item.setExpanded(False)
        if depth > 0:
            for child in self.children:
                child.expand(depth=depth - 1)

    def expand(self, depth=10):
        self.item.setExpanded(True)
        if depth > 0:
            for child in self.children:
                child.expand(depth=depth - 1)

    def pop(self, pos):
        child = self.children.pop(pos)
        self.item.takeChild(pos)
        #
        todo = [child]
        for node in todo:
            todo += node.children
            node.widget.disconnect()


class TreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, model, *, include_root=True):
        width = 250
        super().__init__(parent=None)
        self.setColumnCount(2)
        self.setHeaderLabels(["", ""])
        sheets = list(styles["tomorrow-night"].values())
        self.setStyleSheet("".join(sheets))
        self.setColumnWidth(width // 2, width // 2)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.model = model
        self.include_root = include_root
        self.model.restructured_connect(self._on_restructured)
        self.structure = TreeStructureNode(
            model=self.model, tree_widget=self, parent=None, root=True
        )

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.structure.children[index]
        elif isinstance(index, str):
            for child in self.structure.children:
                if child.label == index:
                    return child
            raise KeyError(f"{index} not found in children of {self}")
        else:
            raise Exception(f"{index} invalid argument to __getitem__")

    def __len__(self) -> int:
        return len(self.structure)

    def append(self, item):
        self.addTopLevelItem(item)
        if isinstance(item, Base):
            widget = item._widget
            widget.setParent(self)
            self.setItemWidget(item, 1, widget)

    def clear(self):
        while self.topLevelItemCount():
            item = self.takeTopLevelItem(0)
        while self.item_widgets:
            w = self.item_widgets.pop()
            w.disconnect()

    def insert(self, index, item):
        if index < 0:
            index += self.topLevelItemCount()
        if index < 0:
            index = 0
        if index > self.topLevelItemCount():
            index = self.topLevelItemCount()
        self.insertTopLevelItem(index, item)
        if isinstance(item, Base):
            widget = item._widget
            widget.setParent(self)
            self.setItemWidget(item, 1, widget)

    def _on_restructured(self):
        @dataclass
        class Task:
            model: object
            structure_node: object

        todo = [Task(model=self.model, structure_node=self.structure)]

        while todo:
            task = todo.pop()
            try:
                # TODO: this could be better?
                #       for example, if the model is simply appended to
                #       all of the sibling nodes will be remade
                #       when they could just append
                #       something to think about if performance ends up mattering
                #       ---Blaise 2022-06-15
                assert len(task.model) == len(task.structure_node)
                for m, s in zip(task.model.children, task.structure_node.children):
                    assert m == s.model
                for m, s in zip(task.model.children, task.structure_node.children):
                    todo.append(Task(model=m, structure_node=s))
            except AssertionError:
                task.structure_node.clear()
                for m in task.model.children:
                    task.structure_node.append(
                        TreeStructureNode(model=m, tree_widget=self, parent=task.structure_node)
                    )

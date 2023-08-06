"""Example of an interface to typical daemons on the Wright Group fs system"""


import sys
import functools
import random


import qtypes
from qtpy import QtWidgets, QtGui, QtCore
from qtypes._base import Base


def random_string(n):
    out = ""
    for _ in range(n):
        random_integer = random.randint(97, 97 + 26 - 1)
        flip_bit = random.randint(0, 1)  # Convert to lowercase if the flip bit is on
        random_integer = random_integer - 32 if flip_bit == 1 else random_integer
        out += chr(random_integer)
    return out


def append_inspection_widgets(root):
    # string representing value
    root.append(qtypes.String("value", disabled=True))

    def on_updated(value, item):
        item.set_value(str(value))

    root.updated_connect(functools.partial(on_updated, item=root[0]))
    on_updated(root.get(), root[0])
    # disable checkbox
    root.append(qtypes.Bool("disabled"))

    def on_updated(data, item):
        item.set({"disabled": data["value"]})

    root[1].updated_connect(functools.partial(on_updated, item=root))
    # updated counter
    root.append(qtypes.Integer("updated count", disabled=True))

    def on_updated(_, item):
        item.set_value(item.get_value() + 1)

    root.updated_connect(functools.partial(on_updated, item=root[-1]))
    # edited counter
    root.append(qtypes.Integer("edited count", disabled=True))

    def on_edited(_, item):
        item.set_value(item.get_value() + 1)

    root.edited_connect(functools.partial(on_edited, item=root[-1]))


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("one of each")

        self.root_item = qtypes.Null(label="")
        self.root_item.append(qtypes.Bool("bool"))
        self.root_item.append(qtypes.Button("button"))
        self.root_item.append(qtypes.Enum("enum", value="red", allowed=["red", "blue", "green"]))
        self.root_item.append(qtypes.Float("float"))
        self.root_item.append(
            qtypes.Float("float with units", units="nm", minimum=400, maximum=800)
        )
        self.root_item.append(qtypes.Integer("integer"))
        self.root_item.append(qtypes.String("string"))
        for child in self.root_item.children:
            append_inspection_widgets(child)

        self.root_item.append(qtypes.Button("change all programmatically"))
        self.root_item[-1].updated_connect(self.change_all)
        self.root_item.append(qtypes.Bool("update every second"))
        self.root_item[-1].updated_connect(self.toggle_timer)

        self.tree_widget = qtypes.TreeWidget(self.root_item)
        self.tree_widget.expandAll()
        self.tree_widget.resizeColumnToContents(0)
        self.setCentralWidget(self.tree_widget)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.change_all)
        self.timer.setInterval(1000)

    def change_all(self, _=None):
        # bool
        self.root_item[0].set_value(not self.root_item[0].get_value())
        # button
        # TODO:
        # enum
        current = self.root_item[2].get()
        new_index = (current["allowed"].index(current["value"]) + 1) % len(current["allowed"])
        self.root_item[2].set_value(current["allowed"][new_index])
        # float
        self.root_item[3].set_value(random.uniform(-100, 100))
        fl = self.root_item[4]
        val = fl.get()
        fl.set_value(random.uniform(val["minimum"], val["maximum"]))
        # integer
        self.root_item[5].set_value(random.randrange(-100, 100))
        # string
        length = random.randint(5, 30)
        self.root_item[6].set_value(random_string(length))

    def toggle_timer(self, toggle):
        if toggle["value"]:
            self.timer.start()
        else:
            self.timer.stop()


def one_of_each():
    app = QtWidgets.QApplication(sys.argv)
    widget = MyMainWindow()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    one_of_each()

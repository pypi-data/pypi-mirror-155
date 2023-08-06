from qtpy import QtWidgets, QtGui, QtCore


class Widget(QtWidgets.QWidget):
    def __init__(self, model, parent):
        super().__init__(parent=parent)
        self.model = model

    def disconect(self):
        pass

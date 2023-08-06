from qtpy import QtWidgets, QtGui, QtCore


class Widget(QtWidgets.QPushButton):
    def __init__(self, model, parent):
        super().__init__(parent=parent)
        self.clicked.connect(self.on_clicked_connect)
        # wire into model
        self.model = model
        self.model.updated_connect(self.on_updated)
        self.on_updated(model.get())

    def disconnect(self):
        self.model.updated_disconnect(self.on_updated)

    def on_clicked_connect(self):
        # TODO: better
        self.model._updated_emit()
        self.model._edited_emit()

    def on_updated(self, data):
        self.setText(data["text"])
        self.setDisabled(data["disabled"])

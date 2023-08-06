from qtpy import QtWidgets, QtGui, QtCore


class Widget(QtWidgets.QLineEdit):
    def __init__(self, model, parent):
        super().__init__(parent=parent)
        self.editingFinished.connect(self.on_editing_finished)
        # wire into model
        self.model = model
        self.model.updated_connect(self.on_updated)
        self.on_updated(model.get())

    def disconnect(self):
        self.model.updated_disconnect(self.on_updated)

    def on_editing_finished(self):
        self.model.set({"value": self.text()}, from_widget=True)

    def on_updated(self, data):
        if not self.hasFocus():
            self.setText(data["value"])
            self.setDisabled(data["disabled"])

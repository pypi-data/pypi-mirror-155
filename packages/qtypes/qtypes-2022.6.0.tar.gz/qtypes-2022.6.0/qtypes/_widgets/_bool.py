from qtpy import QtWidgets, QtGui, QtCore


class Widget(QtWidgets.QCheckBox):
    def __init__(self, model, parent):
        super().__init__(parent=parent)
        self.stateChanged.connect(self.on_state_changed)
        # wire into model
        self.model = model
        self.model.updated_connect(self.on_updated)
        self.on_updated(model.get())

    def disconnect(self):
        self.model.updated_disconnect(self.on_updated)

    def on_state_changed(self, new):
        self.model.set({"value": bool(new)}, from_widget=True)

    def on_updated(self, data):
        self.stateChanged.disconnect(self.on_state_changed)
        self.setChecked(data["value"])
        self.setDisabled(data["disabled"])
        self.stateChanged.connect(self.on_state_changed)

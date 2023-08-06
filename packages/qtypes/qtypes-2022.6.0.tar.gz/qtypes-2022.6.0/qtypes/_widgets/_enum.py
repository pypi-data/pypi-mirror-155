from qtpy import QtWidgets, QtGui, QtCore


class Widget(QtWidgets.QComboBox):
    def __init__(self, model, parent):
        super().__init__(parent=parent)
        self.currentTextChanged.connect(self.on_current_text_changed)
        # wire into model
        self.model = model
        self.model.updated_connect(self.on_updated)
        self.on_updated(model.get())

    def disconnect(self):
        self.model.updated_disconnect(self.on_updated)

    def on_current_text_changed(self, new):
        self.model.set({"value": new}, from_widget=True)

    def on_updated(self, data):
        self.currentTextChanged.disconnect(self.on_current_text_changed)

        if not data["allowed"]:
            # If now allowed values are given, reset to default
            data["allowed"] = self.defaults["allowed"]

        # allowed
        all_items = [self.itemText(i) for i in range(self.count())]
        if data["allowed"] != all_items:
            self.clear()
            self.addItems(data["allowed"])
        # value
        if data["value"] not in data["allowed"]:
            data["value"] = data["allowed"][0]
        index = data["allowed"].index(data["value"])
        self.setCurrentIndex(index)

        self.currentTextChanged.connect(self.on_current_text_changed)

        self.setDisabled(data["disabled"])

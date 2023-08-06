import math

from qtpy import QtWidgets, QtGui, QtCore

from .._units import converter, get_valid_conversions


class Widget(QtWidgets.QWidget):
    def __init__(self, model, parent):
        super().__init__(parent=parent)
        # build widget
        self.setLayout(QtWidgets.QHBoxLayout())
        self.spin_box = QtWidgets.QDoubleSpinBox()
        self.layout().addWidget(self.spin_box)
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.setFixedWidth(100)
        self.combo_box.hide()  # will get shown if units are set
        self.layout().addWidget(self.combo_box)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.spin_box.editingFinished.connect(self.on_spin_box_editing_finished)
        self.combo_box.currentIndexChanged.connect(self.on_combo_box_editing_finished)
        # wire into model
        self.model = model
        self.model.updated_connect(self.on_updated)
        self.on_updated(model.get())

    def disconnect(self):
        self.model.updated_disconnect(self.on_updated)

    @property
    def allowed_units(self):
        out = []
        for i in range(self.combo_box.count()):
            out.append(self.combo_box.itemText(i))
        return out

    def on_combo_box_editing_finished(self):
        new = self.combo_box.currentText()
        self.model.set({"units": new}, from_widget=True)

    def on_spin_box_editing_finished(self):
        self.model.set({"value": self.spin_box.value()}, from_widget=True)

    def on_updated(self, data):
        """
        Must recieve complete and self-consistent dictionary.
        Updates state of widget
        """
        # units
        if data["units"] is not None and len(self.allowed_units) == 0:
            self.combo_box.currentIndexChanged.disconnect(self.on_combo_box_editing_finished)
            self.combo_box.addItems(get_valid_conversions(data["units"]))
            self.combo_box.currentIndexChanged.connect(self.on_combo_box_editing_finished)
        if data["units"] is not None:
            self.combo_box.show()
            self.combo_box.currentIndexChanged.disconnect(self.on_combo_box_editing_finished)
            self.combo_box.setCurrentIndex(self.allowed_units.index(data["units"]))
            self.combo_box.currentIndexChanged.connect(self.on_combo_box_editing_finished)
        # minimum, maximum
        self.spin_box.setMinimum(data["minimum"])
        self.spin_box.setMaximum(data["maximum"])
        # tool tip
        self.spin_box.setToolTip(f"minimum:{data['minimum']}\nmaximum:{data['maximum']}")
        if not self.spin_box.hasFocus():
            # decimals
            self.spin_box.setDecimals(data["decimals"])
            # value
            if math.isnan(data["value"]):
                self.spin_box.setSpecialValueText("nan")
                self.spin_box.setValue(self.spin_box.minimum())
            else:
                self.spin_box.setSpecialValueText("")
                self.spin_box.setValue(data["value"])
        # disabled
        self.setDisabled(data["disabled"])

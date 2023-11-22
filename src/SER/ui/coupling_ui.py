from typing import Collection

from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QSpinBox
from lantz.qt.connect import connect_feat

from .localization import localizator
from ..interfaces import ComponentInitialization, ConfigurableInstrument


class CouplingUI(QGroupBox):

    def __init__(self, config_componentes: Collection[ComponentInitialization]):
        super().__init__()
        self.setTitle(localizator.get("coupling"))
        layout = QGridLayout()
        self.setLayout(layout)

        self.labels = []
        self.sboxes = []

        y = 0
        for comp in config_componentes:
            # TODO: rethink this shit
            if not isinstance(comp.component.instrument, ConfigurableInstrument):
                continue

            label = QLabel(comp.name)
            layout.addWidget(label, y, 0)
            self.labels.append(label)

            spin_box = QSpinBox()
            spin_box.setRange(-10000, +10000)
            spin_box.setValue(comp.component.instrument.coupling)
            spin_box.valueChanged.connect(comp.component.instrument.set_coupling)
            layout.addWidget(spin_box, y, 1)
            self.sboxes.append(spin_box)

            y += 1

import json
from os import path
from typing import Collection, List

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog, QLabel, QPushButton, QFileDialog, QDialogButtonBox

from .localization import localizator
from ..interfaces import ComponentInitialization
from ..model.sequencer import ExperimentSequencer


class ComponentConfigWidget(QWidget):
    name_label: QLabel
    save_button: QPushButton
    load_button: QPushButton
    component: ComponentInitialization

    def __init__(self, component: ComponentInitialization, folder="."):
        super().__init__()

        # This loads the file and loads up each object as part of this class
        # When using this method it's important to not overlap names with the widget
        # as the class will put the widgets as direct attributes of MainWidget
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "component_configuration.ui")
        uic.loadUi(ui_file_path, self)

        self.component = component
        self.folder = folder
        self.name_label.setText(f"{component.component.__class__.__name__}: {component.name}")
        self.load_button.pressed.connect(self.load_configuration)
        self.save_button.pressed.connect(self.save_configuration)

        # Text
        self.load_button.setText(localizator.get("load_configuration"))
        self.save_button.setText(localizator.get("save_configuration"))

    def load_configuration(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.folder)
        file_name, _ = file_dialog.getOpenFileName(self, "Open File", "",
                                                   "JavaScript Object Notation (*.json);;All Files (*)", options=options)

        if file_name:
            with open(file_name, "r+") as file:
                self.component.component.instrument.set_config(json.load(file))

    def save_configuration(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.folder)
        file_name, _ = file_dialog.getSaveFileName(self, "Save File", "",
                                                   "JavaScript Object Notation (*.json);;All Files (*)", options=options)

        if file_name:
            config = self.component.component.instrument.get_config()
            with open(file_name, "w+") as file:
                json.dump(config, file)


class ComponentsDialog(QDialog):
    components_layout: QVBoxLayout
    components_widgets: dict[str, ComponentConfigWidget]
    load_run_button: QPushButton
    save_run_button: QPushButton
    load_sequence_button: QPushButton
    save_sequence_button: QPushButton
    button_box: QDialogButtonBox

    def __init__(self, sequencer: ExperimentSequencer, components: Collection[ComponentInitialization], folder="."):
        super().__init__()

        # This loads the file and loads up each object as part of this class
        # When using this method it's important to not overlap names with the widget
        # as the class will put the widgets as direct attributes of MainWidget
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "components_dialog.ui")
        uic.loadUi(ui_file_path, self)

        self.folder = folder
        self.sequencer = sequencer

        self.components_widgets = {}
        for component in components:
            self.components_widgets[component.name] = ComponentConfigWidget(component, folder)
            self.components_layout.addWidget(self.components_widgets[component.name])

        self.load_run_button.pressed.connect(self.load_run_configuration)
        self.save_run_button.pressed.connect(self.save_run_configuration)
        self.load_sequence_button.pressed.connect(self.load_sequence)
        self.save_sequence_button.pressed.connect(self.save_sequence)

        # Text
        self.load_run_button.setText(localizator.get("load_run"))
        self.save_run_button.setText(localizator.get("save_run"))
        self.load_sequence_button.setText(localizator.get("load_sequence"))
        self.save_sequence_button.setText(localizator.get("save_sequence"))

    def load_run_configuration(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.folder)
        file_name, _ = file_dialog.getOpenFileName(self, "Open File", "",
                                                   "JavaScript Object Notation (*.json);;All Files (*)", options=options)

        if file_name:
            with open(file_name, "r+") as file:
                configs = json.load(file)
                for name, comp_w in configs.items():
                    self.components_widgets[name].component.component.instrument.set_config(comp_w)

    def save_run_configuration(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.folder)
        file_name, _ = file_dialog.getSaveFileName(self, "Save File", "",
                                                   "JavaScript Object Notation (*.json);;All Files (*)", options=options)

        if file_name:
            with open(file_name, "w+") as file:
                combined_configs = {}
                for name, comp_w in self.components_widgets.items():
                    combined_configs[name] = comp_w.component.component.instrument.get_config()
                json.dump(combined_configs, file)

    def load_sequence(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.folder)
        file_name, _ = file_dialog.getOpenFileName(self, "Open File", "",
                                                   "JavaScript Object Notation (*.json);;All Files (*)", options=options)

        if file_name:
            with open(file_name, "r+") as file:
                self.sequencer.load_sequence(json.load(file))

    def save_sequence(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.folder)
        file_name, _ = file_dialog.getSaveFileName(self, "Save File", "",
                                                   "JavaScript Object Notation (*.json);;All Files (*)", options=options)

        if file_name:
            with open(file_name, "w+") as file:
                json.dump(self.sequencer.sequence, file)

from os import path
from typing import Collection, List
from configparser import ConfigParser

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog, QLabel, QPushButton, QFileDialog, QDialogButtonBox

from .localization import localizator
from ..interfaces import ComponentInitialization


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
                                                   "Configuration File (*.ini);;All Files (*)", options=options)

        if file_name:
            config = ConfigParser()
            config.read(file_name)
            self.component.component.instrument.set_config(config)

    def save_configuration(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.folder)
        file_name, _ = file_dialog.getSaveFileName(self, "Save File", "",
                                                   "Configuration File (*.ini);;All Files (*)", options=options)

        if file_name:
            config = self.component.component.instrument.get_config()
            with open(file_name, "w+") as file:
                config.write(file)


class ComponentsDialog(QDialog):
    components_layout: QVBoxLayout
    components_widgets: List[ComponentConfigWidget]
    button_box: QDialogButtonBox

    def __init__(self, components: Collection[ComponentInitialization], folder="."):
        super().__init__()

        # This loads the file and loads up each object as part of this class
        # When using this method it's important to not overlap names with the widget
        # as the class will put the widgets as direct attributes of MainWidget
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "components_dialog.ui")
        uic.loadUi(ui_file_path, self)

        self.components_widgets = []
        for component in components:
            self.components_widgets.append(ComponentConfigWidget(component))
            self.components_layout.addWidget(self.components_widgets[-1])

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class input_name(QDialog):
    def __init__(self, parent = None):
        super(input_name, self).__init__(parent)

        layout = QGridLayout(self)

        # nice widget for editing the date
        self.input_label = QLabel("Input Parameter")
        self.input_parameter = QLineEdit()

        self.output_label = QLabel("Output Parameter")
        self.output_parameter = QLineEdit()
        
        self.directory_label = QLabel("Choose Data")
        self.directory_parameter = QFileDialog.getOpenFileNames()
        self.directory = ""
        if self.directory_parameter:
            for name in self.directory_parameter:
                self.directory = self.directory + name

        self.learning_rate_label = QLabel("Learning Rate")
        self.learning_rate = QLineEdit()

        self.training_steps_label = QLabel("Training Steps")
        self.training_steps = QLineEdit()

        layout.addWidget(self.input_label, 0, 0)
        layout.addWidget(self.input_parameter, 0, 1)
        layout.addWidget(self.output_label, 1, 0)
        layout.addWidget(self.output_parameter, 1, 1)
        layout.addWidget(self.learning_rate_label, 2, 0)
        layout.addWidget(self.learning_rate, 2, 1)
        layout.addWidget(self.training_steps_label, 3, 0)
        layout.addWidget(self.training_steps, 3, 1)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        self.input = self.input_parameter.text()
        self.output = self.output_parameter.text()
        self.rate = self.learning_rate.text()
        self.step = self.training_steps.text()

        return self.input, self.output, self.directory, self.rate, self.step

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getOutput(parent = None):
        dialog = input_name(parent)
        result = dialog.exec_()
        input_, output_, directory_, rate_, step_ = dialog.getData()
        return (input_, output_, directory_, rate_, step_, result == QDialog.Accepted)

class input_layer(QDialog):
    def __init__(self, parent = None):
        super(input_layer, self).__init__(parent)

        layout = QGridLayout(self)

        self.input_label = QLabel("Layer Name")
        self.input_parameter = QLineEdit()

        self.input_size = QLabel("Layer Size")
        self.size_parameter = QLineEdit()

        self.output_label = QLabel("Activation Function")
        self.output_parameter = QComboBox()
        self.output_parameter.addItem("relu")
        self.output_parameter.addItem("sigmoid")
        self.output_parameter.addItem("tanh")

        layout.addWidget(self.input_label, 0, 0)
        layout.addWidget(self.input_parameter, 0, 1)
        layout.addWidget(self.input_size, 1, 0)
        layout.addWidget(self.size_parameter, 1, 1)
        layout.addWidget(self.output_label, 2, 0)
        layout.addWidget(self.output_parameter, 2, 1)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        self.name = self.input_parameter.text()
        self.size = self.size_parameter.text()
        self.func = self.output_parameter.currentText()
        return self.name, self.size, self.func

    # static method to create the dialog and return
    @staticmethod
    def getOutput(parent = None):
        dialog = input_layer(parent)
        result = dialog.exec_()
        name_, size_, func_= dialog.getData()
        return (name_, size_, func_, result == QDialog.Accepted)
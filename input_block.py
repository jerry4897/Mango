import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class input_name(QDialog):
    def __init__(self, parent = None):
        super(input_name, self).__init__(parent)

        layout = QGridLayout(self)
        newfont = QFont("Arial", 10)

        self.input_label = QLabel("Input Parameter")
        self.input_label.setFont(newfont)
        self.input_parameter = QLineEdit()
        self.input_parameter.setFont(newfont)

        self.output_label = QLabel("Output Parameter")
        self.output_label.setFont(newfont)
        self.output_parameter = QLineEdit()
        self.output_parameter.setFont(newfont)

        self.directory_label = QLabel("Choose Data")
        self.directory_parameter = QFileDialog.getOpenFileNames()
        self.directory = ""
        if self.directory_parameter:
            for name in self.directory_parameter:
                self.directory = self.directory + name

        self.learning_rate_label = QLabel("Learning Rate")
        self.learning_rate_label.setFont(newfont)
        self.learning_rate = QLineEdit()
        self.learning_rate.setFont(newfont)

        self.training_steps_label = QLabel("Training Steps")
        self.training_steps_label.setFont(newfont)
        self.training_steps = QLineEdit()
        self.training_steps.setFont(newfont)

        self.batch_label = QLabel("Batch Size")
        self.batch_label.setFont(newfont)
        self.batch_size = QLineEdit()
        self.batch_size.setFont(newfont)

        self.network = QLabel()
        #self.network.setGeometry(0, 0, 50, 50)
        self.network.setPixmap(QPixmap("mnist_neural_net.png"))
        
        self.learning_rate_pix = QLabel()
        #self.learning_rate_pix.setGeometry(0, 0, 50, 50)
        self.learning_rate_pix.setPixmap(QPixmap("learning_rate.png"))

        layout.addWidget(self.network, 0, 0, 2, 2)
        layout.addWidget(self.input_label, 2, 0)
        layout.addWidget(self.input_parameter, 2, 1)
        layout.addWidget(self.output_label, 3, 0)
        layout.addWidget(self.output_parameter, 3, 1)

        self.empty = QLabel()
        layout.addWidget(self.empty, 4, 0)

        layout.addWidget(self.learning_rate_pix, 5, 0, 1, 2)
        layout.addWidget(self.learning_rate_label, 6, 0)
        layout.addWidget(self.learning_rate, 6, 1)
        layout.addWidget(self.training_steps_label, 7, 0)
        layout.addWidget(self.training_steps, 7, 1)
        layout.addWidget(self.batch_label, 8, 0)
        layout.addWidget(self.batch_size, 8, 1)
        
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
        self.batch = self.batch_size.text()
        return self.input, self.output, self.directory, self.rate, self.step, self.batch

    # static method to create the dialog and return
    @staticmethod
    def getOutput(parent = None):
        dialog = input_name(parent)
        result = dialog.exec_()
        input_, output_, directory_, rate_, step_, batch_ = dialog.getData()
        return (input_, output_, directory_, rate_, step_, batch_, result == QDialog.Accepted)

class input_layer(QDialog):
    def __init__(self, parent = None):
        super(input_layer, self).__init__(parent)

        layout = QGridLayout(self)
        newfont = QFont("Arial", 10, QFont.Bold)

        self.input_label = QLabel("Layer Name")
        self.input_label.setFont(newfont)
        self.input_parameter = QLineEdit()
        self.input_parameter.setFont(newfont)

        self.input_size = QLabel("Layer Size")
        self.input_size.setFont(newfont)
        self.size_parameter = QLineEdit()
        self.size_parameter.setFont(newfont)

        '''self.output_label = QLabel("Activation Function")
        self.output_parameter = QComboBox()
        self.output_parameter.addItem("relu")
        self.output_parameter.addItem("sigmoid")
        self.output_parameter.addItem("tanh")
        '''
        layout.addWidget(self.input_label, 0, 0)
        layout.addWidget(self.input_parameter, 0, 1)
        layout.addWidget(self.input_size, 1, 0)
        layout.addWidget(self.size_parameter, 1, 1)
        
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
        return self.name, self.size

    # static method to create the dialog and return
    @staticmethod
    def getOutput(parent = None):
        dialog = input_layer(parent)
        result = dialog.exec_()
        name_, size_ = dialog.getData()
        return (name_, size_, result == QDialog.Accepted)

class output_layer(QDialog):
    def __init__(self, parent = None):
        super(output_layer, self).__init__(parent)

        layout = QGridLayout(self)
        newfont = QFont("Arial", 10, QFont.Bold)

        self.loss_label = QLabel("Loss Function")
        self.loss_label.setFont(newfont)
        self.loss_parameter = QComboBox()
        self.loss_parameter.addItem("softmax_cross_entropy_with_logits")

        self.optimizer_label = QLabel("Optimizer")
        self.optimizer_label.setFont(newfont)
        self.optimizer_parameter = QComboBox()
        self.optimizer_parameter.addItem("AdamOptimizer")
        self.optimizer_parameter.addItem("GradientDescentOptimizer")
        
        self.display_label = QLabel("Display Step")
        self.display_label.setFont(newfont)
        self.display_parameter = QLineEdit()
        self.display_parameter.setFont(newfont)

        layout.addWidget(self.loss_label, 0, 0)
        layout.addWidget(self.loss_parameter, 0, 1)
        layout.addWidget(self.optimizer_label, 1, 0)
        layout.addWidget(self.optimizer_parameter, 1, 1)
        layout.addWidget(self.display_label, 2, 0)
        layout.addWidget(self.display_parameter, 2, 1)
        
        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        self.loss = self.loss_parameter.currentText()
        self.optimizer = self.optimizer_parameter.currentText()
        self.display = self.display_parameter.text()

        return self.loss, self.optimizer, self.display

    # static method to create the dialog and return
    @staticmethod
    def getOutput(parent = None):
        dialog = output_layer(parent)
        result = dialog.exec_()
        loss_, optimizer_, display_ = dialog.getData()
        return (loss_, optimizer_, display_, result == QDialog.Accepted)

class activation_function(QDialog):
    def __init__(self, parent = None):
        super(activation_function, self).__init__(parent)

        layout = QGridLayout(self)
        newfont = QFont("Arial", 10, QFont.Bold)

        self.activation_label = QLabel("Activation Function")
        self.activation_label.setFont(newfont)
        self.activation_parameter = QLineEdit()
        self.activation_parameter.setFont(newfont)

        self.function_pix = QLabel()
        self.function_pix.setPixmap(QPixmap("activation_function.png"))

        layout.addWidget(self.function_pix, 0, 0, 1, 2)
        layout.addWidget(self.activation_label, 1, 0)
        layout.addWidget(self.activation_parameter, 1, 1)
        
        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        self.activation = self.activation_parameter.text()

        return self.activation

    # static method to create the dialog and return
    @staticmethod
    def getOutput(parent = None):
        dialog = activation_function(parent)
        result = dialog.exec_()
        activation_ = dialog.getData()
        return (activation_, result == QDialog.Accepted)
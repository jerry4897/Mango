import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class input_mode(QDialog):
    def __init__(self, parent = None):
        super(input_mode, self).__init__()
        #layout = QHBoxLayout(self)
        layout = QGridLayout(self)
        self.mode_flag = 1
        self.setWindowTitle("Choose Network Mode")

        self.logo_pix = QLabel()
        self.logo_pix.setPixmap(QPixmap("logo.png"))

        self.mode1 = QRadioButton("Basic Neural Network")
        self.mode1.setChecked(True)
        self.mode1.toggled.connect(lambda:self.btnstate(self.mode1))
        layout.addWidget(self.mode1, 1, 0)

        self.mode2 = QRadioButton("Convolutional Neural Network")
        self.mode2.setChecked(False)
        self.mode2.toggled.connect(lambda:self.btnstate(self.mode2))

        self.mode3 = QRadioButton("Spike Neural Network")
        self.mode3.setChecked(False)
        self.mode3.toggled.connect(lambda:self.btnstate(self.mode2))
        
        layout.addWidget(self.logo_pix, 0, 0, 1, 3)
        layout.addWidget(self.mode2, 1, 1)
        layout.addWidget(self.mode3, 1, 2)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def btnstate(self,b):
	
        if b.text() == "Basic Neural Network":
            if b.isChecked() == True:
                print(b.text()+" is selected")
                self.mode_flag = 1
            else:
                print(b.text()+" is deselected")
				
        if b.text() == "Convolutional Neural Network":
            if b.isChecked() == True:
                print(b.text()+" is selected")
                self.mode_flag = 2
            else:
                print(b.text()+" is deselected")
        
        if b.text() == "Spike Neural Network":
            if b.isChecked() == True:
                print(b.text()+" is selected")
                self.mode_flag = 3
            else:
                print(b.text()+" is deselected")
    
    def getData(self):
        self.mode = self.mode_flag
        
        return self.mode_flag

    # static method to create the dialog and return
    @staticmethod
    def getOutput(parent = None):
        dialog = input_mode(parent)
        result = dialog.exec_()
        flag = dialog.getData()
        return (flag, result == QDialog.Accepted)

class stimulus_epoch(QDialog):
    def __init__(self, parent = None):
        super(stimulus_epoch, self).__init__(parent)

        layout = QGridLayout(self)

        self.stimulus_label = QLabel("Stimulus epoch")
        self.stimulus_parameter = QLineEdit()

        layout.addWidget(self.stimulus_label, 0, 0)
        layout.addWidget(self.stimulus_parameter, 0, 1)
        
        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        self.stimulus = self.stimulus_parameter.text()

        return self.stimulus

    # static method to create the dialog and return
    @staticmethod
    def getOutput(parent = None):
        dialog = stimulus_epoch(parent)
        result = dialog.exec_()
        stimulus_ = dialog.getData()
        return (stimulus_, result == QDialog.Accepted)
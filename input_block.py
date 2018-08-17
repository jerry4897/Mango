import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class input_block(QWidget):                                         # pop up when blocks are dropped to screen,
    def __init__(self, input_flag):                                 # It shows menu that insert the 'name' and 'activation function'. 
        super().__init__()
        self.title = 'Block input'
        self.left = 200
        self.top = 200
        self.width = 640
        self.height = 480
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        if input_flag:
            self.initUI()
        else:
            self.set_input()

        self.first_input
        self.second_input

    def set_input(self):                                                    # for variable_scope
        self.first_input, okPressed = QInputDialog.getText(self, "Input parameter","Input parameter:", QLineEdit.Normal, "")
        if okPressed and self.first_input != '':
            print(self.first_input)
        
        self.second_input, okPressed = QInputDialog.getText(self, "Output parameter","Output parameter:", QLineEdit.Normal, "")
        if okPressed and self.second_input != '':
            print(self.second_input)

    def initUI(self):                                                       # for name_scope(layer)
        self.first_input = self.getName()
        self.second_input = self.getFucntion()
        self.show()

    def getName(self):
        text, okPressed = QInputDialog.getText(self, "Get name","Layer name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
        return text

    def getFucntion(self):
        items = ("Relu","SoftMax")
        item, okPressed = QInputDialog.getItem(self, "Activation Function","Activation Function:", items, 0, False)
        if okPressed and item:
            print(item)
        return item
 
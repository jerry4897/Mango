from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import main

class menu_set(QTableWidget):
    def __init__(self, parent = None):
        super(menu_set, self).__init__()
        self.cellClicked.connect(self.cellClick)
    def cellClick(self, row, col):
        print("Click" + str(row) + " " + str(col))

class menu_init(menu_set):
    def __init__(self):
        super(menu_init, self).__init__()
        self.resize(250, 200)
        self.setRowCount(4)
        self.setColumnCount(2)

        column_headers = ['name', 'shape', 'type', 'connections']
        self.setHorizontalHeaderLabels(column_headers)

        self.setItem(0,0, QTableWidgetItem("Item (1,1)"))
        self.setItem(0,1, QTableWidgetItem("Item (1,2)"))
        self.setItem(1,0, QTableWidgetItem("Item (2,1)"))
        self.setItem(1,1, QTableWidgetItem("Item (2,2)"))
        self.setItem(2,0, QTableWidgetItem("Item (3,1)"))
        self.setItem(2,1, QTableWidgetItem("Item (3,2)"))
        self.setItem(3,0, QTableWidgetItem("Item (4,1)"))
        self.setItem(3,1, QTableWidgetItem("Item (4,2)"))

class menu_block(menu_set):
    def __init__(self, index, shape, connect_list):
        super(menu_block, self).__init__()
        self.resize(250, 200)
        self.setRowCount(4)
        self.setColumnCount(3)

        column_headers = ['index', 'shape', 'connections']
        self.setHorizontalHeaderLabels(column_headers)

        self.setItem(0,0, QTableWidgetItem(str(index)))
        self.setItem(0,1, QTableWidgetItem(str(shape)))
        self.setItem(0,2, QTableWidgetItem(str(connect_list)))

    def edititem(self, item):
        pass

class right_click_table(QWidget):
#    def __init__(self, parent = None):
#        QWidget.__init__(self, parent)
    def __init__(self, block_list):
        super(right_click_table, self).__init__()
        layout = QGridLayout()
        widget = QWidget()

        i = 0
        for block in block_list:
            if(block_list[i].shape == 1):
                layout.addWidget(QCheckBox("rectangle" + " " + str(block_list[i].index), self), i, 0)
            else:
                layout.addWidget(QCheckBox("circle" + " " + str(block.index), self), i, 0)
            i += 1

        self.delete_button = QPushButton("Delete")
        layout.addWidget(self.delete_button, 0, 1)
        widget.setLayout(layout)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(False)
        self.scroll.setWidget(widget)
        
        gLayout = QGridLayout()
        gLayout.addWidget(self.scroll)
        self.setLayout(gLayout)

class load_scene(QGraphicsScene):
    def __init__(self, scene):
        super(load_scene, self).__init__()
        global scen
        scen = scene

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import dropped_blocks

class TableWidget(QTableWidget):
 
    def __init__(self, parent = None):
        QTableWidget.__init__(self, parent)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
         
        quitAction = QAction("Quit", self)
        quitAction.triggered.connect(self.test)
        self.addAction(quitAction)

    def test(self):
        print("wow!")

class mytest(QWidget):
    def __init__(self): 
        super().__init__()
        print("menu start")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # @pyqtSlot('QPoint') 
    @pyqtSlot(QPoint) 
    def __context_menu(self, position): 
        menu = QMenu() 
        copy_action = menu.addAction("복사하기") 
        quit_action = menu.addAction("Quit")
        action = menu.exec_(self.table.mapToGlobal(position)) 
        if action == quit_action:
            qApp.quit() 
        elif action == copy_action: 
            print("copy...") 

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
        '''self.setItem(1,1, QTableWidgetItem("Item (2,2)"))
        self.setItem(2,0, QTableWidgetItem("Item (3,1)"))
        self.setItem(2,1, QTableWidgetItem("Item (3,2)"))
        self.setItem(3,0, QTableWidgetItem("Item (4,1)"))
        self.setItem(3,1, QTableWidgetItem("Item (4,2)"))'''
    def edititem(self, item):
        pass

class load_scene(QGraphicsScene):
    def __init__(self, scene):
        super(load_scene, self).__init__()
        global scen
        scen = scene

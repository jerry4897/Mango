import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import dropped_blocks
import arrow
import menu

#####
click_listen = None
num = 0
#####
block_list = []

class pallete_part(QGraphicsObject):                        # pallete part : right corner of Window.         
    def __init__(self, parent=None):
        super(pallete_part, self).__init__(parent)

        self.color = QColor(Qt.lightGray)
        self.dragOver = True
        self.shape = 0
        self.setAcceptDrops(False)

    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if QLineF(QPointF(event.screenPos()), QPointF(event.buttonDownScreenPos(Qt.LeftButton))).length() < QApplication.startDragDistance():
            return

        drag = QDrag(event.widget())
        mime = QMimeData()
        drag.setMimeData(mime)
        drag.setHotSpot(event.pos().toPoint())
        mime.setText(str(self.shape))

        pixmap = QPixmap(60, 60)
        drag.setHotSpot(QPoint(30, 30))
        if(self.shape == 2):                                    # rec : self.shape == 1
            pixmap = QPixmap(120, 60)                           # cir : self.shape == 2
            drag.setHotSpot(QPoint(100, 30))
       
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)
        painter.translate(0, 0)
        painter.setRenderHint(QPainter.Antialiasing)

        self.paint(painter, None, None)
        painter.end()

        pixmap.setMask(pixmap.createHeuristicMask())
        drag.setPixmap(pixmap)
        drag.exec_()
        self.setCursor(Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
      
class neuron_rec(pallete_part):                                     # rectangular shape of pallete
    def __init__(self, parent=None):
        super(neuron_rec, self).__init__(parent)
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 1                              

    def boundingRect(self):
        return QRectF(0, 0, 60, 60)
    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawRect(0, 0, 60, 60)

class neuron_cir(pallete_part):                                     # circle shape of pallete
    def __init__(self, parent=None):
        super(neuron_cir, self).__init__(parent)
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 2

    def boundingRect(self):
        return QRectF(80, 0, 40, 60)
    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawEllipse(80, 0, 40, 60)

class pallete(pallete_part):                                        # pallete activating part
    def __init__(self):
        super(pallete, self).__init__()

        self.setFlag(self.ItemHasNoContents)

        self.rectangle = neuron_rec(self)                           # activate rectangle button
        self.circle = neuron_cir(self)                              # activate circle button
    def boundingRect(self):
        return QRectF()

    def paint(self, painter, option, widget=None):
        pass

class qgraphicsView(QGraphicsView):                     # Main board Graphic View (Drop zone)
    def __init__(self, scene):
        super(qgraphicsView, self).__init__()
        self.scene = scene
        #gScene = scene
        self.setScene(self.scene)
        self.setAcceptDrops(True)

        arrow.load_scene(self.scene)
        menu.load_scene(self.scene)
    def dragMoveEvent(self, event):
        event.setAccepted(True)

    def dragEnterEvent(self, event):
        event.setAccepted(True)
        self.dragOver = True
        self.dragMoveEvent(event)
        self.update()
            
    def dropEvent(self, event):
        self.dragOver = True
        event.setDropAction(Qt.MoveAction)
        event.setAccepted(True)
        
        pos = event.pos()
        new_block = graphics(pos, int(event.mimeData().text()), self.scene)             # Drop(Add) on the graphics
        block_list.append(new_block)
        #print(str(new_block.index))
        event.acceptProposedAction()

    def resizeEvent(self, event):
        pass

# Dock widget needed to separate window panel efficiently.
class Dock_Graphics(QDockWidget):                               # Graphics (Drop Zone) Dock widget
    def __init__(self):
        super(Dock_Graphics, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Graphics')
        self.scene = QGraphicsScene(0, 0, 650, 400)
        self.graphic = qgraphicsView(self.scene)
        self.setWidget(self.graphic)
        self.show()
    def mousePressEvent(self, event):
        click_listen.flag = 0
        print("Click empty screen")

class Dock_Code(QDockWidget):                                   # Code (Code writing Zone) Dock widget
    def __init__(self):
        super(Dock_Code, self).__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Code')
        self.plaintext = QTextEdit()
        self.plaintext.setPlainText("import torch\n")
        self.plaintext.setAcceptDrops(False)
        self.setWidget(self.plaintext)
        self.show()

class Dock_Constraints(QDockWidget):
    def __init__(self):
        super(Dock_Constraints, self).__init__()
        self.setWindowTitle('Constraints')
        self.show()

class Window(QMainWindow):                                                 # Main window
    def __init__(self):
        QMainWindow.__init__(self)
        global click_listen
        #global dock_cons
        pallete_buttons = pallete()                                         

        scene = QGraphicsScene(0, 0, 200, 400)
        scene.addItem(pallete_buttons)

        graphic = QGraphicsView(scene)
        graphic.show()
        self.setCentralWidget(graphic)                                      # Drop zone

        self.dock = Dock_Graphics()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock) 
        
        self.dock1 = Dock_Code()
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock1)
        
        self.dock2 = Dock_Constraints()
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock2)
        #dock_cons = self.dock2

        click_listen = click_listener()             #

############################################################################################

class graphics_part(QGraphicsObject):                                               #
    def __init__(self, parent=None):
        super(graphics_part, self).__init__(parent)
        global num
        self.color = QColor(Qt.lightGray)
        self.dragOver = True
        self.pos_ = None
        self.setAcceptDrops(False)
        self.setFlag(self.ItemIsMovable, False)
        self.index = num
        self.connect_list = []                                                      # List that save connected blocks
        self.table = menu.menu_block(self.index, self.shape, self.connect_list)
        self.table.itemChanged.connect(self.refresh_table)
        
    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:                                         # drag & drop
            self.setCursor(Qt.ClosedHandCursor)
            self.table.setItem(0, 1, QTableWidgetItem(str(self.shape)))
            print(str(self.index) + " " + str(self.shape) + " " + str(self.connect_list))
            window.dock2.setWidget(self.table)
            self.setFlag(self.ItemIsMovable, True)

            if(click_listen.flag == 0):                                             # 0 : click background
                click_listen.from_ = self                                           # 1 : click block    
                click_listen.flag = 1                                               # clock blocks consequently : connect blocks
            elif(click_listen.flag == 1):
                click_listen.to_ = self
                click_listen.connect(self)
                arrow.arrows(click_listen.from_, click_listen.to_)
                click_listen.flag = 0
                click_listen.from_ = None
                click_listen.to_ = None

        elif event.button() == Qt.RightButton:                                      # remove
        
            block_list[self.index].shape = self.shape
            print("right clicked")            
            window.dock2.setWidget(menu.right_click_table(block_list))
            self.update()

    def refresh_table(self):
        self.index = self.table.item(0,0).text()
        self.shape = self.table.item(0,1).text()
        self.connect_list.append(self.table.item(0,2).text())

class neuron_rec_(graphics_part):
    def __init__(self, pos_):
        super(neuron_rec_, self).__init__()
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 1
        self.pos_ = pos_

    def boundingRect(self):
        return QRectF(self.pos_.x() - 30, self.pos_.y() - 60, 60, 60)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawRect(self.pos_.x() - 30, self.pos_.y() - 60, 60, 60)
        painter.drawText(self.pos_.x() - 4, self.pos_.y() - 22, str(self.index))

class neuron_cir_(graphics_part):
    def __init__(self, pos_):
        super(neuron_cir_, self).__init__()
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 2
        self.pos_ = pos_

    def boundingRect(self):
        return QRectF(self.pos_.x()-20, self.pos_.y()-60, 40, 60)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawEllipse(self.pos_.x() - 20, self.pos_.y() - 60, 40, 60)
        painter.drawText(self.pos_.x() - 4, self.pos_.y() - 22, str(self.index))

class graphics(graphics_part):
    def __init__(self, pos, shape, scene):
        super(graphics, self).__init__()
        self.setFlag(self.ItemHasNoContents)
        self.scene = scene
        global num

        if(shape == 1):
            print("Add Rectangle")
            self.scene.addItem(neuron_rec_(pos))
        else:
            print("Add Circle")
            self.scene.addItem(neuron_cir_(pos))

        num += 1                                                        # index number for blocks

    def boundingRect(self):
        return QRectF()

    def paint(self, painter, option, widget=None):
        pass

class click_listener():
    global num
    def __init__(self):
        super(click_listener, self).__init__()
        self.flag = 0
        self.from_ = None
        self.to_ = None

    def connect(self, dest):
        flag = 0                                                    # Avoid duplication
        for i in self.from_.connect_list:
            if i == dest.index:
                flag = 1
                break

        if flag == 0:
            self.from_.connect_list.append(dest.index)

        print("dest : ", self.from_.index)
        print(self.from_.connect_list)

if __name__ == '__main__':
    global window
    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 200, 1000, 700)
    window.setWindowTitle('Mango')
    window.show()
    sys.exit(app.exec_())

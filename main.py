import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import dropped_blocks
import arrow

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

        self.setScene(self.scene)
        self.setAcceptDrops(True)

        arrow.load_scene(self.scene)

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
        #pal = dropped_blocks.graphics(pos, int(event.mimeData().text()))                # Drop(Add) on the graphics
        dropped_blocks.graphics(pos, int(event.mimeData().text()), self.scene)
        #dropped_blocks.graphics(pos, int(event.mimeData().text()), self.scene)
        #tmp = QPoint(200, 200)
        #dropped_blocks.arrows(pos, tmp, self.scene)
        ###self.scene.addItem(pal)
        #dropped_blocks.arrow(self.scene)
        #self.scene.addItem(dropped_blocks.click_listener().paintEvent(self))
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
        dropped_blocks.click_listen.flag = 0
        print("Click empty screen")

class Dock_Code(QDockWidget):                                   # Code (Code writing Zone) Dock widget
    def __init__(self):
        super(Dock_Code, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Code')
        self.plaintext = QTextEdit()
        self.plaintext.setPlainText("import torch\n")
        self.setWidget(self.plaintext)
        self.show()

'''class DockContents(QWidget):                                                # delete?
    _sizehint = None
    def setSizeHint(self, width, height):
        self._sizehint = QSize(width, height)

    def sizeHint(self):
        print('sizeHint:', self._sizehint)
        if self._sizehint is not None:
            return self._sizehint
        return super(MyWidget, self).sizeHint()
'''
class Window(QMainWindow):                                                 # Main window
    def __init__(self):
        QMainWindow.__init__(self)

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

        dropped_blocks.click_listen = dropped_blocks.click_listener()             #
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    #neu_list = dropped_blocks.neuron_list()
    window.setGeometry(500, 200, 1000, 700)
    window.setWindowTitle('Mango')
    window.show()
    sys.exit(app.exec_())

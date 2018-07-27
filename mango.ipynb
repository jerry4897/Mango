import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import dropped_blocks

class pallete_part(QGraphicsObject):
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
        pixmap.fill(Qt.white)

        painter = QPainter(pixmap)
        painter.translate(0, 0)
        painter.setRenderHint(QPainter.Antialiasing)
        self.paint(painter, None, None)
        painter.end()

        pixmap.setMask(pixmap.createHeuristicMask())

        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(30, 30))
        
        drag.exec_()
        self.setCursor(Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
      
class neuron_rec(pallete_part):
    def __init__(self, parent=None):
        super(neuron_rec, self).__init__(parent)
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 1                              

    def boundingRect(self):
        return QRectF(0, 0, 60, 60)
    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawRect(0, 0, 60, 60)

class neuron_cir(pallete_part):
    def __init__(self, parent=None):
        super(neuron_cir, self).__init__(parent)
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 2

    def boundingRect(self):
        return QRectF(80, 0, 40, 60)
    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawEllipse(80, 0, 40, 60)

class pallete(pallete_part):
    def __init__(self):
        super(pallete, self).__init__()

        self.setFlag(self.ItemHasNoContents)
        self.rectangle = neuron_rec(self)
        #self.circle = neuron_cir(self.rectangle)
        self.circle = neuron_cir(self)
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
    def dragMoveEvent(self, event):
        #pass
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
        pal = dropped_blocks.pallete(pos, int(event.mimeData().text()))
        
        self.scene.addItem(pal)
        event.acceptProposedAction()
    def resizeEvent(self, event):
        pass

class Dock_Graphics(QDockWidget):
    def __init__(self):
        super(Dock_Graphics, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Graphics')
        self.scene = QGraphicsScene(0, 0, 650, 400)
        self.graphic = qgraphicsView(self.scene)
        self.setWidget(self.graphic)

        self.show()

class Dock_Code(QDockWidget):
    def __init__(self):
        super(Dock_Code, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Code')
        self.plaintext = QTextEdit()
        self.plaintext.setPlainText("import tensorflow as tf\n")
        #self.plaintext.append("????")
        #self.plaintext.textChanged.connect(self.text_changed)
        self.setWidget(self.plaintext)
        self.show()

class DockContents(QWidget):
    _sizehint = None
    def setSizeHint(self, width, height):
        self._sizehint = QSize(width, height)

    def sizeHint(self):
        print('sizeHint:', self._sizehint)
        if self._sizehint is not None:
            return self._sizehint
        return super(MyWidget, self).sizeHint()

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        pallete_buttons = pallete()

        scene = QGraphicsScene(0, 0, 200, 400)
        scene.addItem(pallete_buttons)
        
        '''for obj in scene.items():
            if obj.shape == 0:
                print(obj)'''

        graphic = QGraphicsView(scene)
        graphic.show()

        self.setCentralWidget(graphic)                                      # Drop zone

        self.dock = Dock_Graphics()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock) 
        
        self.dock1 = Dock_Code()
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock1)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 200, 1000, 700)
    window.setWindowTitle('Mango')
    window.show()
    sys.exit(app.exec_())

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class arrow_part(QGraphicsItem):                                               #
    def __init__(self, parent=None):
        super(arrow_part, self).__init__(parent)
        #global num
        self.color = QColor(Qt.lightGray)
        self.dragOver = True
        self.pos_ = None
        self.setAcceptDrops(False)
        self.setFlag(self.ItemIsMovable, False)
        #self.index = num
        self.connect_list = []                                                      # List that save connected blocks

    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)

class arrow(arrow_part):
    def __init__(self, from_, to_):
        super(arrow, self).__init__()
        self.from_ = from_
        self.to_ = to_

    def boundingRect(self):
        return QRectF(self.from_.x(), self.from_.y(), self.to_.x(), self.to_.y())

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        #painter.drawLine(self.from_.x(), self.from_.y(), self.to_.x(), self.to_.y())
        painter.drawLine(100, 100, 200, 250)

class arrows(arrow_part):
    def __init__(self, from_, to_):
        super(arrows, self).__init__()
        self.setFlag(self.ItemHasNoContents)
        global num
        self.from_ = from_
        self.to_ = to_

        #scen.addRect(100, 100, 200, 200)
        scen.addItem(arrow(self.from_, self.to_))
        scen.update()
    def boundingRect(self):
        return QRectF()

    def paint(self, painter, option, widget=None):
        pass

class load_scene(QGraphicsScene):
    def __init__(self, scene):
        super(load_scene, self).__init__()
        global scen
        scen = scene
        #self.give_scene()
        #self.scene.addRect(100, 100, 200, 200)
    #def give_scene(self):
    #    return self.scene

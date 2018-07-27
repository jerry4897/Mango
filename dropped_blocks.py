from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class pallete_part(QGraphicsObject):
    def __init__(self, parent=None):
        super(pallete_part, self).__init__(parent)

        self.color = QColor(Qt.lightGray)
        self.dragOver = True
        self.pos_ = None
        self.setAcceptDrops(False)
        self.setFlag(self.ItemIsMovable)

    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)

class neuron_rec(pallete_part):
    def __init__(self, parent=None):
        super(neuron_rec, self).__init__(parent)
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 1
    def boundingRect(self):
        return QRectF(self.pos_.x() - 30, self.pos_.y() - 60, 60, 60)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawRect(self.pos_.x() - 30, self.pos_.y() - 60, 60, 60)
        #print(self.pos_x)


class neuron_cir(pallete_part):
    def __init__(self, parent=None):
        super(neuron_cir, self).__init__(parent)
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 2

    def boundingRect(self):
        return QRectF(self.pos_.x()-20, self.pos_.y()-60, 40, 60)
    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawEllipse(self.pos_.x() - 20, self.pos_.y() - 60, 40, 60)


class pallete(pallete_part):
    def __init__(self, pos, shape):
        super(pallete, self).__init__()

        self.setFlag(self.ItemHasNoContents)
        #print(pos)
        if(shape == 1):
            neuron_rec(self).pos_ = pos   
        else:
            neuron_cir(self).pos_ = pos
            

    def boundingRect(self):
        return QRectF()

    def paint(self, painter, option, widget=None):
        pass

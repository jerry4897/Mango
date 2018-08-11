from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

arrow_list = []

class arrow_part(QGraphicsItem):                                               #
    def __init__(self, parent=None):
        super(arrow_part, self).__init__(parent)
        self.color = QColor(Qt.lightGray)
        self.dragOver = True
        self.pos_ = None
        self.setAcceptDrops(False)
        self.setFlag(self.ItemIsMovable, False)
        self.connect_list = []                                                      # List that save connected blocks

class arrow(arrow_part):
    def __init__(self, from_x, from_y, to_x, to_y):
        super(arrow, self).__init__()
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y

    def boundingRect(self):
        return QRectF(self.from_x, self.from_y-30, self.to_x, self.to_y-30)

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.DashLine))
        #painter.setPen(Qt.yellow)
        if(self.from_x == self.to_x and self.from_y == self.to_y):
            painter.drawLine(self.from_x + 30, self.from_y - 30, self.from_x + 60, self.from_y-30)
            painter.drawLine(self.from_x + 60, self.from_y - 30, self.from_x + 60, self.from_y-90)
            painter.drawLine(self.from_x + 60, self.from_y - 90, self.from_x, self.from_y-90)
            painter.drawLine(self.from_x, self.from_y - 90, self.from_x, self.from_y-60)
        else:
            painter.drawLine(self.from_x, self.from_y-30, self.to_x, self.to_y-30)
            '''self.mid_x = (self.from_x + self.to_x) / 2
            self.mid_y = (self.from_y + self.to_y - 60) / 2
            painter.drawLine(self.mid_x - 2, self.mid_y-2, self.mid_x, self.mid_y)
            painter.drawLine(self.mid_x - 2, self.mid_y+2, self.mid_x, self.mid_y)'''

class arrows(arrow_part):
    def __init__(self, from_x, from_y, to_x, to_y):
        super(arrows, self).__init__()
        self.setFlag(self.ItemHasNoContents)
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y

        tmp = arrow(self.from_x, self.from_y, self.to_x, self.to_y)
        arrow_list.append(tmp)
        scen.addItem(tmp)
        scen.update()
        print(arrow_list)

    def boundingRect(self):
        return self.QRectF

    def paint(self, painter, option, widget=None):
        pass
    
    def remove_arrow(self, index):
        import sip
        sip.delete(arrow_list[index])
        arrow_list.remove(arrow_list[index])
        scen.update()

class load_scene(QGraphicsScene):
    def __init__(self, scene):
        super(load_scene, self).__init__()
        global scen
        scen = scene
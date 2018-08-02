from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import math
import arrow

click_listen = None
num = 0
'''
When buttons(neurons) dragged from the pallete, these classes are activated.
'''
class Arrow(QGraphicsLineItem):
    def __init__(self, startItem, endItem, parent=None, scene=None):
        super(Arrow, self).__init__(parent, scene)
  
        self.arrowHead = QPolygonF()
  
        self.myStartItem = startItem
        self.myEndItem = endItem
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.myColor = Qt.black
        self.setPen(QPen(self.myColor, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
  
    def setColor(self, color):
        self.myColor = color
  
    def startItem(self):
        return self.myStartItem
  
    def endItem(self):
        return self.myEndItem
  
    def boundingRect(self):
        extra = (self.pen().width() + 20) / 2.0
        p1 = self.line().p1()
        p2 = self.line().p2()
        return QRectF(p1, QSizeF(p2.x() - p1.x(), p2.y() - p1.y())).normalized().adjusted(-extra, -extra, extra, extra)
  
    def shape(self):
        path = super(Arrow, self).shape()
        path.addPolygon(self.arrowHead)
        return path
  
    def updatePosition(self):
        line = QLineF(self.mapFromItem(self.myStartItem, 0, 0), self.mapFromItem(self.myEndItem, 0, 0))
        self.setLine(line)
  
    def paint(self, painter, option, widget=None):
        if (self.myStartItem.collidesWithItem(self.myEndItem)):
            return
  
        myStartItem = self.myStartItem
        myEndItem = self.myEndItem
        myColor = self.myColor
        myPen = self.pen()
        myPen.setColor(self.myColor)
        arrowSize = 20.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)
  
        centerLine = QLineF(myStartItem.pos(), myEndItem.pos())
        endPolygon = myEndItem.polygon()
        p1 = endPolygon.first() + myEndItem.pos()
  
        intersectPoint = QPointF()
        for i in endPolygon:
            p2 = i + myEndItem.pos()
            polyLine = QLineF(p1, p2)
            intersectType = polyLine.intersect(centerLine, intersectPoint)
            if intersectType == QLineF.BoundedIntersection:
                break
            p1 = p2
  
        self.setLine(QLineF(intersectPoint, myStartItem.pos()))
        line = self.line()
  
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle
  
        arrowP1 = line.p1() + QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi / 3) * arrowSize)
        arrowP2 = line.p1() + QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)
  
        self.arrowHead.clear()
        for point in [line.p1(), arrowP1, arrowP2]:
            self.arrowHead.append(point)
  
        painter.drawLine(line)
        painter.drawPolygon(self.arrowHead)
        if self.isSelected():
            painter.setPen(QPen(myColor, 1, Qt.DashLine))
            myLine = QLineF(line)
            myLine.translate(0, 4.0)
            painter.drawLine(myLine)
            myLine.translate(0,-8.0)
            painter.drawLine(myLine)

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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:                                         # drag & drop
            self.setCursor(Qt.ClosedHandCursor)
            self.setFlag(self.ItemIsMovable, True)

            if(click_listen.flag == 0):                                             # 0 : click background
                click_listen.from_ = self                                           # 1 : click block    
                click_listen.flag = 1                                               # clock blocks consequently : connect blocks
            elif(click_listen.flag == 1):
                click_listen.to_ = self
                click_listen.connect(self)
                #self.connect(arrows(click_listen.from_, click_listen.to_, ))
                arrow.arrows(click_listen.from_, click_listen.to_)
                click_listen.flag = 0
                click_listen.from_ = None
                click_listen.to_ = None

        elif event.button() == Qt.RightButton:                                      # remove
            print("right clicked")
            tb = TableWidget()
            tb.show()
            self.update()
            #self.setParent(None)
            #self.update()
    '''def mouseReleaseEvent(self, event):
        posm = event.pos()
        if self.contains(posm):
            print("시발")'''
class TableWidget(QTableWidget):
 
    def __init__(self, parent = None):
        QTableWidget.__init__(self, parent)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
         
        quitAction = QAction("Quit", self)
        quitAction.triggered.connect(self.test)
        self.addAction(quitAction)
    def test(self):
        print("wow!")
'''class neuron_rec(graphics_part):
    def __init__(self, parent=None):
        super(neuron_rec, self).__init__(parent)
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 1
    def boundingRect(self):
        return QRectF(self.pos_.x() - 30, self.pos_.y() - 60, 60, 60)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawRect(self.pos_.x() - 30, self.pos_.y() - 60, 60, 60)'''
class neuron_rec(graphics_part):
    def __init__(self, pos_):
        super(neuron_rec, self).__init__()
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 1

        self.pos_ = pos_
    def boundingRect(self):
        return QRectF(self.pos_.x() - 30, self.pos_.y() - 60, 60, 60)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawRect(self.pos_.x() - 30, self.pos_.y() - 60, 60, 60)

class neuron_cir(graphics_part):
    def __init__(self, pos_):
        super(neuron_cir, self).__init__()
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 2

        self.pos_ = pos_
    def boundingRect(self):
        return QRectF(self.pos_.x()-20, self.pos_.y()-60, 40, 60)
    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawEllipse(self.pos_.x() - 20, self.pos_.y() - 60, 40, 60)


class graphics(graphics_part):
    #def __init__(self, pos, shape):
    def __init__(self, pos, shape, scene):
        super(graphics, self).__init__()
        self.setFlag(self.ItemHasNoContents)
        global num
        self.scene = scene
        if(shape == 1):
            print("Add Rectangle")
            #neuron_rec(self).pos_ = pos
            self.scene.addItem(neuron_rec(pos))
        else:
            print("Add Circle")
            #neuron_cir(self).pos_ = pos
            self.scene.addItem(neuron_cir(pos))

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

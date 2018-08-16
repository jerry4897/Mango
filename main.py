import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import arrow
import menu

click_listen = None
num = 0                                                     # index of blocks.
shape = 1                                                   # shape of blocks.
block_list = []                                             # save all the list of blocks that are exist in main screen.
connection_list = [[-1, -1], [-1, -1]]                      # 2-dimensional list that save the connections of blocks.
f = open("test.py", "w+")

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

class input_holder(pallete_part):                                     # circle shape of pallete
    def __init__(self, parent=None):
        super(input_holder, self).__init__(parent)
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 0

    def boundingRect(self):
        return QRectF(140, 0, 80, 40)
    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawRect(140, 0, 80, 40)
        painter.drawText(165, 25, "input")

class pallete(pallete_part):                                        # pallete activating part
    def __init__(self):
        super(pallete, self).__init__()

        self.setFlag(self.ItemHasNoContents)

        self.rectangle = neuron_rec(self)                           # activate rectangle button
        self.circle = neuron_cir(self)                              # activate circle button
        self.input_box = input_holder(self)

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
        global num
        event.setDropAction(Qt.MoveAction)
        event.setAccepted(True)
        
        pos = event.pos()
        new_block = graphics(pos, int(event.mimeData().text()), self.scene)             # Drop(Add) on the graphics
        block_list.append(new_block)

        block_list[len(block_list) - 1].shape = shape
        if(shape > 0):
            block_input = input_block(0)                                                # input menu pop up
            block_list[len(block_list) - 1].name = block_input.first_input
            block_list[len(block_list) - 1].function = block_input.second_input 
            window.dock1.plaintext.append("with tf.variable_scope('" + block_list[len(block_list) - 1].name + "')as scope:\n" + "    print(\"" + block_input.first_input + "\")")
        else:
            block_input = input_block(1)
            block_list[len(block_list) - 1].name = block_input.first_input
            block_list[len(block_list) - 1].function = block_input.second_input  
            window.dock1.plaintext.append("with tf.name_scope('" + "input" + "')as scope:")
            window.dock1.plaintext.append("    X = tf.placeholder(tf.float32, [None, " + block_list[len(block_list) - 1].name + "])")
            window.dock1.plaintext.append("    Y = tf.placeholder(tf.float32, [None, " + block_list[len(block_list) - 1].function + "])")

        f.seek(0)
        f.truncate(0)
        f.write(window.dock1.plaintext.toPlainText())
        f.flush()
        
        import py_compile                                               # convert plain text of 'code' to 'test.py'.
        try:                                                            # Then, 'test.py' is compiled to 'dest.pyc'
            py_compile.compile("test" + ".py" , "dest" + ".pyc")
            print("compile complete")
        except py_compile.PyCompileError:
            print("error")

        import shlex                                                    # Show output of 'dest.pyc' to cmd.
        from subprocess import Popen, PIPE
        args = shlex.split("python dest.pyc")
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        #exitcode = proc.returncode
        print(out)
        
        #print(new_block.pos)
        #print(str(new_block.index))
        event.acceptProposedAction()

    def resizeEvent(self, event):
        pass

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
            self.set_input()
        else:
            self.initUI()

        self.first_input
        self.second_input
    def set_input(self):
        self.first_input, okPressed = QInputDialog.getText(self, "Input parameter","Input parameter:", QLineEdit.Normal, "")
        if okPressed and self.first_input != '':
            print(self.first_input)
        
        self.second_input, okPressed = QInputDialog.getText(self, "Output parameter","Output parameter:", QLineEdit.Normal, "")
        if okPressed and self.second_input != '':
            print(self.second_input)

    def initUI(self): 
        self.first_input = self.getName()
        self.second_input = self.getFucntion()
 
        self.show()
    def getName(self):
        text, okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
        return text
    def getFucntion(self):
        items = ("Relu","SoftMax")
        item, okPressed = QInputDialog.getItem(self, "Activation Function","Activation Function:", items, 0, False)
        if okPressed and item:
            print(item)
        return item
 
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
        self.plaintext.setPlainText("import tensorflow as tf\nimport numpy as np\n")
        self.plaintext.setAcceptDrops(False)
        self.plaintext.textChanged.connect(self.renew)
        self.setWidget(self.plaintext)
        self.show()

    def renew(self):
        f.seek(0)
        f.truncate(0)
        f.write(self.plaintext.toPlainText())
        f.flush()
        
        import py_compile
        try:
            py_compile.compile("test" + ".py" , "dest" + ".pyc")
            print("compile complete!")
        except py_compile.PyCompileError:
            print("error")

class Dock_Constraints(QDockWidget):                           # Menu / Constraints widget
    def __init__(self):
        super(Dock_Constraints, self).__init__()
        self.setWindowTitle('Constraints')
        self.show()

class Window(QMainWindow):                                                 # Main window
    def __init__(self):
        QMainWindow.__init__(self)
        global click_listen
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

        click_listen = click_listener()                                     # Manage click event.

'''
When the block dragged and dropped to the main screen(graphics),
classes below are activated.
'''
class graphics_part(QGraphicsObject):                                               #
    def __init__(self, parent=None):
        super(graphics_part, self).__init__(parent)
        global num
        self.color = QColor(Qt.lightGray)
        self.dragOver = True
        self.pos_ = None
        self.setAcceptDrops(False)
        self.index = num
        self.connect_list = []                                                      # List that save connected blocks
        self.table = menu.menu_block(self.index, self.connect_list)
        self.table.itemChanged.connect(self.refresh_table)
        self.__mousePressPos = None
        self.setFlag(self.ItemIsMovable, True)
        
    def mousePressEvent(self, event):
        self.__mousePressPos = event.pos()                          # delete?
        if event.button() == Qt.LeftButton:                                         
            self.setCursor(Qt.ClosedHandCursor)
            self.table.setItem(0, 3, QTableWidgetItem(str((self.shape))))
            self.table.setItem(0, 0, QTableWidgetItem(str((block_list[self.index].name))))
            self.table.setItem(0, 1, QTableWidgetItem(str((block_list[self.index].function))))
            print(str(self.index) + " " + str(self.shape) + " " + str(self.connect_list))
            window.dock2.setWidget(self.table)

        elif event.button() == Qt.RightButton:                                      # right click menu
            print("right clicked")
            window.dock2.setWidget(menu.right_click_table(block_list, self, connection_list))
            self.update()

    def refresh_table(self):
        #self.index = self.table.item(0,0).text()
        #self.shape = self.table.item(0,1).text()
        self.connect_list.append(self.table.item(0,4).text())

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

class input_holder_(graphics_part):
    def __init__(self, pos_):
        super(input_holder_, self).__init__()
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 0
        self.pos_ = pos_

    def boundingRect(self):
        return QRectF(self.pos_.x()-20, self.pos_.y()-60, 80, 40)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawRect(self.pos_.x() - 20, self.pos_.y() - 60, 80, 40)
        painter.drawText(self.pos_.x() + 4, self.pos_.y() - 32, "input")

class graphics(graphics_part):
    def __init__(self, pos, shape_, scene):
        super(graphics, self).__init__()
        self.setFlag(self.ItemHasNoContents)
        self.scene = scene
        self.pos = pos
        
        global num
        global shape
        global connection_list
        shape = shape_
        if(shape_ == 1):
            print("Add Rectangle")
            self.scene.addItem(neuron_rec_(pos))
        elif(shape_ == 2):
            print("Add Circle")
            self.scene.addItem(neuron_cir_(pos))
        else:
            print("Add Input Holder")
            self.scene.addItem(input_holder_(pos))

        num += 1                                                        # index number for blocks
        if(num == len(connection_list)):
            menu.extend_list(connection_list)

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
    f.truncate(0)
    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 200, 1000, 700)
    window.setWindowTitle('Mango')
    window.show()
    sys.exit(app.exec_())
    f.close()
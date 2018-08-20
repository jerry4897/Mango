import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import arrow
import menu
import input_block
import write_code

click_listen = None
num = 0                                                     # index of blocks + input box.
shape = 1                                                   # shape of blocks.
block_list = []                                             # save all the list of blocks that are exist in main screen.
connection_list = [[-1, -1], [-1, -1]]                      # 2-dimensional list that save the connections of blocks.

layer_names = []
layer_functions = []
layer_sizes = []
num_layer = 0
num_classes = 0

directory = ""

learning_rate = 0
training_steps = 0
batch_size = 0

optimizer = ""
loss_function = ""
display_step = 0

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

class output_holder(pallete_part):
    def __init__(self, parent=None):
        super(output_holder, self).__init__(parent)
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 3

    def boundingRect(self):
        return QRectF(140, 60, 80, 40)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawRect(140, 60, 80, 40)
        painter.drawText(160, 85, "output")

class pallete(pallete_part):                                        # pallete activating part
    def __init__(self):
        super(pallete, self).__init__()

        self.setFlag(self.ItemHasNoContents)

        self.rectangle = neuron_rec(self)                           # activate rectangle button
        self.circle = neuron_cir(self)                              # activate circle button
        self.input_box = input_holder(self)
        self.output_box = output_holder(self)

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
        if shape == 0:
            type_text.append_input_text()                                                                # type code to plain text of 'Code' part.
            compile_text(1)                                                                # copy the 'Code' to test.py and compile it to dest.pyc
        elif shape < 3:
            tmp = layer_info()
            layer_info.get_layer_info(tmp)
        #else:

        #print(new_block.pos)
        #print(str(new_block.index))
        event.acceptProposedAction()                

    def resizeEvent(self, event):
        pass

'''class type_text_transfer():
    def __init__(self, from_name, from_size, to_name, to_size, activation_function):
        super().__init__()
        type_text()'''
class type_text():
    def __init__(self):
        super().__init__()
        global num_classes
        global directory
        global learning_rate
        global training_steps
        global batch_size

    @staticmethod
    def append_input_text(parent = None):
        """
        if shape:
            block_list[len(block_list) - 1].name, block_list[len(block_list) - 1].function, ok = input_block.input_layer.getOutput()    
        else :
            block_list[len(block_list) - 1].name, block_list[len(block_list) - 1].function, direc, ok = input_block.input_name.getOutput()
        
        if shape :
            window.dock1.plaintext.append("with tf.variable_scope('" + block_list[len(block_list) - 1].name + "')as scope:\n" + "    print(\"" +  block_list[len(block_list) - 1].function + "\")\n")
        else:
            window.dock1.plaintext.append("input_data = input_data.read_data_sets(\"" + direc + "\")\n")
            window.dock1.plaintext.append("with tf.name_scope('" + "input" + "')as scope:")
            window.dock1.plaintext.append("    X = tf.placeholder(tf.float32, [None, " + block_list[len(block_list) - 1].name + "])")
            window.dock1.plaintext.append("    Y = tf.placeholder(tf.float32, [None, " + block_list[len(block_list) - 1].function + "])\n")
        
        global num_classes
        global directory
        global learning_rate
        global training_steps
        global batch_size

        global optimizer
        global loss_function
        global display_step
        """
        block_len = len(block_list) - 1

        input_size, num_classes, directory, learning_rate, training_steps, batch_size, ok = input_block.input_name.getOutput()
        block_list[block_len].name = "input"
        block_list[block_len].function = "None"
        block_list[block_len].index = block_len
        block_list[block_len].size = input_size

        layer_names.append("input")
        layer_sizes.append(input_size)
        print(layer_sizes[0])
        print(num_classes)
        print(directory)
        print(learning_rate)
        print(training_steps)
        print(batch_size)
        write_code.write_input_box_process(window, "input", input_size, num_classes, directory, learning_rate, training_steps, batch_size)

class layer_info():
    def __init__(self):
        super().__init__()
        global optimizer
        global loss_function
        global display_step
        
    def get_layer_info(self):
        block_len = len(block_list) - 1
        name, size, ok = input_block.input_layer.getOutput()
        block_list[block_len].name = name
        #block_list[block_len].function = func
        block_list[block_len].index = block_len
        block_list[block_len].size = size

        layer_names.append(name)
        layer_sizes.append(size)
        #layer_functions.append(func)

class output_block():
    def __init__(self):
        super().__init__()
        global num_classes
        global directory
        global learning_rate
        global training_steps
        global batch_size

        layer_names.append("output")                                                         # output
        layer_sizes.append(num_classes)
        loss_function, optimizer, display_step, ok = input_block.output_layer.getOutput()
        ''''elif shape < 3 :                                                                         # layer
            name, size, func, ok = input_block.input_layer.getOutput()
            block_list[block_len].name = name
            block_list[block_len].function = func
            block_list[block_len].index = block_len
            block_list[block_len].size = size

            layer_names.append(name)
            layer_sizes.append(size)
            layer_functions.append(func)
            #write_code.write_layer_process(window, layer_names, layer_sizes, num_classes, directory, learning_rate, training_steps, batch_size)
        
        else :
            layer_names.append("output")                                                         # output
            layer_sizes.append(num_classes)
            loss_function, optimizer, display_step, ok = input_block.output_layer.getOutput()
            print(loss_function)
            print(optimizer)
            print(display_step)
            #write_code.write_to_dock_code(window, layer_names, layer_sizes, directory, learning_rate, training_steps, batch_size, loss_function, optimizer, display_step)
        '''
        #print(layer_sizes)

        #write_code.write_to_dock_code(window, layer_names, layer_sizes, direc, learning_rate, training_steps, batch_size, loss_function, optimizer, display_step)
             
class compile_text():
    def __init__(self, flag_for_show_output):
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

        if flag_for_show_output:
            import shlex                                                    # Show output of 'dest.pyc' to cmd.
            from subprocess import Popen, PIPE
            args = shlex.split("python dest.pyc")
            proc = Popen(args, stdout=PIPE, stderr=PIPE)
            out, err = proc.communicate()
            #exitcode = proc.returncode
            print(out)
 
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
        self.plaintext.textChanged.connect(lambda : compile_text(0))
        self.setWidget(self.plaintext)
        self.show()

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

        click_listen = click_listener()                                             # Manage click event.

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
        self.__mousePressPos = event.pos()                                          # delete?
        if event.button() == Qt.LeftButton:                                         
            self.setCursor(Qt.ClosedHandCursor)
            self.table.setItem(0, 3, QTableWidgetItem(str((self.shape))))
            self.table.setItem(0, 0, QTableWidgetItem(str((block_list[self.index].name))))
            self.table.setItem(0, 1, QTableWidgetItem(str((block_list[self.index].function))))
            print(str(self.index) + " " + str(self.shape) + " " + str(self.connect_list))
            window.dock2.setWidget(self.table)

        elif event.button() == Qt.RightButton:                                      # right click menu
            print("right clicked")
            window.dock2.setWidget(menu.right_click_table(block_list, self, connection_list, window))
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

class output_holder_(graphics_part):
    def __init__(self, pos_):
        super(output_holder_, self).__init__()
        self.setCursor(Qt.OpenHandCursor)
        self.shape = 3
        self.pos_ = pos_

    def boundingRect(self):
        return QRectF(self.pos_.x()-20, self.pos_.y()-60, 80, 40)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
        painter.drawRect(self.pos_.x() - 20, self.pos_.y() - 60, 80, 40)
        painter.drawText(self.pos_.x(), self.pos_.y() - 32, "output")

class graphics(graphics_part):
    def __init__(self, pos, shape_, scene):
        super(graphics, self).__init__()
        self.setFlag(self.ItemHasNoContents)
        self.scene = scene
        self.pos = pos
        
        global num
        global num_layer
        global shape
        global connection_list
        shape = shape_
        if shape_ == 1 :
            print("Add Rectangle")
            self.scene.addItem(neuron_rec_(pos))
        elif shape_ == 2 :
            print("Add Circle")
            self.scene.addItem(neuron_cir_(pos))
        elif shape == 0 :
            print("Add Input Holder")
            self.scene.addItem(input_holder_(pos))
        else:
            print("Add Output Holder")
            self.scene.addItem(output_holder_(pos))

        if shape_:
            num_layer += 1
        num += 1                                                                # index number for blocks
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
        flag = 0                                                                # Avoid duplication
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
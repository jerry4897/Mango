from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import main
import arrow
import input_block
import write_code

arrow_num = 0                                                   # count the number of arrows.
'''
Menu / Constraints widget : Bottom right screen of the window.
'''
class menu_set(QTableWidget):
    def __init__(self, parent = None):
        super(menu_set, self).__init__()
        self.cellClicked.connect(self.cellClick)

    def cellClick(self, row, col):
        print("Click" + str(row) + " " + str(col))

class menu_block(menu_set):
    def __init__(self, index, connect_list):
        super(menu_block, self).__init__()
        self.resize(250, 200)
        self.setRowCount(2)
        self.setColumnCount(5)

        column_headers = ['name', 'activation function ', 'index', 'shape', 'connections']
        self.setHorizontalHeaderLabels(column_headers)

        self.setItem(0,2, QTableWidgetItem(str(index)))
        self.setItem(0,4, QTableWidgetItem(str(connect_list)))

    def edititem(self, item):
        pass

'''
Check box class.
Every block has it's own connection list.
Initially every blocks are appeared in one's menu screen,
when you check box, blocks are connected. 
'''
class check_box_class(QGridLayout):
    def __init__(self, block_list, cur_block_index, cur_block_shape, connection_list, window):
        super(check_box_class, self).__init__()
        check_box_list = []
        self.checked_list = []                                                              # 0 : non-checked, 1 : checked

        if cur_block_shape == 1:
            self.addWidget(QLabel("ID : rectangle " + str(cur_block_index)), 0, 0)
        elif cur_block_shape == 2:
            self.addWidget(QLabel("ID : circle " + str(cur_block_index)), 0, 0)
        else:
            self.addWidget(QLabel("ID : iniput " + str(cur_block_index)), 0, 0)
        self.addWidget(QLabel("Connection"), 1, 0)

        for i in range(len(block_list)):
            check_box_list.append(check_box(cur_block_index, block_list, block_list[i].index, block_list[i].shape, self.checked_list, connection_list, window))
            self.checked_list.append(0)
            self.addWidget(check_box_list[i], i+1, 1)
            if (connection_list[cur_block_index][i] > -1):
                check_box_list[i].setChecked(True)
            else:
                check_box_list[i].setChecked(False)
            
class check_box(QCheckBox):
    def __init__(self, cur_block_index, block_list, check_box_index, check_box_shape, checked_list, connection_list, window):
        super(check_box, self).__init__()
        self.cur_block_index = cur_block_index
        self.check_box_index = check_box_index
        self.checked_list = checked_list

        self.block_list = block_list
        self.cur_block_index = cur_block_index
        self.check_box_index = check_box_index

        if(check_box_shape == 1):
            self.setText("rectangle " + str(check_box_index))
        elif(check_box_shape == 2):
            self.setText("circle " + str(check_box_index))
        else:
           self.setText("input " + str(check_box_index)) 
        self.stateChanged.connect(lambda : self.checked(connection_list, window))

    def checked(self, connection_list, window):
        global arrow_num

        # Add arrow.
        if self.isChecked() == True:
            if connection_list[self.cur_block_index][self.check_box_index] == -1:
                self.checked_list[self.check_box_index] = 1
                connection_list[self.cur_block_index][self.check_box_index] = arrow_num
                arrow.arrows(self.block_list[self.cur_block_index].pos.x(), self.block_list[self.cur_block_index].pos.y(), self.block_list[self.check_box_index].pos.x(), self.block_list[self.check_box_index].pos.y())
                arrow_num += 1
                activation_function, ok = input_block.activation_function.getOutput()
                write_code.write_layer_process(window, self.block_list[self.cur_block_index].name, self.block_list[self.cur_block_index].size, self.block_list[self.check_box_index].name, self.block_list[self.check_box_index].size, activation_function)
                #tmp = main.layer_info()
                #tmp.append_layer_text(self.block_list[self.cur_block_index].name, self.block_list[self.cur_block_index].size, self.block_list[self.check_box_index].name, self.block_list[self.check_box_index].size, activation_function)
                

        # remove arrow.
        elif connection_list[self.cur_block_index][self.check_box_index] > -1:
            self.checked_list[self.check_box_index] = 0
            arrow.arrows.remove_arrow(self, connection_list[self.cur_block_index][self.check_box_index])
            connection_list[self.cur_block_index][self.check_box_index] = -1
            arrow_num -= 1
        
        print(self.block_list[self.cur_block_index].pos)
        for i in range(len(connection_list)):
            print(connection_list[i])
        print("\n")
            
# If you click right click button this class is activated.
class right_click_table(QWidget):
    def __init__(self, block_list, current_block, connection_list, window):
        super(right_click_table, self).__init__()
        widget = QWidget()
        global list_
        list_ = block_list
        self.curr = current_block
        self.connection_list = connection_list

        layout = check_box_class(block_list, current_block.index, current_block.shape, connection_list, window)

        self.delete_button = QPushButton("Delete")
        layout.addWidget(self.delete_button, 0, 1)
        self.delete_button.clicked.connect(self.remove_block)

        widget.setLayout(layout)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(False)
        self.scroll.setWidget(widget)
        
        gLayout = QGridLayout()
        gLayout.addWidget(self.scroll)
        self.setLayout(gLayout)

    # Remove block... Connected with 'remove' button.
    def remove_block(self):
        import sip
        for i in list_:
            if(i.index == self.curr.index):
                list_.remove(i)
        sip.delete(self.curr)
        self.curr = None
        #for i in range(len(list_)):
        #    arrow.arrows.remove_arrow(self, )

class extend_list(list):                                            # Extend the connection list.
    def __init__(self, connection_list):
        super(extend_list, self).__init__()
        if len(connection_list) == 0:
            connection_list = [[-1, -1], [-1, -1]]
        
        for i in range(len(connection_list)):
            connection_list[i].append(-1)
            connection_list[i].append(-1)
        connection_list.append([-1] * ((len(connection_list)) + 2))
        connection_list.append([-1] * ((len(connection_list) - 1) + 2))
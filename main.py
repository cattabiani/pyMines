import sys
import random
import numpy
from enum import Enum, auto

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QLineEdit, QPushButton, QFormLayout
from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot  
from PyQt5.QtGui import QIntValidator   

class STATUS(Enum):
    PLAYING = auto()
    LOST = auto()
    WON = auto()
    NOTSET = auto()

class PyMines():



    def __init__(self, rows, cols, bmbs):
        if rows*cols > bmbs and rows >0 and cols > 0 and bmbs > 0 :
            self.rows_ = rows
            self.cols_ = cols
            self.bmbs_ = bmbs
            self.disc_ = 0
            self.st_ = STATUS.NOTSET
            self.brd_ = []
            self.vbrd_ = []

    def ck(self, xx, yy):
        return xx >= 0 and yy >= 0 and xx < self.rows_ and yy < self.cols_

    def setBrd(self, xx, yy):
        if self.ck(xx, yy) and not len(self.brd_) :
            temp = [-1]*self.bmbs_ + [0]*(self.rows_*self.cols_-self.bmbs_-1)
            random.shuffle(temp)
            temp.insert(xx*self.cols_ + yy, 0)
            self.brd_ = numpy.array(temp)
            self.brd_ = self.brd_.reshape([self.rows_, self.cols_])
            self.setNeighbours()
            self.vbrd_ = -numpy.ones([self.rows_, self.cols_], dtype=int)
            self.st_ = STATUS.PLAYING
            self.disc_ = 0
    
    def setNeighbours(self):
        for xx in range(self.rows_):
            for yy in range(self.cols_):
                if self.brd_[xx][yy] == -1 :
                    for ii in range(-1, 2):
                        for jj in range(-1, 2):
                            nxx = xx + ii
                            nyy = yy + jj
                            if self.ck(nxx, nyy) and self.brd_[nxx][nyy] != -1 :
                                self.brd_[nxx][nyy] += 1

    def toggleFlag(self, xx, yy) :
        if self.st_ == STATUS.PLAYING and self.ck(xx, yy) :
            if self.vbrd_[xx][yy] == -1:
                self.vbrd_[xx][yy] = -2
            elif self.vbrd_[xx][yy] == -2:
                self.vbrd_[xx][yy] = -1

    def click(self, xx, yy) :
        self.setBrd(xx, yy)
        out = []
        lst = []
        if self.st_ == STATUS.PLAYING and self.ck(xx, yy) and self.vbrd_[xx][yy] == -1:
            lst.append([xx, yy])

        while lst :
            elem = lst.pop(0)
            xx = elem[0]
            yy = elem[1]

            if self.brd_[xx][yy] == -1 :
                self.st_ = STATUS.LOST
            else :
                self.vbrd_[xx][yy]  = self.brd_[xx][yy]
                out.append([xx, yy])
                self.disc_ += 1
                if self.disc_ + self.bmbs_ >= self.rows_*self.cols_ :
                    self.st_ = STATUS.WON

                if self.vbrd_[xx][yy] == 0 :
                    for ii in range(-1, 2) :
                        for jj in range(-1, 2) :
                            nxx = xx + ii
                            nyy = yy + jj
                            if self.ck(nxx, nyy) and self.vbrd_[nxx][nyy] == -1:
                                lst.append([nxx,nyy])
                                self.vbrd_[nxx][nyy] = -2

        
        return out

    def lbl(self,xx,yy):
        if self.ck(xx, yy) :
            if self.vbrd_[xx][yy] == -1 :
                return ""
            elif self.vbrd_[xx][yy] == -2 :
                return "F"
            else :
                return str(self.vbrd_[xx][yy])

    def __str__(self):
        temp = "Rows: " + str(self.rows_) + "\n"
        temp += "Cols: " + str(self.cols_) + "\n"
        temp += "Bmbs: " + str(self.bmbs_) + "\n"
        temp += "Disc: " + str(self.disc_) + "\n"
        temp += "Status: " + str(self.st_) + "\n"
        temp += "Board: " + "\n" + str(self.brd_) + "\n"
        temp += "Visible Board: " + "\n" + str(self.vbrd_) + "\n"
        return temp

    rows_ = 0
    cols_ = 0
    bmbs_ = 0
    disc_ = 0
    st_ = STATUS.NOTSET
    brd_ = []
    vbrd_ = []
    
    

class PyMineSquare_GUI(QPushButton):
    def __init__(self, xx, yy):
        QPushButton.__init__(self)
        self.xx_ = xx
        self.yy_ = yy

    leftClick = pyqtSignal(int, int)
    rightClick = pyqtSignal(int, int)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.leftClick.emit(self.xx_, self.yy_)
        elif event.button() == QtCore.Qt.RightButton:
            self.rightClick.emit(self.xx_, self.yy_)

    

    xx_ = -1
    yy_ = -1


class PyMines_GUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # self.setMinimumSize(QSize(640, 480))    
        self.setWindowTitle("PyMines") 

        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   
    
        self.mainLayout_ = QGridLayout() 
        centralWidget.setLayout(self.mainLayout_)  

        self.setUpLayout_ = QFormLayout() 
        self.mainLayout_.addLayout(self.setUpLayout_, 0, 0)

        self.onlyInt_ = QIntValidator()
        

        self.rows_ = QLineEdit(self)
        self.rows_.setValidator(self.onlyInt_)
        self.setUpLayout_.addRow("Rows: ", self.rows_)
        self.cols_ = QLineEdit(self)
        self.cols_.setValidator(self.onlyInt_)
        self.setUpLayout_.addRow("Cols: ", self.cols_)
        self.bmbs_ = QLineEdit(self)
        self.bmbs_.setValidator(self.onlyInt_)
        self.setUpLayout_.addRow("Bombs: ", self.bmbs_)

        self.newGame_ = QPushButton("New Game")
        self.mainLayout_.addWidget(self.newGame_, 1, 0)

        self.mf_ = QGridLayout()
        self.mainLayout_.addLayout(self.mf_, 2, 0)

        self.newGame_.clicked.connect(self.newGame)

        self.st_ = QLabel(self.model_.st_.name)
        self.mainLayout_.addWidget(self.st_, 3, 0)

    def newGame(self):
        rows = 0
        if (self.rows_.text()):
            rows = int(self.rows_.text())
        cols = 0
        if (self.cols_.text()):
            cols = int(self.cols_.text())
        bmbs = 0
        if (self.bmbs_.text()):
            bmbs = int(self.bmbs_.text())
        self.model_ = PyMines(rows, cols, bmbs)

        # for ii in range(self.mf_.count()):
        #     self.mf_.itemAt(ii).widget().close()
        for i in reversed(range(self.mf_.count())): 
            widgetToRemove = self.mf_.itemAt(i).widget()
            # remove it from the layout list
            self.mf_.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)
        
        for ii in range(self.model_.rows_):
            for jj in range(self.model_.cols_):
                temp = PyMineSquare_GUI(ii, jj)
                temp.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                temp.leftClick.connect(self.leftClick)
                temp.rightClick.connect(self.rightClick)
                # temp.customContextMenuRequested.connect(temp.emit.)
                self.mf_.addWidget(temp, ii, jj)
        
        self.st_.setText(self.model_.st_.name)

    def leftClick(self, xx, yy) :
        changed = self.model_.click(xx, yy)

        for ii in changed :
            xx = ii[0]
            yy = ii[1]
            self.mf_.itemAtPosition(xx, yy).widget().setText(self.model_.lbl(xx, yy))

        self.st_.setText(self.model_.st_.name)


    def rightClick(self, xx, yy) :
        if self.model_.st_ == STATUS.PLAYING :
            self.model_.toggleFlag(xx, yy)

            self.mf_.itemAtPosition(xx, yy).widget().setText(self.model_.lbl(xx, yy))

    model_ = PyMines(0, 0, 0)
    
    



# zio = PyMines(7, 7, 1)
# zio.set(2, 3)
# print(zio)


app = QtWidgets.QApplication(sys.argv)
mainWin = PyMines_GUI()
mainWin.show()
sys.exit( app.exec_() )





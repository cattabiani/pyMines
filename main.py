import sys
import random
import numpy
from enum import Enum

class PyMines():
    class STATUS(Enum):
        PLAYING = 0
        LOST = 1
        WON = 2
        NOTSET = 3
        


    def __init__(self, rows, cols, bmbs):
        if rows*cols > bmbs and rows >0 and cols > 0 and bmbs > 0 :
            self.rows_ = rows
            self.cols_ = cols
            self.bmbs_ = bmbs
            self.disc_ = 0
            self.st_ = self.STATUS.NOTSET
            self.brd_ = []
            self.vbrd_ = []


    def ck(self, xx, yy):
        return xx >= 0 and yy >= 0 and xx < self.rows_ and yy < self.cols_

    def set(self, xx, yy):
        if self.ck(xx, yy) and not self.brd_ :
            temp = [-1]*self.bmbs_ + [0]*(self.rows_*self.cols_-self.bmbs_-1)
            random.shuffle(temp)
            temp.insert(xx*self.cols_ + yy, 0)
            self.brd_ = numpy.array(temp)
            self.brd_ = self.brd_.reshape([self.rows_, self.cols_])
            self.setNeighbours()
            self.vbrd_ = -numpy.ones([self.rows_, self.cols_], dtype=int)
            self.st_ = self.STATUS.PLAYING
            self.disc_ = 0

            self.click(xx, yy)
    
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
        if self.st_ == self.STATUS.PLAYING and self.ck(xx, yy) :
            if self.vbrd_[xx][yy] == -1:
                self.vbrd_[xx][yy] = -2
            elif self.vbrd_[xx][yy] == -2:
                self.vbrd_[xx][yy] = -1

    def click(self, xx, yy) :
        lst = [[xx, yy]]
        if self.st_ == self.STATUS.PLAYING and self.ck(xx, yy) and self.vbrd_[xx][yy] == -1:
            lst.append([xx, yy])

        while lst :
            elem = lst.pop(0)
            xx = elem[0]
            yy = elem[1]

            if self.brd_[xx][yy] == -1 :
                self.st_ = self.STATUS.LOST
                break
            else :
                self.vbrd_[xx][yy]  = self.brd_[xx][yy]
                self.disc_ += 1
                if self.disc_ + self.bmbs_ >= self.rows_*self.cols_ :
                    self.st_ = self.STATUS.WON
                    break
                elif self.vbrd_[xx][yy] == 0 :
                    for ii in range(-1, 2) :
                        for jj in range(-1, 2) :
                            nxx = xx + ii
                            nyy = yy + jj
                            if self.ck(nxx, nyy) and self.vbrd_[nxx][nyy] == -1:
                                lst.append([nxx,nyy])
                                self.vbrd_[nxx][nyy] = -2


    def __str__(self):
        temp = "Rows: " + str(self.rows_) + "\n"
        temp += "Cols: " + str(self.cols_) + "\n"
        temp += "Bmbs: " + str(self.bmbs_) + "\n"
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
    
    


zio = PyMines(3, 4, 2)
zio.set(2, 3)


print(zio)





from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox
from math import sqrt
import time

alg_flag = 0                                # Algorithm of drawing lines. 0 - Async DDA; 1 - Bresenham's line algorithm
pixel = 20
offset = 100


def isNegative(num):
    if num<0:
        return -1
    else:
        return 1

class DrawAlgos(QWidget):

    def __init__(self):
        super().__init__()
        self.shape = 'triangle'
        self.cb_list = []
        self.initUI()

    def initUI(self):


        cb1 = QCheckBox('triangle', self)
        cb1.move(20, 20)
        cb1.toggle()
        cb1.stateChanged.connect(self.changeShape)
        self.cb_list.append(cb1)

        cb2 = QCheckBox('square', self)
        cb2.move(20, 40)
        cb2.stateChanged.connect(self.changeShape)
        self.cb_list.append(cb2)

        cb3 = QCheckBox('hexagon', self)
        cb3.move(20, 60)
        cb3.stateChanged.connect(self.changeShape)
        self.cb_list.append(cb3)


        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('QCheckBox')
        self.show()

    def changeShape(self, state):
        if state == Qt.Checked:
            for cb in self.cb_list:
                if(cb != self.sender()):
                    cb.setChecked(False)
                else:
                    cb.setChecked(True)
            self.shape = self.sender().text()
            self.update()


    def paintEvent(self, event):            # Overriding this method allows to carry redrawing while resizing
        width = self.size().width()
        height = self.size().height()
        painter = QPainter(self)
        pen = QPen(Qt.black)
        pen.setWidth(pixel)
        painter.setPen(pen)

        shapes = {
            'triangle':
                    (
                        (width//2, offset),         # We can choose what kind of figure
                        (offset, height-offset),        # we want to draw by setting up the
                        (width-offset, height-offset),  # tuple of coordinates (tuples). Here it's triangle.
                    ),
            'square':
                    (
                        (offset, offset),
                        (width-offset, offset),
                        (width-offset, height-offset),
                        (offset, height-offset),
                    ),
            'hexagon':
                (
                    (20, 20),
                    (width - 20, 20),
                    (20, height - 20),
                    (width - 20, height - 20),

                )

        }

        points = shapes[self.shape]
        for i in range(len(points)):
            dx = points[(i + 1) % len(points)][0] - points[i][0]       # Calculate dx, dy and watch out of being
            dy = points[(i + 1) % len(points)][1] - points[i][1]        # out of range!

            direction = 0                   # Direction flag: 0 is y and 1 is x
            d = 0
            if(not dx):
                d = 0
                direction = 0
            if(not dy):
                d = 0
                direction = 1
            elif(abs(dx) >= abs(dy)):
                d = abs(dy/dx)
                direction = 1
            else:
                d = abs(dx/dy)
                direction = 0
            (x1, y1) = points[i]
            (x2, y2) = points[(i + 1) % len(points)]
            while(True):

                painter.drawPoint(round(x1), round(y1))
                increment = 1
                if(direction):
                        x1 += increment*pixel*isNegative(dx)
                        y1 += d*pixel*isNegative(dy)
                else:
                        y1 += increment*pixel*isNegative(dy)
                        x1 += d*pixel*isNegative(dx)
                if(sqrt((x1-x2)**2 + (y1-y2)**2) < pixel):      # here we add one more pixel to the tail
                    painter.drawPoint(round(x1), round(y1))     # so the line is not interrupted
                    break






if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = DrawAlgos()
    w.show()
    sys.exit(app.exec_())
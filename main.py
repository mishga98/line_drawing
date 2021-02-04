from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox
from math import sqrt
import time

pixel = 20
offset = 100


def isNegative(num):
    if num < 0:
        return -1
    else:
        return 1


class DrawAlgos(QWidget):

    def __init__(self):
        super().__init__()
        self.shape = 'triangle'
        self.cb_shapes_list = []
        self.cb_algs_list = []
        self.alg_flag = 0  # Algorithm of drawing lines. 0 - Async DDA; 1 - Bresenham's line algorithm
        self.initUI()

    def initUI(self):

        cb1 = QCheckBox('triangle', self)
        cb1.move(20, 20)
        cb1.toggle()
        cb1.stateChanged.connect(self.changeShape)
        self.cb_shapes_list.append(cb1)

        cb2 = QCheckBox('square', self)
        cb2.move(20, 40)
        cb2.stateChanged.connect(self.changeShape)
        self.cb_shapes_list.append(cb2)

        cb3 = QCheckBox('octagon', self)
        cb3.move(20, 60)
        cb3.stateChanged.connect(self.changeShape)
        self.cb_shapes_list.append(cb3)

        cb4 = QCheckBox('ADDA', self)
        cb4.move(120, 20)
        cb4.toggle()
        cb4.stateChanged.connect(self.changeAlg)
        self.cb_algs_list.append(cb4)

        cb5 = QCheckBox('Bresenham', self)
        cb5.move(120, 40)
        cb5.stateChanged.connect(self.changeAlg)
        self.cb_algs_list.append(cb5)

        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('QCheckBox')
        self.show()

    def changeShape(self, state):
        if state == Qt.Checked:
            for cb in self.cb_shapes_list:
                if (cb != self.sender()):
                    cb.setChecked(False)
                else:
                    cb.setChecked(True)
            self.shape = self.sender().text()
            self.update()

    def changeAlg(self, state):
        if state == Qt.Checked:
            for cb in self.cb_algs_list:
                if (cb != self.sender()):
                    cb.setChecked(False)
                else:
                    cb.setChecked(True)
            if (self.sender().text() == "ADDA"):
                self.alg_flag = 0
            else:
                self.alg_flag = 1
            self.update()

    def paintEvent(self, event):  # Overriding this method allows to carry redrawing while resizing
        width = self.size().width()
        height = self.size().height()
        painter = QPainter(self)
        pen = QPen(Qt.black)
        pen.setWidth(pixel)
        painter.setPen(pen)

        shapes = {
            'triangle':
                (
                    (width // 2, offset),  # We can choose what kind of figure
                    (offset, height - offset),  # we want to draw by setting up the
                    (width - offset, height - offset),  # tuple of coordinates (tuples). Here it's triangle.
                ),
            'square':
                (
                    (offset, offset),
                    (width - offset, offset),
                    (width - offset, height - offset),
                    (offset, height - offset),
                ),
            'octagon':
                (
                    (offset + 100, offset + 100),
                    (offset + 100 + 50 * width / 200, offset + 100),
                    (offset + 100 + 75 * width / 200, offset + 100 + 25 * width / 200),
                    (offset + 100 + 75 * width / 200, offset + 100 + 75 * width / 200),
                    (offset + 100 + 50 * width / 200, offset + 100 + 100 * width / 200),
                    (offset + 100, offset + 100 + 100 * width / 200),
                    (offset + 100 - 25 * width / 200, offset + 100 + 75 * width / 200),
                    (offset + 100 - 25 * width / 200, offset + 100 + 25 * width / 200),
                )

        }

        points = shapes[self.shape]

        # >--------------------- ADDA started here -------------------------------------------------------------<
        if not self.alg_flag:
            for i in range(len(points)):
                dx = points[(i + 1) % len(points)][0] - points[i][0]  # Calculate dx, dy and watch out of being
                dy = points[(i + 1) % len(points)][1] - points[i][1]  # out of range!

                direction = 0  # Direction flag: 0 is y and 1 is x
                d = 0
                if (not dx):
                    d = 0
                    direction = 0
                if (not dy):
                    d = 0
                    direction = 1
                elif (abs(dx) >= abs(dy)):
                    d = abs(dy / dx)
                    direction = 1
                else:
                    d = abs(dx / dy)
                    direction = 0
                (x1, y1) = points[i]
                (x2, y2) = points[(i + 1) % len(points)]

                while (True):
                    painter.drawPoint(round(x1), round(y1))
                    increment = 1
                    if (direction):
                        x1 += increment * pixel * isNegative(dx)  # isNegative() result helps to carry direction
                        y1 += d * pixel * isNegative(dy)
                    else:
                        y1 += increment * pixel * isNegative(dy)
                        x1 += d * pixel * isNegative(dx)
                    if (sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < pixel):  # here we add one more pixel to the tail
                        painter.drawPoint(round(x1), round(y1))  # so the line is not interrupted
                        break
        # >--------------------- ADDA end ----------------------------------------------------------------------<

        # >--------------------- Bresenham started here --------------------------------------------------------<
        else:
            for i in range(len(points)):
                [(ax, ay), (bx, by)] = sorted([points[(i + 1) % len(points)], points[i]], key=lambda a: a[1])
                delta_x = bx - ax
                delta_y = by - ay
                if delta_x >= 0:
                    dx = 1
                else:
                    dx = -1
                    delta_x *= -1
                d = 0
                if delta_y >= delta_x:
                    t = 2 * delta_x
                    delta = 2 * delta_y
                else:
                    t = 2 * delta_y
                    delta = 2 * delta_x
                if delta_y >= delta_x:
                    while abs(ay-by)>pixel:
                        painter.drawPoint(ax, ay)
                        ay += 1*pixel
                        d += t
                        if d > delta_y:
                            ax += dx*pixel
                            d -= delta
                    painter.drawPoint(ax, ay)
                else:
                    while abs(ax-bx)>pixel:
                        painter.drawPoint(ax, ay)
                        ax += 1*dx*pixel
                        d += t
                        if d > delta_x:
                            ay += 1*pixel
                            d -= delta
                    painter.drawPoint(ax, ay)

        # >--------------------- Bresenham end here --------------------------------------------------------<


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = DrawAlgos()
    w.show()
    sys.exit(app.exec_())

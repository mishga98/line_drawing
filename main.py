from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget
from math import sqrt
import time

alg_flag = 0                                # Algorithm of drawing lines. 0 - Async DDA; 1 - Bresenham's line algorithm
pixel = 20


def isNegative(num):
    if num<0:
        return -1
    else:
        return 1

class DrawAlgos(QWidget):

    def paintEvent(self, event):            # Overriding this method allows to carry redrawing while resizing
        width = self.size().width()
        height = self.size().height()
        painter = QPainter(self)
        pen = QPen(Qt.black)
        pen.setWidth(pixel)
        painter.setPen(pen)

        points = (
                    (width//2, 20),         # We can choose what kind of figure
                    (20, height-20),        # we want to draw by setting up the
                    (width-20, height-20),  # tuple of coordinates (tuples). Here it's triangle.
                 )
        points = (
                    (20, 20),
                    (width - 20, 20),
                    (width - 20, height - 20),
                    (20, height-20),


                 )

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
            while(sqrt((x1-x2)**2 + (y1-y2)**2) >= pixel):

                painter.drawPoint(round(x1), round(y1))
                increment = 1
                if(direction):
                        x1 += increment*pixel*isNegative(dx)
                        y1 += d*pixel*isNegative(dy)
                else:
                        y1 += increment*pixel*isNegative(dy)
                        x1 += d*pixel*isNegative(dx)
                print('direction', direction)
                print('x1:', x1, 'x2:', x2)
                print('y1:', y1, 'y2:', y2)
                print('dx:', dx, 'dy:', dy)
                #print('d', d)




if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = DrawAlgos()
    w.show()
    sys.exit(app.exec_())
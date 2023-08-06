#!/usr/bin/env python3

from cxwidgets.aQt.QtCore import QTimer, Qt, QSize, pyqtSlot, pyqtProperty, QLineF, QPointF
from cxwidgets.aQt.QtGui import QPalette, QColor, QPainter, QRadialGradient, QBrush, QPicture, QPen, QFont
from cxwidgets.aQt.QtWidgets import QWidget, QApplication


class BPMWidget(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.x_size, self.y_size = 200, 200
        self.dark_mode = True
        self.draw_aperture = True
        self.draw_grid = True
        self.n_gridlines = 2  # number per side from cross-lines
        self.fill_bg = True
        self.draw_cross = True
        self.cross_by_doubleclick = True

        # apertures, mm
        self.ax, self.ay = 20.0, 20.0
        # beam coordinates, mm
        self.x = None
        self.y = None
        # cross coordinates in mm
        self.cross_x = 0
        self.cross_y = 0

        # beam picture radius
        self.r = 12

        self.l_color, self.al_color, self.bg_color, self.l_pen, self.al_pen = None, None, None, None, None
        self.updateColors()
        self.beam_color = QColor(255, 165, 0)   # orange
        self.cross_pen = QPen(QColor('#ff00ff'))

        self.base_picture, self.beam_picture, self.cross_picture = None, None, None
        self.painter = QPainter()
        self.generateBasePicture()
        self.generateBeamPicture()
        self.generateCrossPicture()
        self.setBeamPos(0, 0)

    # coordinate system transforms
    def x2xp(self, x):
        return int((self.x_size / 2) * (1 + x / self.ax))

    def y2yp(self, y):
        return int((self.y_size / 2) * (1 - y / self.ay))

    def xp2x(self, xp):
        return (xp * (2 / self.x_size) - 1) * self.ax

    def yp2y(self, yp):
        return -1 * (yp * (2 / self.y_size) - 1) * self.ay

    def updateColors(self):
        if self.dark_mode:
            self.l_color = QColor(0, 200, 0)
            self.al_color = self.l_color.darker(220)
            self.bg_color = QColor('#000000')
        else:
            self.l_color = QColor(100, 100, 100)
            self.al_color = self.l_color.lighter(200)
            self.bg_color = QColor('#d0f0d0')

        # pal = QPalette()
        # pal.setColor(QPalette.Window, self.bg_color)
        self.l_pen = QPen(self.l_color)
        self.al_pen = QPen(self.al_color)
        self.al_pen.setStyle(Qt.DashLine)

    def generateBeamPicture(self):
        pic = QPicture()
        p = self.painter
        p.begin(pic)
        r = self.r
        gradient = QRadialGradient(QPointF(r, r), r)
        gradient.setColorAt(0, self.beam_color)
        gradient.setColorAt(1, self.bg_color)
        brush = QBrush(gradient)
        pen = QPen(self.bg_color)
        pen.setStyle(Qt.NoPen)
        p.setPen(pen)
        p.setBrush(brush)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.drawEllipse(0, 0, 2 * r, 2 * r)
        p.end()
        self.beam_picture = pic

    def generateCrossPicture(self):
        pic = QPicture()
        p = self.painter
        p.begin(pic)
        r = self.r
        p.setPen(self.cross_pen)
        ls = [QLineF(r, 0, r, 2 * r), QLineF(0, r, 2*r, r)]
        p.drawLines(ls)
        p.end()
        self.cross_picture = pic

    def generateBasePicture(self):
        pic = QPicture()
        p = self.painter
        p.begin(pic)
        p.setPen(self.bg_color)
        def_brush = p.brush()
        if self.fill_bg:
            p.setBrush(self.bg_color)
        p.drawRect(0, 0, self.x_size, self.y_size)

        p.setPen(self.l_pen)
        p.setBrush(def_brush)
        # draw central cross
        sx_2 = self.x_size/2
        sy_2 = self.y_size/2
        x_lines = [QLineF(sx_2, 0, sx_2, self.y_size), QLineF(0, sy_2, self.x_size, sy_2)]
        p.drawLines(x_lines)

        p.setFont(QFont("Times", 8,))
        p.drawText(int(self.x_size/2) + 3, 10, f'{self.ay:.0f}')
        p.drawText(self.x_size - 15, int(self.y_size/2) + 10, f'{self.ax:.0f}')

        # draw apperture if needed
        if self.draw_aperture:
            p.drawEllipse(0, 0, self.x_size, self.y_size)

        if self.draw_grid:
            p.setPen(self.al_pen)
            grid_lines = []
            gx_step = sx_2 / (self.n_gridlines + 1)
            gy_step = sy_2 / (self.n_gridlines + 1)
            for i in range(self.n_gridlines):
                grid_lines.append(QLineF((i+1)*gx_step, 0, (i+1)*gx_step, self.y_size))
                grid_lines.append(QLineF(sx_2 + (i+1)*gx_step, 0, sx_2 + (i+1)*gx_step, self.y_size))

                grid_lines.append(QLineF(0, (i+1)*gy_step, self.x_size, (i+1)*gy_step))
                grid_lines.append(QLineF(0, sy_2 + (i+1)*gy_step, self.x_size, sy_2 + (i+1)*gy_step))

            p.drawLines(grid_lines)
        p.end()
        self.base_picture = pic

    def paintEvent(self, event):
        p = self.painter
        p.begin(self)
        p.drawPicture(0, 0, self.base_picture)
        p.drawPicture(self.x2xp(self.x) - self.r, self.y2yp(self.y) - self.r, self.beam_picture)
        p.drawPicture(self.x2xp(self.cross_x) - self.r, self.y2yp(self.cross_y) - self.r, self.cross_picture)
        p.end()

    def resizeEvent(self, event):
        sx = event.size().width()
        sy = event.size().height()
        if self.x_size != sx or self.y_size != sy:
            self.x_size = sx
            self.y_size = sy
            self.generateBasePicture()
            self.update()

    def heightForWidth(self, w):
        return w * self.ay / self.ax

    def mouseDoubleClickEvent(self, event):
        if self.draw_cross and self.cross_by_doubleclick:
            event.accept()
            ev_xp = event.x()
            ev_yp = event.y()
            self.setCrossPos(self.xp2x(ev_xp), self.yp2y(ev_yp))
        else:
            event.ignore()

    def minimumSizeHint(self):
        return QSize(100, 100)

    def sizeHint(self):
        return QSize(self.x_size, self.y_size)

    @pyqtProperty(bool)
    def darkMode(self):
        return self.dark_mode

    @darkMode.setter
    def darkMode(self, mode):
        self.dark_mode = mode
        self.updateColors()
        self.generateBasePicture()
        self.generateBeamPicture()
        self.update()

    @pyqtProperty(bool)
    def drawAperture(self):
        return self.draw_aperture

    @drawAperture.setter
    def drawAperture(self, da):
        self.draw_aperture = da
        self.generateBasePicture()
        self.update()

    @pyqtProperty(bool)
    def drawGrid(self):
        return self.draw_grid

    @drawGrid.setter
    def drawGrid(self, dg):
        self.draw_grid = dg
        self.generateBasePicture()
        self.update()

    @pyqtProperty(int)
    def nGridLines(self):
        return self.n_gridlines

    @nGridLines.setter
    def nGridLines(self, n):
        self.n_gridlines = n
        self.generateBasePicture()
        self.update()

    @pyqtProperty(QColor)
    def beamColor(self):
        return self.beam_color

    @beamColor.setter
    def beamColor(self, col):
        self.beam_color = col
        self.generateBeamPicture()
        self.update()

    @pyqtProperty(QColor)
    def crossColor(self):
        return self.cross_pen.color()

    @crossColor.setter
    def crossColor(self, col):
        self.cross_pen.setColor(col)
        self.generateCrossPicture()
        self.update()

    @pyqtProperty(bool)
    def fillBg(self):
        return self.fill_bg

    @fillBg.setter
    def fillBg(self, fb):
        self.fill_bg = fb
        self.generateBasePicture()
        self.update()

    @pyqtProperty(float)
    def Ax(self):
        return self.ax

    @Ax.setter
    def Ax(self, a):
        self.ax = a

    @pyqtProperty(float)
    def Ay(self):
        return self.ay

    @Ay.setter
    def Ay(self, a):
        self.ay = a

    @pyqtSlot(float, float)
    def setBeamPos(self, x, y):
        if self.x != x or self.y != y:
            self.x = x
            self.y = y
            self.update()

    def getBeamX(self):
        return self.x

    @pyqtSlot(float)
    def setBeamX(self, x):
        if self.x != x:
            self.x = x
            self.update()

    beamX = pyqtProperty(float, getBeamX, setBeamX)

    def getBeamY(self):
        return self.y

    @pyqtSlot(float)
    def setBeamY(self, y):
        if self.y != y:
            self.y = y
            self.update()

    beamY = pyqtProperty(float, getBeamY, setBeamY)

    @pyqtSlot(float, float)
    def setCrossPos(self, x, y):
        if self.cross_x != x or self.cross_y != y:
            self.cross_x = x
            self.cross_y = y
            self.update()


if __name__ == "__main__":
    import sys

    app = QApplication(['test'])
    w = BPMWidget()
    w.show()
    sys.exit(app.exec_())

# This Python file uses the following encoding: utf-8
import os
import sys
from matplotlib import image
import tensorflow as tf
from PIL import Image
import numpy as np
from drt_telea import telea
from drt_unet import UNet


from PySide2.QtCore import (
    QSize,
    QPoint,
    QDir, 
    QFile,
    Qt
)
from PySide2.QtWidgets import (
    QMainWindow, 
    QApplication, 
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QPushButton, 
    QLabel,
    QAction,
    QActionGroup,
    QToolBar
    
)

from PySide2.QtGui import (
    QPixmap,
    QPainter,
    QColor,
    QImage,
    QCursor,
    QIcon,
    QBrush,
    QPen
)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.model = UNet()
        self.model_path = self.getPathToModel()
        self.model.loadModel(self.model_path)
        
        self.setWindowTitle("Фото реставратор")
        

        self.inputImage = QLabel()
        self.transparent = QLabel(parent=self.inputImage)
        self.outputImage = QLabel()
    
        self.drawing, self.erasing = False, False
        self.brushSize = 4
        self.brushColor = Qt.red
        self.eraserColor = Qt.transparent
        self.last_x, self.last_y = None, None
        self.pred_mask, self.image = None, None

        menuBar = self.menuBar()
        
        menu = menuBar.addMenu("Меню")
        
        self.open_action = menu.addAction("Открыть")
        self.open_action.triggered.connect(self.getPathToImage)

        self.start_action = menu.addAction("Автоматическое восстановление")
        self.start_action.triggered.connect(self.createMask)
        self.start_action.setDisabled(True)
        
        self.mask_action = menu.addAction("Ручное восстановление")
        self.mask_action.triggered.connect(self.getMaskfFromUI)
        self.mask_action.setDisabled(True)
        
        self.save_action = menu.addAction("Сохранить")
        self.save_action.triggered.connect(self.saveFile)
        self.save_action.setDisabled(True)

        brush_size = menuBar.addMenu("Размер &кисти")

        pix_4 = QAction("4px", self)
        brush_size.addAction(pix_4)
        pix_4.triggered.connect(self.Pixel_4)

        pix_7 = QAction("7px", self)
        brush_size.addAction(pix_7)
        pix_7.triggered.connect(self.Pixel_7)

        pix_9 = QAction("9px", self)
        brush_size.addAction(pix_9)
        pix_9.triggered.connect(self.Pixel_9)

        pix_12 = QAction("12px", self)
        brush_size.addAction(pix_12)
        pix_12.triggered.connect(self.Pixel_12)

        layout = QHBoxLayout()

        layout.addWidget(self.inputImage)
        layout.addWidget(self.outputImage)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        vert_layout = QHBoxLayout()

        vert_layout.addWidget(self.transparent)
        self.transparent.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.inputImage.setLayout(vert_layout)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)

        self.pencil_action = QAction(QIcon("pencil.png"), "Your button", self)
        self.pencil_action.triggered.connect(self.paint)
        self.pencil_action.setCheckable(True)
        toolbar.addAction(self.pencil_action)

        self.eraser_action = QAction(QIcon("eraser.png"), "Your button", self)
        self.eraser_action.triggered.connect(self.erase)
        self.eraser_action.setCheckable(True)
        toolbar.addAction(self.eraser_action)
        
    def getPathToImage(self):
        self.open_path, _ = QFileDialog.getOpenFileName(
            self,
            'Open image',
            QDir.currentPath(),
            'Image files (*.jpg *.png *.jpeg)'
        )
        if self.open_path != None or self.open_path != '':
            self.image = np.asarray(Image.open(self.open_path))
            self.displayImage()
            
    def displayImage(self):
        self.dispImage = QImage(self.open_path)
        print(self.dispImage.size())
        self.pixmapImage = QPixmap.fromImage(self.dispImage)
        
        self.inputImage.resize(self.dispImage.width(), self.dispImage.height())
        self.inputImage.setPixmap(self.pixmapImage)

        self.transparent.resize(self.dispImage.width(), self.dispImage.height())
        self.pixmapMask = QPixmap(self.pixmapImage.size())
        self.pixmapMask.fill(QColor(0, 0, 0, 0))
        self.transparent.setPixmap(self.pixmapMask)
        
        self.outputImage.resize(self.pixmapImage.size())
        
        # self.setGeometry(, 0, 2 * self.dispImage.width(), self.dispImage.height())
        self.setFixedSize(2 * self.dispImage.width(), self.dispImage.height())
        
        self.start_action.setDisabled(False)
        self.mask_action.setDisabled(False)

        print(self.dispImage.size())

    def getPathToModel(self):
        for p in sys.path:
             if os.path.isdir(p):
                 for f in os.listdir(p):
                     if f == 'drt_unet':
                         return os.path.join(p, f, 'models')

    def saveFile(self):
        file_path = QFileDialog.getSaveFileName(
            self,
            'Save image',
            QDir.currentPath(),
            'Image files (*.jpg *.png *.jpeg)'
        )
        if file_path != None and file_path != "":
            tmp = self.outputImage.pixmap().toImage()
            tmp.save("test.png")  
    
    def imageRestoration(self):

        print(type(self.image), type(self.pred_mask))

        telea.inpaint(self.image, self.pred_mask)

        self.image = np.squeeze(self.image)
        self.image = np.ceil(self.image).astype(np.uint8)

        height, width, _ = self.image.shape    
        bytesPerLine = 3 * width
        q_img = QImage(self.image, width, height, bytesPerLine, QImage.Format_RGB888)
        self.outputImage.setPixmap(QPixmap(q_img))

        self.save_action.setDisabled(False)

    def createMask(self):
        self.image = self.image.astype(np.float16)
        x = tf.reshape(self.image, (1, self.image.shape[0], self.image.shape[1], self.image.shape[2]))
        tensor = tf.data.Dataset.from_tensors(x)
        
        predicted_mask = self.model.predict(tensor, batch_size=1)
        
        self.image = np.ceil(self.image).astype(np.uint8)       
        
        predicted_mask = np.round(predicted_mask).astype(np.float16)
        
        self.pred_mask = np.squeeze(predicted_mask)
        self.pred_mask = np.ceil(self.pred_mask * 255.).astype(np.uint8)      
       
        for x in range(self.pred_mask.shape[0]):
            for y in range(self.pred_mask.shape[1]):
                if self.pred_mask[x][y] == 255:
                    self.pred_mask[x][y] = 0
                else:
                    self.pred_mask[x][y] = 255

        self.pred_mask = self.pred_mask // 255
        self.pred_mask = np.round(self.pred_mask).astype(np.float16)
        
        self.imageRestoration()

    def getMaskfFromUI(self):
                
        tmp = self.transparent.pixmap().toImage() 
        tmp_array = np.ndarray(shape=(tmp.height(),tmp.width()), dtype=float)
        for x in range(tmp.width()):
            for y in range(tmp.height()):
                if tmp.pixel(x, y) == QColor(255, 0, 0).rgb():
                    tmp.setPixel(x, y, QColor(255, 255, 255).rgb())
                    tmp_array[y][x] = 1
                else:
                    tmp.setPixel(x, y, QColor(0, 0, 0).rgb())
                    tmp_array[y][x] = 0

        img = self.image
        # msk = tmp_array * 255.
        mask = tmp_array

        print(mask)
        telea.inpaint(img, mask)
        
        img = np.squeeze(img)
        img = np.ceil(img).astype(np.uint8)

        height, width, _ = img.shape    
        bytesPerLine = 3 * width
        q_img = QImage(img, width, height, bytesPerLine, QImage.Format_RGB888)

        self.outputImage.setPixmap(QPixmap(q_img))

        self.save_action.setDisabled(False)

    def mouseMoveEvent(self, event):
        
        if self.drawing == None and self.erasing == None:
            return

        if self.drawing == False and self.erasing == False:
            return

        qp = self.transparent.mapFromGlobal(QCursor.pos())

        if self.last_x is None:
            self.last_x, self.last_y = qp.x(), qp.y()
            return

        image = self.transparent.pixmap().toImage()
        
        painter = QPainter()
        painter.begin(image)
        if self.drawing:
            color = self.brushColor
        else:
            color = self.eraserColor

        painter.setPen(QPen(color, self.brushSize,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))    

        image.setPixel(self.last_x, self.last_y, self.brushColor)
        painter.drawLine(self.last_x, self.last_y, qp.x() , qp.y())

        self.transparent.setPixmap(QPixmap.fromImage(image))

        painter.end()
        
        self.update()

        self.last_x, self.last_y = qp.x(), qp.y()

    def mouseReleaseEvent(self, event):
        self.last_x = None
        self.last_y = None
    
    def Pixel_4(self):
        self.brushSize = 4

    def Pixel_7(self):
        self.brushSize = 7

    def Pixel_9(self):
        self.brushSize = 9

    def Pixel_12(self):
        self.brushSize = 12

    def paint(self):
        if self.drawing == True:
            self.drawing = False
        else:
            self.drawing = True

    def erase(self):
        if self.erasing == True:
            self.erasing = False
        else:
            self.erasing = True

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

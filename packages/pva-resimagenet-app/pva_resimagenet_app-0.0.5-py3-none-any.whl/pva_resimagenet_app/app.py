import os
import sys

from skimage import io, color
from skimage.transform import resize
from skimage.util import img_as_ubyte

import torch

from PySide2.QtCore import Qt, QSize, QThread, Signal
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QLabel,
    QWidget,
    QFileDialog,
)
from PySide2.QtGui import QImage, QPixmap, QColor, QMovie

from pva_resimagenet import ResImageNet

class ImageProcessThread(QThread):
    processComplete = Signal(torch.Tensor)

    def __init__(self, model, image):
        super().__init__()
        self.model = model
        self.image = image

    def run(self):
        image_out = self.model(self.image)
        self.processComplete.emit(image_out)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = ResImageNet(device="cpu", pretrained=True)
        self.image_in_arr = None
        self.image_out_arr = None

        self.setWindowTitle("ResImage")
        self.setMinimumSize(QSize(800, 500))

        menu_bar = self.menuBar()

        menu = menu_bar.addMenu("Меню")
        self.open_action = menu.addAction("Открыть файл...")
        self.open_action.triggered.connect(self.openFile)
        self.start_action = menu.addAction("Восстановить изображение")
        self.start_action.triggered.connect(self.processImage)
        self.start_action.setDisabled(True)
        self.save_action = menu.addAction("Сохранить изображение в файл...")
        self.save_action.triggered.connect(self.saveImage)
        self.save_action.setDisabled(True)

        menu_bar.addAction("О программе")

        layout = QHBoxLayout()

        self.image_in = QLabel()
        self.image_in.setScaledContents(True)
        self.image_out = QLabel()
        self.image_out.setScaledContents(True)

        imout_layout = QHBoxLayout()
        self.movie_label = QLabel(parent=self.image_out)
        imout_layout.addWidget(self.movie_label)
        self.movie_label.setAlignment(Qt.AlignCenter)
        self.image_out.setLayout(imout_layout)
        self.movie = QMovie(os.path.join(os.path.dirname(__file__), "data", "load_icon.gif"))
        self.movie.setScaledSize(QSize(200, 200))

        layout.addWidget(self.image_in)
        layout.addWidget(self.image_out)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
    
    def openFile(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберете изображение", os.getcwd(),
                                                "Изображения (*.jpeg *.jpg *.jpe *.jfif *.png *.bmp)")
        if file_name != None and file_name != "":

            self.image_in.clear()
            self.image_out.clear()

            self.image_in_arr = io.imread(file_name)

            # RGBA/RGB to Gray conversion
            if len(self.image_in_arr.shape) > 2:
                if self.image_in_arr.shape[2] > 3:
                    self.image_in_arr = color.rgba2rgb(self.image_in_arr)
                    self.image_in_arr = color.rgb2gray(self.image_in_arr)
                elif self.image_in_arr.shape[2] == 3:
                    self.image_in_arr = color.rgb2gray(self.image_in_arr)

            image_in = img_as_ubyte(self.image_in_arr.copy())

            height, width = image_in.shape
            bytes_per_line = 1 * width
            qimage_in = QImage(image_in, width, height, bytes_per_line, QImage.Format_Grayscale8)
            self.image_in.setPixmap(QPixmap(qimage_in))

            tmp_pix = QPixmap(width, height)
            tmp_pix.fill(QColor(200, 200, 200))
            self.image_out.setPixmap(tmp_pix)

            self.start_action.setDisabled(False)

    def processImage(self):
        if self.image_in_arr is not None:
            #Show load icon while waiting for end of process
            self.movie_label.setMovie(self.movie)
            self.movie.start()

            self.thr = ImageProcessThread(self.model, self.image_in_arr)
            self.thr.processComplete.connect(self.processComplete)
            self.thr.start()
    
    def processComplete(self, arr):
        self.movie_label.clear()

        image_out = arr

        image_out = image_out.squeeze().numpy()
        self.image_out_arr = img_as_ubyte(image_out)

        height, width = self.image_out_arr.shape
        bytes_per_line = 1 * width
        qimage_out = QImage(self.image_out_arr, width, height, bytes_per_line, QImage.Format_Grayscale8)
        self.image_out.setPixmap(QPixmap(qimage_out))

        self.save_action.setDisabled(False)

    def saveImage(self):
        dialog_filters = "JPEG (*.jpg *.jpeg *.jpe *.jfif);;PNG (*.png);;BMP (*.bmp)"
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить в...", os.getcwd(),
                                                   dialog_filters)
        if file_name != None and file_name != "":
            io.imsave(file_name, self.image_out_arr)

def app():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    app()
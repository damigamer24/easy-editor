from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QPushButton
import os
from PyQt5.QtGui import QPixmap
from PIL import Image
from PyQt5.QtCore import Qt
from PIL import ImageFilter

app = QApplication([])

my_window = QWidget()
my_window.setWindowTitle("Easy Editor")
my_window.resize(700, 500)

image = QLabel("Image")
btn_folder = QPushButton("Folder")
files = QListWidget()

btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_mirror = QPushButton("Mirror")
btn_sharp = QPushButton("Sharpness")
btn_bw = QPushButton("B/W")


row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_folder)
col1.addWidget(files)

col2.addWidget(image)

row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_mirror)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)

col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
my_window.setLayout(row)

my_window.show()

workdir = ""

def chooseFolder():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filterfiles(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


def showFilenamesList():
    extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
    chooseFolder()
    filenames = filterfiles(os.listdir(workdir), extensions)
    files.clear()
    for filename in filenames:
        files.addItem(filename)

btn_folder.clicked.connect(showFilenamesList)

class ImageEditor:
    def __init__(self):
        self.actual_image = None
        self.filename = None
        self.dir = None
        self.save_dir = "editedimages/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.actual_image = Image.open(image_path)

    def do_left(self):
        self.actual_image = self.actual_image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_right(self):
        self.actual_image = self.actual_image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path) 
    
    def do_mirror(self):
        self.actual_image = self.actual_image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_bw(self):
        self.actual_image = self.actual_image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if os.path.exists(path) == False or os.path.isdir(path) == False:
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.actual_image.save(image_path)

    def do_sharpen(self):
        self.actual_image = self.actual_image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)


    def showImage(self, path):
        image.hide()
        pixmap = QPixmap(path)
        w, h = image.width(), image.height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        image.setPixmap(pixmap)
        image.show()

editor = ImageEditor()

def showChosenImage():
    if files.currentRow() >= 0:
        filename = files.currentItem().text()
        editor.loadImage(workdir, filename)
        image_path = os.path.join(workdir, filename)
        editor.showImage(image_path)
files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(editor.do_bw)
btn_left.clicked.connect(editor.do_left)
btn_right.clicked.connect(editor.do_right)
btn_mirror.clicked.connect(editor.do_mirror)
btn_sharp.clicked.connect(editor.do_sharpen)

app.exec_()
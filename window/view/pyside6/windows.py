from re import T
import sys

from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QGuiApplication, QIcon, QPalette, QColor, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton


def onClickButton():
    print('按钮被按下')


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.centralwidget = QWidget()

        self.pushButton = QPushButton(self.centralwidget)
        self.init()

    def init(self):
        # 设置主窗口的尺寸
        self.resize(640, 480)

        # QRect(x坐标,y坐标，按钮宽度,按钮高度)
        self.pushButton.setGeometry(QRect(1, 1, 100, 50))

        # 设置按钮上文本的字体类型（微软雅黑、宋体...）,尺寸大小，是否斜体
        font1 = QFont()
        font1.setFamilies([u"Microsoft YaHei UI"])
        font1.setPointSize(10)
        font1.setItalic(False)

        self.pushButton.setFont(font1)

        # clicked（bool）只是当按钮的setCheckable()设置为True时才有可能使得status为True
        # （即设置后按钮想点灯开关一样，能够按一下保持一直开，再按下保持一直关），否则开关点击一下后仍为关闭状态，status一直为False
        self.pushButton.setCheckable(False)

        # 设置字体颜色
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, QColor(Qt.black))
        self.pushButton.setPalette(palette)

        # 设置按钮的文本/
        self.pushButton.setText('按钮设置')
        # 设置按钮的图标
        self.pushButton.setIcon(QIcon(r'C:\Users\15516\Desktop\testui\box-color.ico'))

        # 按钮--->连接信号和槽
        self.pushButton.clicked.connect(onClickButton)
    

        self.setCentralWidget(self.centralwidget)

        self.center()

    def center(self):
        # 获取屏幕尺寸坐标
        screen = QGuiApplication.primaryScreen().geometry()

        # 获取主窗口坐标
        size = self.geometry()

        Left = (screen.width() - size.width()) / 2
        Right = (screen.height() - size.height()) / 2

        # 将主窗口移动到电脑屏幕中心位置
        self.move(Left, Right)

def show(title):
    app = QApplication(sys.argv)
    window = Window()
    window.setWindowTitle(title)
    window.show()
    while app.exec():
        pass
    # sys.exit(app.exec())
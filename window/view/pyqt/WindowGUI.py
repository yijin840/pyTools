from PyQt5 import QtWidgets, QtGui
import sys


def show():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    window.show()
    sys.exit(app.exec_())

from PyQt4 import QtGui
import sys
from mainWindow import MyWindowClass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MyWindow = MyWindowClass()
    MyWindow.show()
    sys.exit(app.exec_())

from PyQt4 import QtGui,QtCore
import sys
from mainWindow import MyWindowClass
from systemTrayIcon import SystemTrayIcon

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MyWindow = MyWindowClass()
    MyWindow.show()
    SystemTray = SystemTrayIcon(MyWindow)
    MyWindow.setTray(SystemTray)
    SystemTray.show()
    sys.exit(app.exec_())

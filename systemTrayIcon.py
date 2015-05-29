__ALL__ = ['SystemTrayIcon']

from PyQt4 import QtGui,QtCore
import sys
import os

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        """Icono"""
        self.icon = QtGui.QIcon(
                os.path.join(os.path.dirname(
                    sys.argv[0]),
                    'icons',
                    'icono.jpg'
                )
        )
        QtGui.QSystemTrayIcon.__init__(self, self.icon, parent)
        self.parent = parent
        """Menu system tray icon click derecho"""
        menu = QtGui.QMenu()
        """Las acciones del menu"""
        accionrestaurar = QtGui.QAction('Restaurar', self)
        accionrestaurar.triggered.connect(lambda: self.restaurar())
        menu.addAction(accionrestaurar)
        accionsalir = QtGui.QAction( 'Salir', self)
        accionsalir.triggered.connect(lambda: self.cerrar())
        menu.addAction(accionsalir)
        """establecer el menu"""
        self.setContextMenu(menu)
        """capturar el click en el system tray icon"""
        self.activated.connect(self.ontrayiconactivated)
        """emitir"""
        QtCore.QObject.connect(self,
                           QtCore.SIGNAL('emitir'),
                           self.emitir
                          )

    def ontrayiconactivated(self, reason):
        """3 click izquierdo, 2 doble click, 1 click derecho"""
        if str(reason) == '2':
            self.parent.show()
            self.parent.setWindowState(
                self.parent.windowState() &
                ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive
            )
            self.parent.activateWindow()

    def restaurar(self):
        self.parent.show()

    def cerrar(self):
        self.hide()
        sys.exit()

    def emitir(self,mensaje):
        if self.parent.isVisible() is False:
            self.showMessage('',str(mensaje),2000)
from PyQt4 import QtCore, QtGui
import os,sys


class UserDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        super(UserDialog, self).__init__(parent)
        layout = QtGui.QVBoxLayout(self)
        """title"""
        self.setWindowTitle(' ')
        """Icon """
        self.setWindowIcon(QtGui.QIcon(os.path.join(
            os.path.dirname(sys.argv[0]),
            'icons',
            'icono.jpg'
        )))
        """Flags"""
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        """qlabel usuario"""
        self.labeltbUsu = QtGui.QLabel('Usuario:')
        layout.addWidget(self.labeltbUsu)
        """qlineedit usuario"""
        self.tbUsu = QtGui.QLineEdit()
        layout.addWidget(self.tbUsu)
        """letras y numero, max 15"""
        regexp = QtCore.QRegExp('([a-zA-Z1-9]){1,15}')
        validator = QtGui.QRegExpValidator(regexp)
        self.tbUsu.setValidator(validator)
        """qlabel ip"""
        self.labelIp = QtGui.QLabel('Ip Servidor:')
        layout.addWidget(self.labelIp)
        """qlineedir ip"""
        self.tbIp = QtGui.QLineEdit()
        layout.addWidget(self.tbIp)
        """ip mask"""
        regexpip = QtCore.QRegExp('[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}')
        validatorip = QtGui.QRegExpValidator(regexpip)
        self.tbIp.setValidator(validatorip)
        """Ok button"""
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def usuinsert(self):
        return self.tbUsu.text(),self.tbIp.text()

    @staticmethod
    def getUsu(parent = None):
        dialog = UserDialog(parent)
        dialog.exec_()
        usu, ip = dialog.usuinsert()
        return str(usu),str(ip)

    def closeEvent(self, evnt):
        evnt.ignore()

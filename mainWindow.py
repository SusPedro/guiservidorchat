from PyQt4 import QtCore, QtGui, uic
import os,sys,threading ,socket,thread
from getUsuario import UserDialog
from systemTrayIcon import SystemTrayIcon

form_class = uic.loadUiType(
    os.path.join(os.path.dirname(sys.argv[0]), 'ui', 'mainWindow.ui')
)[0]

tray = None

class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        sys.stderr = file(os.path.join(os.path.dirname(__file__), 'log', 'mainWindow.log'),'a')
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        """icono"""
        self.setWindowIcon(QtGui.QIcon(os.path.join(
            os.path.dirname(sys.argv[0]),
            'icons',
            'icono.jpg'
        )))
        """Conexiones"""
        self.btCon.clicked.connect(self.btconfn)
        self.btEnviar.clicked.connect(self.btenviarfn)
        QtCore.QObject.connect(self.lMensajes,
                               QtCore.SIGNAL('sen'),
                               self.modificar
                               )
        """context menu"""
        self.tbMensaje.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lMensajes.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        """elementos"""
        self.btEnviar.setVisible(False)
        self.tbMensaje.setVisible(False)
        self.txtMensaje.setVisible(False)
        self.lMensajes.setReadOnly(True)
        """solo letras [A-Za-z]"""
        regexp = QtCore.QRegExp('([a-zA-Z1-9+]+\s)*[a-zA-Z1-9+]+$')
        validator = QtGui.QRegExpValidator(regexp)
        self.tbMensaje.setValidator(validator)

    def keyPressEvent(self, event):
        key = event.key()
        """Key_return intro normal, key_enter intro numerico"""
        if key == QtCore.Qt.Key_Enter or key == QtCore.Qt.Key_Return:
            self.btEnviar.click()

    def closeEvent(self, evnt):
        self.hide()
        evnt.ignore()

    def getUsuario(self):
        info= UserDialog.getUsu()
        while(info[0] == ''):
            info = UserDialog.getUsu()
        return info

    def btconfn(self):
        self.s = socket.socket()
        try:
            self.lMensajes.append('conectando')
            self.info = self.getUsuario()
            self.lMensajes.append(str(self.info[0])+' '+str(self.info[1]))
            self.s.connect((str(self.info[1]), 44000))
            self.lMensajes.append('conectado correctamente')
            self.s.send(str(self.info[0]))
            self.r = recibido(self.s,self.lMensajes)
            self.r.setDaemon(True)
            self.r.start()
            self.btEnviar.setVisible(True)
            self.btCon.setVisible(False)
            self.btEnviar.setVisible(True)
            self.tbMensaje.setVisible(True)
            self.txtMensaje.setVisible(True)
        except Exception,e:
            self.lMensajes.append('Direccion Ip incorrecta')
            sys.stderr.write(str(e)+"\n")

    def btenviarfn(self):
        try:
            self.msg = str(self.tbMensaje.text())
            self.s.send(self.msg)
        except Exception,e:
            pass
            sys.stderr.write(str(e)+"\n")

    def modificar(self,text):
        self.lMensajes.append(text)

    @staticmethod
    def setTray(tra):
        global tray
        tray = tra
class recibido(threading.Thread):
    def __init__(self,socket,contenedor):
        threading.Thread.__init__(self)
        sys.stderr = file(os.path.join(os.path.dirname(__file__), 'log', 'recibido.log'),'a')
        self.soc = socket
        self.contenedor = contenedor

    def run(self):
        global tray
        while True:
            try:
                r = self.soc.recv( 128)
                a = r.decode('utf-8')
                self.contenedor.emit(QtCore.SIGNAL('sen'),str(a))
                tray.emit(QtCore.SIGNAL('emitir'),a)
            except Exception, e:
                sys.stderr.write(str(e)+"\n")
                pass



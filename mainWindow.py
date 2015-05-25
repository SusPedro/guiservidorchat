from PyQt4 import QtCore, QtGui, uic
import os,sys,threading ,socket,thread

form_class = uic.loadUiType(
    os.path.join(os.path.dirname(sys.argv[0]), 'ui', 'mainWindow.ui')
)[0]


class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        sys.stderr = file(os.path.join(os.path.dirname(sys.argv[0]), 'log', 'log.txt'), 'a')
        self.setupUi(self)
        """Conexiones"""
        self.btEnviar.clicked.connect(self.btenviarfn)
        QtCore.QObject.connect(self.lMensajes,
                               QtCore.SIGNAL('sen'),
                               self.modificar
                               )
        """"""
        """Conectar servidor"""
        self.s = socket.socket()
        try:
            self.lMensajes.append('conectando')
            self.s.connect(("192.168.1.36", 44000))
            self.lMensajes.append('conectado correctamente')
            self.r = recibido(self.s,self.lMensajes)
            self.r.setDaemon(True)
            self.r.start()
        except Exception,e:
            self.lMensajes.append('error conectando')
            sys.stderr.write(str(e))


    def keyPressEvent(self, event):
        key = event.key()
        """Key_return intro normal, key_enter intro numerico"""
        if key == QtCore.Qt.Key_Enter or key == QtCore.Qt.Key_Return:
            self.btEnviar.click()

    def closeEvent(self, evnt):
        self.s.close()
        pass
        sys.exit()

    def getUsuario(self):
        nusu = ['',False]
        while(nusu[1] == False):
            nusu = QtGui.QInputDialog.getText(self,
                                              "Nombre de usuario",
                                              "Nombre de usuario:",
                                              QtGui.QLineEdit.Normal
                                              )
            sys.stderr.write(str(nusu[1]))
        return nusu

    def btenviarfn(self):
        try:
            self.msg = str(self.tbMensaje.text())
            self.s.send(self.msg)
        except Exception,e:
            sys.stderr.write(str(e))

    def modificar(self,text):
        self.lMensajes.append(text)

class recibido(threading.Thread):
    def __init__(self,socket,contenedor):
        threading.Thread.__init__(self)
        self.soc = socket
        self.contenedor = contenedor

    def run(self):
        while True:
            try:
                r = self.soc.recv( 128)
                a = r.decode('utf-8')
                self.contenedor.emit(QtCore.SIGNAL('sen'),str(a))
            except Exception,e:
                sys.stderr.write(str(e))




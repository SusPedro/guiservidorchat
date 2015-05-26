from PyQt4 import QtCore, QtGui, uic
import os,sys,threading ,socket,thread

form_class = uic.loadUiType(
    os.path.join(os.path.dirname(sys.argv[0]), 'ui', 'mainWindow.ui')
)[0]


class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        sys.stderr = file(os.path.join(os.path.dirname(__file__), 'log', 'mainWindow.log'),'a')
        self.setupUi(self)
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
        while(nusu[1] == False or nusu[0] == ''):
            nusu = QtGui.QInputDialog.getText(self,
                                              "Nombre de usuario",
                                              "Nombre de usuario:",
                                              QtGui.QLineEdit.Normal
                                              )
        return nusu[0]

    def btconfn(self):
        """Conectar servidor"""
        self.s = socket.socket()
        try:
            self.lMensajes.append('conectando')
            self.s.connect(("10.215.5.208", 44000))
            self.lMensajes.append('conectado correctamente')
            self.r = recibido(self.s,self.lMensajes)
            self.r.setDaemon(True)
            self.r.start()
            self.name = self.getUsuario()
            self.s.send(str(self.name))
        except Exception,e:
            self.lMensajes.append('error conectando')
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

class recibido(threading.Thread):
    def __init__(self,socket,contenedor):
        threading.Thread.__init__(self)
        sys.stderr = file(os.path.join(os.path.dirname(__file__), 'log', 'recibido.log'),'a')
        self.soc = socket
        self.contenedor = contenedor

    def run(self):
        while True:
            try:
                r = self.soc.recv( 128)
                a = r.decode('utf-8')
                self.contenedor.emit(QtCore.SIGNAL('sen'),str(a))
            except Exception,e :
                sys.stderr.write(str(e)+"\n")
                pass



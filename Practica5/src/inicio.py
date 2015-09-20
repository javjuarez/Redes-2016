# -*- coding: utf-8 -*-

import xmlrpclib
import socket
import threading
import sys
import pyaudio
import wave

from chateo import Gui
from SimpleXMLRPCServer import SimpleXMLRPCServer
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Clase que muestra un listado con usuarios conectados en el chat
class lista(QWidget):
    def __init__(self, diccUsuarios, ipLocal, nombreUsuario):
        QWidget.__init__(self)

        self.setWindowTitle('Contactos conectados')

        self.ipLocal = ipLocal
        self.usuario = nombreUsuario
        self.contectados = diccUsuarios

        # No se muestra el usuario "anfitrión"
        if self.ipLocal in diccUsuarios.keys():
            del diccUsuarios[self.ipLocal]

        # Se muestra la lista de usuarios conectados en el servidor
        self.lista = QListWidget()
        for keys in self.contectados.keys():
            item = QListWidgetItem(keys + "-" + self.contectados[keys])
            self.lista.addItem(item)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.lista)

        self.botonMostrar = QPushButton("Conectar chat") # Cambiar a conectar
        vbox.addWidget(self.botonMostrar)

        self.botonActualiza = QPushButton("Actualizar lista")
        vbox.addWidget(self.botonActualiza)

        self.setLayout(vbox)

        self.botonMostrar.clicked.connect(self.conectaChat)
        self.botonActualiza.clicked.connect(self.actualiza)

    # Se selecciona un elemento del listado y realiza 
    # la conexión de chat con el usuario seleccionado
    def conectaChat(self):
        texto = str(self.lista.currentItem().text())
        listaUtil = texto.split("-")

        direccion = listaUtil[0]
        usuarioChatear = listaUtil[1]
        nombreUsuario = self.usuario
        par = EstablecerConexion(direccion)

        if len(direccion) > 0 and len(nombreUsuario) > 0 and par[0] :
            global chat
            global proxyListado
            proxyListado = par[1]
            chat = Gui(direccion, nombreUsuario)
            chat.show()
            # Muestra la ventana del chat en el otro usuario
            # proxyServ.senialVentana(direccion, nombreUsuario, usuarioChatear, self.ipLocal)
        else:
            print "No se puede iniciar el chat (direccion invalida o campos vacios)"

    # Actualiza la lista de usuarios, muestra si un usuario
    # se está conectado o no
    def actualiza(self):
        self.lista.clear()
        nuevoDic = proxyServ.getUsuarios()
        # No se muestra el usuario "anfitrión"
        if self.ipLocal in nuevoDic.keys():
            del nuevoDic[self.ipLocal]
        for keys in nuevoDic.keys():
            item = QListWidgetItem(keys + "-" + nuevoDic[keys])
            self.lista.addItem(item)

# Clase que muestra la interfaz de inicio
# Pide dirección ip del servidor de contactos, la propio y un nick name
class Conectar(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('Conectar direccion IP')
        self.ipServidor = QLineEdit()
        self.ipLocal = QLineEdit()
        self.nick = QLineEdit()
        self.btn_server = QPushButton("Corre servidor")
        self.btn_connect = QPushButton("Conectar")
        self.btn_disconnect = QPushButton("Desconectar")
        
        hIpServ = QHBoxLayout()
        hIpLocal = QHBoxLayout()
        hNick = QHBoxLayout()
        vbox = QVBoxLayout()
        
        hNick.addWidget(QLabel("Nick name:"))
        hNick.addWidget(self.nick)

        hIpLocal.addWidget(QLabel("Dir IP local"))
        hIpLocal.addWidget(self.ipLocal)

        hIpServ.addWidget(QLabel("Dir IP de servidor:"))
        hIpServ.addWidget(self.ipServidor)
        
        vbox.addLayout(hIpServ)
        vbox.addLayout(hIpLocal)
        vbox.addLayout(hNick)
        vbox.addWidget(self.btn_server)
        vbox.addWidget(self.btn_connect)
        vbox.addWidget(self.btn_disconnect)

        self.setGeometry(0,0,400,200)
        
        self.setLayout(vbox)
        
        self.btn_connect.clicked.connect(self.conectaServidorContactos)
        self.btn_server.clicked.connect(self.iniciaServidor)
        self.btn_disconnect.clicked.connect(self.desconectarServidor)

    # Desconecta al usuario del servidor de contactos y
    # cierra el programa
    def desconectarServidor(self):
        print proxyServ.getUsuarios()
        ip = str(self.ipLocal.text().toAscii())
        proxyServ.quitarUsuario(ip)
        # self.close()
        QCoreApplication.instance().quit()

    # Conecta al usuario con el servidor de contactos y
    # muestra la lista de usuarios conectados
    def conectaServidorContactos(self):
        direccion = str(self.ipServidor.text().toAscii())
        ipLocal = str(self.ipLocal.text().toAscii())
        nombreUsuario = str(self.nick.text().toAscii())

        par = EstablecerConexion(direccion)
        if len(direccion) > 0 and len(nombreUsuario) > 0 and par[0]:
            global listado
            global proxyServ
            proxyServ = par[1]
            proxyServ.agregaUsuario(ipLocal, nombreUsuario)
            dicc = proxyServ.getUsuarios()
            listado = lista(dicc, ipLocal, nombreUsuario)
            listado.show()
	
    # Inicia el servidor propio del usuario, esto con tal de
    # que se pueda comunicar con otros usuarios
    def iniciaServidor(self):
    	dirIp = "10.0.0.3"
        # dirIp = "localhost"
    	t = threading.Thread(target=correServidor, args=(dirIp,), name="servidor")
        t.setDaemon(True)
    	t.start()
    	# self.servidor = SimpleXMLRPCServer(("10.0.0.3", 8000)) # Bob
		# self.servidor = SimpleXMLRPCServer(("10.0.0.4", 8000)) # Alice

# Función de prueba
# Muestra el nombre host del usuario
def gethostname1():
	return socket.gethostname()

# Se muestra el mensaje enviado por otro usuario en
# la ventana del chat
def mensajeEnviado(mensaje, usuario):
	if chat.enviar:
		print "Mensaje enviado exitosamente"
		print usuario
		chat.recv.append(usuario + " ---> \n" + mensaje)

# Preparativos para la función de reproducir audio
CHUNK = 1024
FILE_NAME = "audioTemp.wav"

# Reproduce el audio enviado
def playAudio(audio):
    # print "Entrando en la reproducción del audio"
    with open(FILE_NAME, "wb") as handle:
        handle.write(audio.data)
    wf = wave.open(FILE_NAME, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()) ,
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
    chat.recv.append("* Fin del audio")
    stream.close()
    p.terminate()

# Muestra en el chat que se envió un archivo de audio
def audioEnviado(audio, usuario):
    if chat.audio:
        chat.recv.append("*" + usuario + " acaba de enviar un mensaje de audio *")
        playAudio(audio)

# Función que muestra una ventana de chat cuando otro usuario
# quiera hablar con nostros
def showVentana(dirIp, nombreUsuario, usuarioChatear):
    print nombreUsuario
    chatShow = Gui(dirIp, usuarioChatear)
    print chatShow
    chatShow.show()
    chatShow.recv.append(nombreUsuario + " ha iniciado un chat contigo")

# Corre el servidor propio del usuario, con tal de poder comunicarse
# con otro en el chat
def correServidor(ipLocal):    
    servidor = SimpleXMLRPCServer((ipLocal, 8000), allow_none=True)
    servidor.register_function(gethostname1, "gethostname1")
    servidor.register_function(mensajeEnviado, "mensajeEnviado")
    servidor.register_function(playAudio, "playAudio")
    servidor.register_function(audioEnviado, "audioEnviado")
    servidor.register_function(showVentana, "showVentana")
    try:
        print "Escuchado por el puerto 8000"
        print "Ctrl + C para salir"
        servidor.serve_forever()
    except KeyboardInterrupt:
        print "Saliendo"

# Abre un proxy con una dirección ip
def EstablecerConexion(ip):
	if(len(ip) > 0):
		# global proxy
		try:
			proxy = xmlrpclib.ServerProxy("http://" + ip + ":8000/")
		except IOError:
			print "La ip no es valida"
			return (False, None)
		return (True, proxy)
	else :
		return (False, None)

App = QApplication(sys.argv)
Con = Conectar()
Con.show()
App.exec_()

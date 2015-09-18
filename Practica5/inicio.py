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

# chat = ""

class lista(QWidget):
    def __init__(self, diccUsuarios, ipLocal, nombreUsuario):
        QWidget.__init__(self)

        self.ipLocal = ipLocal
        self.usuario = nombreUsuario
        self.contectados = diccUsuarios

        # No se muestra el usuario "anfitrión"
        if ipLocal in diccUsuarios.keys():
            del diccUsuarios[ipLocal]

        # Se muestra la lista de usuarios conectados en el servidor
        self.lista = QListWidget()
        for keys in self.contectados.keys():
            item = QListWidgetItem(keys + "-" + self.contectados[keys])
            self.lista.addItem(item)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.lista)

        self.botonMostrar = QPushButton("Mostrar y agregar")
        vbox.addWidget(self.botonMostrar)

        self.setLayout(vbox)

        self.botonMostrar.clicked.connect(self.mostrarListas)

    def mostrarListas(self):
        texto = str(self.lista.currentItem().text())
        listaUtil = texto.split("-")
        print listaUtil
        print listaUtil[0]
        print listaUtil[1]
        print "Actualizando elementos"
        self.lista.clear()
        nuevoDic = {"10.0.0.2":"javier", "10.0.0.5":"moni"}
        for keys in nuevoDic.keys():
            item = QListWidgetItem(keys + "-" + nuevoDic[keys])
            self.lista.addItem(item)

class Conectar(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('Conectar direccion IP')
        self.ipServidor = QLineEdit()
        self.ipLocal = QLineEdit()
        self.nick = QLineEdit()
        self.btn_server = QPushButton("Corre servidor")
        self.btn_connect = QPushButton("Conectar")
        
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

        self.setGeometry(0,0,400,200)
        
        self.setLayout(vbox)
        
        # self.btn_connect.clicked.connect(self.conectaProxy)
        self.btn_connect.clicked.connect(self.conectaServidorContactos)
        self.btn_server.clicked.connect(self.iniciaServidor)

    def conectaServidorContactos(self):
        direccion = str(self.ipServidor.text().toAscii())
        ipLocal = str(self.ipLocal.text().toAscii())
        nombreUsuario = str(self.nick.text().toAscii())
        if len(direccion) > 0 and len(nombreUsuario) > 0 and EstablecerConexion(direccion):
            global listado
            global proxy
            proxy.agregaUsuario(ipLocal, nombreUsuario)
            dicc = proxy.getUsuarios()
            listado = lista(dicc, ipLocal, nombreUsuario)
            listado.show()
            proxy.printUsuarios()
        
    # def conectaProxy(self):
    #     global hostProxy
    #     # chat = Gui()
    #     direccion = str(self.ip.text().toAscii())
    #     nombreUsuario = str(self.nick.text().toAscii())
    #     # proxy = xmlrpclib.ServerProxy("http://" + direccion + ":8000/")
    #     # hostProxy = str(proxy.gethostname1()) #Para obtener el nombre del equipo-servidor al que nos conectamos
    #     if len(direccion) > 0 and len(nombreUsuario) > 0 and EstablecerConexion(direccion) :
    #     	global chat
    #     	global proxy
    #     	chat = Gui(direccion, nombreUsuario)
    #     	chat.show()
    #     else:
    #     	print "No se puede iniciar el chat (direccion invalida o campos vacios)"
	
    def iniciaServidor(self):
    	dirIp = "10.0.0.3"
        # dirIp = "localhost"
    	t = threading.Thread(target=correServidor, args=(dirIp,), name="servidor")
        t.setDaemon(True)
    	t.start()
    	# self.servidor = SimpleXMLRPCServer(("10.0.0.3", 8000)) # Bob
    	# self.servidor.serve_forever
		# servidor = ServidorThread("10.0.0.4") # Alice

def gethostname1():
	return socket.gethostname()

def mensajeEnviado(mensaje, usuario):
	if chat.enviar:
		print "Mensaje enviado exitosamente"
		print usuario
		chat.recv.append(usuario + " ---> \n" + mensaje)

# Preparativos para la función de reproducir audio
CHUNK = 1024
FILE_NAME = "audioTemp.wav"
# CHANNELS = 1 
# RATE = 44100
# DELAY_SECONDS = 5 
# DELAY_SIZE = DELAY_SECONDS * RATE / (10 * CHUNK)
# FORMAT = pyaudio.paInt16

def playAudio(audio):
    # print "Entrando en la reproducción del audio"
    with open(FILE_NAME, "wb") as handle:
        handle.write(audio.data)
        # print "Abriendo archivo"
    wf = wave.open(FILE_NAME, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()) ,
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    # print data == ''
    while data != '':
        # print "Reproduciendo..."
        stream.write(data)
        data = wf.readframes(CHUNK)
    chat.recv.append("* Fin del audio")
    # stream.write(data)
    stream.close()
    p.terminate()

def audioEnviado(audio, usuario):
    if chat.audio:
        chat.recv.append("*" + usuario + " acaba de enviar un mensaje de audio *")
        # chat.recv.append("* Revisa en tu carpeta XOXO <3 *")
        playAudio(audio)
        # chat.recv.append("* Fin del audio")

def correServidor(ipLocal):    
    servidor = SimpleXMLRPCServer((ipLocal, 8000))
    servidor.register_function(gethostname1, "gethostname1")
    servidor.register_function(mensajeEnviado, "mensajeEnviado")
    servidor.register_function(playAudio, "playAudio")
    servidor.register_function(audioEnviado, "audioEnviado")
    try:
        print "Escuchado por el puerto 8000"
        print "Ctrl + C para salir"
        servidor.serve_forever()
    except KeyboardInterrupt:
        print "Saliendo"


def EstablecerConexion(ip):
	if(len(ip) > 0):
		global proxy
		try:
			proxy = xmlrpclib.ServerProxy("http://" + ip + ":8000/")
		except IOError:
			print "La ip no es valida"
			return False
		return True
	else :
		return False

App = QApplication(sys.argv)
# GUI = Gui("127.0.0.1", "Javier")
# GUI.show()
Con = Conectar()
Con.show()
App.exec_()

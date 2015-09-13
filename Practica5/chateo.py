# -*- coding: utf-8 -*-
# Comentario
import sys
import xmlrpclib
import socket
import threading

import pyaudio
import wave

from SimpleXMLRPCServer import SimpleXMLRPCServer
from PyQt4.QtCore import *
from PyQt4.QtGui import *


usuarioLocal = ""
proxy = ""
    
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

class Gui(QWidget):
    def __init__(self, ipProxy, usuarioL):
        QWidget.__init__(self)
        
        # self.proxy = xmlrpclib.ServerProxy("http://" + ipProxy + ":8000/")
        # print self.proxy


        global usuarioLocal 
        self.usuarioLocal = usuarioL

        if EstablecerConexion(ipProxy) != True:
            print "Conexión fallida"
            self.close()

        self.setWindowTitle('Chat')
        
        self.recv = QTextEdit()
        self.send = QLineEdit()
        self.btn_send = QPushButton("Enviar")
        self.btn_audio = QPushButton("Audio")
        self.btn_video = QPushButton("Video")
        
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        
        vbox.addWidget(self.recv)
        vbox.addLayout(hbox)
        vbox.addWidget(self.btn_audio)
        vbox.addWidget(self.btn_video)
        
        hbox.addWidget(self.send)
        hbox.addWidget(self.btn_send)
        
        self.setLayout(vbox)
 
        self.btn_send.clicked.connect(self.enviar)
        self.btn_audio.clicked.connect(self.audio)
        self.btn_video.clicked.connect(self.video)

        # print self.proxyChat

    def enviar(self):

        texto = str(self.send.text().toAscii())
        print proxy.gethostname1()
        # hostProxy = str(self.proxy.gethostname1()) #Para obtener el nombre del equipo-servidor al que nos conectamos
        # print hostProxy
        if texto != "":
            self.recv.append("Tu ---> \n" + texto)
            self.send.setText("")
            proxy.mensajeEnviado(texto, self.usuarioLocal)
            return True

    def audio(self):
        self.recv.append("* Grabando audio, tienes 3 segundos...")
        self.grabar();
        # proxy.audioEnviado(audio, self.usuarioLocal)
        return True

    def grabar(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 3 #Tiempo de grabación
        WAVE_OUTPUT_FILENAME = "output.wav"

        p = pyaudio.PyAudio()


        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        # print("* recording")
        # self.recv.append("* Grabando audio, tienes 3 segundos...")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        # print("* done recording")
        self.recv.append("* Fin de grabado")

        stream.stop_stream()
        stream.close()
        p.terminate()
        # return frames

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        with open(WAVE_OUTPUT_FILENAME, "rb") as handle:
            audio = xmlrpclib.Binary(handle.read())
        proxy.audioEnviado(audio, self.usuarioLocal)

    def video(self):
        pass

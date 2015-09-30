# -*- coding: utf-8 -*-

import sys
import xmlrpclib
import socket
import threading

import pyaudio
import wave

import cv2

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

# Clase que muestra la interfaz gráfica de un chat
class Gui(QWidget):
    def __init__(self, ipProxy, usuarioL):
        QWidget.__init__(self)

        global usuarioLocal 
        self.usuarioLocal = usuarioL

        if EstablecerConexion(ipProxy) != True:
            print "Conexión fallida"
            self.close()

        # Iniciamos la interfaz
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

        # Asignamos funciones a los botones
        self.btn_send.clicked.connect(self.enviar)
        self.btn_audio.clicked.connect(self.audio)
        self.btn_video.clicked.connect(self.video)

    # Función que muestra el mensaje en ambos lados del chat
    def enviar(self):

        texto = str(self.send.text().toAscii())
        print proxy.gethostname1()
        if texto != "":
            self.recv.append("Tu ---> \n" + texto)
            self.send.setText("")
            proxy.mensajeEnviado(texto, self.usuarioLocal)
            return True

    # Función que envia un audio grabado de un chat a otro
    def audio(self):
        self.recv.append("* Grabando audio, tienes 3 segundos...")
        self.grabar();
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

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        self.recv.append("* Fin de grabado")

        stream.stop_stream()
        stream.close()
        p.terminate()

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
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QMessageBox.warning(self, "Advertencia", "No se encuentra dispositivo:\nAsegurate de conectar una camara")
        else:
            pass

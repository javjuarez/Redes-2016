# -*- coding: utf-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCServer
from chateo import Gui
from socket import error as socket_error

import xmlrpclib
import threading

# usuariosConectados = {}

class Listener():
	def __init__(self):
		
		# Diccionario que guarda los usuarios conectados al servidor
		# Se guardarán de la forma direccionIp: nombreDeUsuario
		global usuariosConectados
		usuariosConectados = {}

	# Agrega un usuario al diccionario
	# Equivale a que un usuario se conecta al chat
	def agregaUsuario(self, dirIp, nombreUsuario):
		usuariosConectados[dirIp] = nombreUsuario
		self.servidorVivo(dirIp)
		return usuariosConectados

	# Quita un usuario al diccionario.
	# Equivale a que un usuario se desconecta del chat
	def quitarUsuario(self, dirIp):
		del usuariosConectados[dirIp]
		# print usuariosConectados
		return usuariosConectados

	# Obtiene el diccionario de usuarios
	# Esto para mostrar quienes están conectados
	def getUsuarios(self):
		return usuariosConectados

	# Imprime el diccionario en terminal
	def printUsuarios(self):
		print usuariosConectados

	# Función que manda una señal al un usuario cuando otro
	# se quiera conectar con él
	def senialVentana(self, dirIpRemota, nombreUsuario, usuarioChatear, dirIpLocal):
		proxy = xmlrpclib.ServerProxy("http://" + dirIpRemota + ":8000/")
		proxy.showVentana(dirIpLocal, nombreUsuario, usuarioChatear)

	# Función que permite saber si un servidor se encuentra conectado
	def servidorVivo(self, ip):
		proxy = xmlrpclib.ServerProxy("http://" + ip + ":8000/")
		# print usuariosConectados
		t = threading.Timer(5.0, self.servidorVivo, [ip])
		try:
			vivo = proxy.getConectado()
			if vivo:
				print "En línea"
			else:
				print "Muerto por variable"
		except socket_error:
			print "Muerto por exception"
			t.cancel()
			self.actualizaListas()
		t.daemon = True
		t.start()

	# Función que actualiza automáticamente la lista de 
	# contactos conectados
	def actualizaListas(self):
		for keys in usuariosConectados.keys():
			proxy = xmlrpclib.ServerProxy("http://" + keys + ":8000/")
			proxy.actualizaListaContactos()

# Servidor de contactos
servidor = SimpleXMLRPCServer(("10.0.0.7", 8000), allow_none=True)
print "Escuchando por el puerto 8000"
servidor.register_instance(Listener())
try:
	servidor.serve_forever()
except KeyboardInterrupt:
	print "Saliendo"
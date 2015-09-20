# -*- coding: utf-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCServer
from chateo import Gui

import xmlrpclib

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

# Servidor de contactos
servidor = SimpleXMLRPCServer(("10.0.0.7", 8000), allow_none=True)
print "Escuchando por el puerto 8000"
servidor.register_instance(Listener())
try:
	servidor.serve_forever()
except KeyboardInterrupt:
	print "Saliendo"
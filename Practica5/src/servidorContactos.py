# -*- coding: utf-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCServer
from chateo import Gui

import xmlrpclib

# Diccionario que guarda los usuarios conectados al servidor
# Se guardarán de la forma direccionIp: nombreDeUsuario
# usuariosConectados = {}

class Listener():
	def __init__(self):
		global usuariosConectados
		usuariosConectados = {}

	def agregaUsuario(self, dirIp, nombreUsuario):
		usuariosConectados[dirIp] = nombreUsuario
		return usuariosConectados

	def quitarUsuario(self, dirIp):
		del usuariosConectados[dirIp]
		# print usuariosConectados
		return usuariosConectados

	def getUsuarios(self):
		return usuariosConectados

	def printUsuarios(self):
		print usuariosConectados

	def senialVentana(self, dirIpRemota, nombreUsuario, usuarioChatear, dirIpLocal):
		# print dirIpRemota
		proxy = xmlrpclib.ServerProxy("http://" + dirIpRemota + ":8000/")
		# print proxy
		proxy.showVentana(dirIpLocal, nombreUsuario, usuarioChatear)

# Servidor de contactos
servidor = SimpleXMLRPCServer(("10.0.0.7", 8000), allow_none=True)
print "Escuchando por el puerto 8000"
# servidor.register_function(agregaUsuario, "agregaUsuario")
# servidor.register_function(quitarUsuario, "quitarUsuario")
# servidor.register_function(getUsuarios, "getUsuarios")
# servidor.register_function(printUsuarios, "printUsuarios")
servidor.register_instance(Listener())
try:
	servidor.serve_forever()
except KeyboardInterrupt:
	print "Saliendo"
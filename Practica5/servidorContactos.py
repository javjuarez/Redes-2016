# -*- coding: utf-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCServer

# Diccionario que guarda los usuarios conectados al servidor
# Se guardarán de la forma direccionIp: nombreDeUsuario
usuariosConectados = {}

def agregaUsuario(dirIp, nombreUsuario):
	usuariosConectados[dirIp] = nombreUsuario
	return usuariosConectados

def quitarUsuario(dirIp):
	del usuariosConectados[dirIp]
	# print usuariosConectados
	return usuariosConectados

def getUsuarios():
	return usuariosConectados

def printUsuarios():
	print usuariosConectados

# Servidor de contactos
servidor = SimpleXMLRPCServer(("10.0.0.7", 8000))
print "Escuchando por el puerto 8000"
servidor.register_function(agregaUsuario, "agregaUsuario")
servidor.register_function(quitarUsuario, "quitarUsuario")
servidor.register_function(getUsuarios, "getUsuarios")
servidor.register_function(printUsuarios, "printUsuarios")
try:
	servidor.serve_forever()
except KeyboardInterrupt:
	print "Saliendo"
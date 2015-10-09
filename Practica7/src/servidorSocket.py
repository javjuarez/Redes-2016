# -*- coding: utf-8 -*-

import socket
import pickle
import threading

# Servidor de contactos
class servidor(object):
	def __init__(self):
		
		self.usuariosConectados = [] # Guarda los usuarios conectados
		self.listaConexion = [] # Guarda los sockets que se conectan
		self.serv_ip = "10.0.0.7" # Ip del servidor de contactos
		self.serv_port = 8000
		self.buff_size = 1024
		self.escucha()

	# Define las acciones que va a hacer el servidor para funcionar
	def escucha(self):
		try:
			# Inicia el socket del servidor
			self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			# Evita que la dirección siga usándose después de cerrarse
			self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.socket_servidor.bind((self.serv_ip, self.serv_port))
			self.socket_servidor.listen(1)
			self.listaConexion.append((self.socket_servidor, self.serv_ip, "Servidor"))
			while True:
				# Entra un nuevo usuario
				for sck in self.listaConexion:
					if sck[0] == self.socket_servidor:
						conn, addr = self.socket_servidor.accept()
						
						data = pickle.loads(conn.recv(self.buff_size))
						tripleta = (conn, ) + data
						
						# Se guardan el socket y el usuario conectado en sus respectivas listas
						self.listaConexion.append(tripleta)
						if not data in self.usuariosConectados:
							self.usuariosConectados.append(data)
						lista_conectados = pickle.dumps(self.usuariosConectados)
						conn.send(lista_conectados)
						# Manda a todos los usuarios la lista actualizada de contactos
						self.enviaMensajes(conn, lista_conectados)
						print self.usuariosConectados
					# Aquí se cubre el caso en el que un usuario se desconecta, se actualiza la lista
					# else:
					# 	try:
					# 		# sck[0].send("Estas conectado?")
					# 		data = pickle.loads(sck[0].recv(self.buff_size))
					# 	except:
					# 		sck[0].close()
					# 		self.listaConexion.remove(sck)
					# 		for elem in self.usuariosConectados:
					# 			if sck[1] == elem[0]:
					# 				self.usuariosConectados.remove(elem)
					# 				break
					# 		lista_conectados = pickle.dumps(self.usuariosConectados)
					# 		self.enviaMensajes(sck[0], lista_conectados)
					# 		continue
		except KeyboardInterrupt:
			print "Saliendo"
			self.socket_servidor.close()
			return

	# Envía a todos los sockets, a excepción de sck_propio y el del servidor, un mensaje "global"
	def enviaMensajes(self, sck_propio, data):
		for socks in self.listaConexion:
			if socks[0] != self.socket_servidor and socks[0] != sck_propio:
				try:
					socks[0].send(data)
				except Exception, e:
					print "Desconectado"
					socks[0].close()
					self.listaConexion.remove(socks)

servidor()
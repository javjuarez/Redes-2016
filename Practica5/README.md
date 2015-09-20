Javier Juárez Carrillo				308335486
Francisco Javier González Huerta	308312221

La práctica comprende 3 archivos

	chateo.py
	inicio.py
	servidorContactos.py

El archivo servidorContactos.py se encarga de comunicar a los
usuarios que se quieran conectar con el chat, ésta tiene una 
dirección ip distinta a las que se usan para nuestros contactos. 
El archivo inicio.py se encarga de conectar al usuario con el 
servdor de contactos y correr el servidor del propio usuario para 
poder intercambiar mensajes con el otro usuario. El archivo chateo.
py contiene la interfaz del chat con el que nuestros usuarios se 
van a comunicar.

Forma de ejecutar archivos:

En una "máquina distinta" a la de los usuarios que van a chatear
se ejecuta el archivo servidorContactos.py, en el código se puede
observar que se corre con la dirección ip 10.0.0.7, en las máquinas
de los usuarios se corren los archivos inicio.py, se les pedirá
la dirección ip del servidor de contactos, la dirección propia y un
nick name con el que se verá para el otro usuario, dar click en los
botones "Corre servidor" y "Conectar" (no necesariamente en ese
orden), se mostrará un listado de usuarios conectados, seleccionar
con el que se va a comunicar y dar click en el botón "Conectar
chat"

Consideraciones:

Ambos usuarios deben dar click en "Conectar chat" ya que no pudimos
hacer que aparecieran ambos chats en las máquinas de los dos
usuarios
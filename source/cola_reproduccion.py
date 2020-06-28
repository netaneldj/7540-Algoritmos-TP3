import os
from cancion import Cancion
from clase_pila import Pila
from verificar_ruta import verificar_ruta

EXTENSIONES_ACEPTADAS = ("wav", "mp3", "flac", "ogg", "wma")

class ColaDeReproduccion:
	"""Clase que representa la cola de reproduccion del reproductor. Permite agregar y remover 
	canciones, ademas de poder hacer y deshacer estas acciones. Las canciones se guardan en la 
	cola como objetos de clase Cancion."""
	
	def __init__(self, lista_canciones = []):
		""" Recibe una lista de objetos de clase Cancion con las canciones que se quieren 
		reproducir."""
		self.cola_de_reproduccion=lista_canciones
		self.modificacion_cola=Pila()
		self.accion_deshecha=Pila()
		if not lista_canciones:
			self.primero=None
			self.ultimo=None
			self.pos_actual=None
		else:
			self.primero=cola_de_reproduccion[0]
			self.ultimo=cola_de_reproduccion[-1]
			self.pos_actual=0

	def cancion_actual(self):
		""" Devuelve un objeto de clase Cancion que corresponde a la cancion actual, o None si no 
		hay canciones cargadas en la cola."""
		if self.pos_actual is None:
			return None
		return self.cola_de_reproduccion[self.pos_actual]
		

	def cancion_siguiente(self):
		""" Devuelve un objeto de clase Cancion que corresponde a la cancion siguiente en la cola, 
		o None si no hay mas canciones."""
		if self.pos_actual is None:
			return None
		for posicion in range(len(self.cola_de_reproduccion)):
			if self.cola_de_reproduccion[posicion]==self.cola_de_reproduccion[self.pos_actual]:
				try:
					nueva_pos_actual=self.pos_actual+1
					cancion_siguiente=self.cola_de_reproduccion[nueva_pos_actual]
					self.pos_actual+=1
					return cancion_siguiente
				except IndexError:
					return None

	def cancion_anterior(self):
		""" Devuelve un objeto de clase Cancion que corresponde a la cancion anterior en la cola, 
		o None si no hay canciones en la misma o la actual es la primera de la cola."""
		if self.pos_actual is None:
			return None
		for indice in range(len(self.cola_de_reproduccion)):
			if self.cola_de_reproduccion[indice]==self.cola_de_reproduccion[self.pos_actual]:
				if indice==0:
					return None
				self.pos_actual-=1
				return self.cola_de_reproduccion[self.pos_actual]
					
	
	def agregar_cancion(self, ruta_cancion):
		""" Agrega una Cancion a la cola a partir de su ruta. Devuelve True si se agrego 
		correctamente, False en caso contrario. Esta accion puede deshacerse y rehacerse."""
		if not verificar_ruta(ruta_cancion):
			return False
		cancion=Cancion(ruta_cancion)
		if self.primero is None:
			self.cola_de_reproduccion.append(cancion)
			self.primero=self.cola_de_reproduccion[0]
			self.ultimo=self.cola_de_reproduccion[-1]
			self.pos_actual=0
			self.modificacion_cola.apilar(('add',ruta_cancion))
			return True
		self.cola_de_reproduccion.append(cancion)
		self.ultimo=self.cola_de_reproduccion[-1]
		self.modificacion_cola.apilar(('add',ruta_cancion))
		return True

	def remover_cancion(self, ruta_cancion):
		""" Remueve una Cancion de la cola a partir de su ruta. Devuelve True si se removio 
		correctamente, False en caso contrario. Esta accion puede deshacerse y rehacerse."""
		if not verificar_ruta(ruta_cancion):
			return False
		for indice in range(len(self.cola_de_reproduccion)):
			if self.cola_de_reproduccion[indice].obtener_ruta()==ruta_cancion:
				if indice==self.pos_actual:
					continue
				self.cola_de_reproduccion.pop(indice)
				self.primero=self.cola_de_reproduccion[0]
				self.ultimo=self.cola_de_reproduccion[-1]
				self.modificacion_cola.apilar(('del',ruta_cancion))
				if indice<self.pos_actual:
					self.pos_actual-=1
				return True
		return False
			
	def deshacer_modificacion(self):
		""" Deshace la ultima accion realizada. Devuelve True si pudo deshacerse, False en caso 
		contrario."""
		if len(self.cola_de_reproduccion)==1 or self.modificacion_cola.esta_vacia():
			return False
		if self.modificacion_cola.ver_tope()[0]=='add':
				self.cola_de_reproduccion.pop()
				self.ultimo=self.cola_de_reproduccion[-1]
				self.accion_deshecha.apilar(self.modificacion_cola.desapilar())
				return True
		for posicion in range(len(self.cola_de_reproduccion)):
			if self.cola_de_reproduccion[posicion].obtener_ruta()==self.modificacion_cola.ver_tope()[1]:
				self.cola_de_reproduccion.append(Cancion(self.modificacion_cola.ver_tope()[1]))
				self.ultimo=self.cola_de_reproduccion[-1]
				self.accion_deshecha.apilar(self.modificacion_cola.desapilar())
				return True
		

	def rehacer_modificacion(self):
		""" Rehace la ultima accion que se deshizo. Devuelve True si pudo rehacerse, False en caso 
		contrario."""
		if self.accion_deshecha.esta_vacia():
			return False
		if self.accion_deshecha.ver_tope()[0]=='add':
			self.cola_de_reproduccion.append(Cancion(self.accion_deshecha.ver_tope()[1]))
			self.ultimo=self.cola_de_reproduccion[-1]
			self.modificacion_cola.apilar(self.accion_deshecha.desapilar())
			return True
		self.cola_de_reproduccion.pop()
		self.ultimo=self.cola_de_reproduccion[-1]
		self.modificacion_cola.apilar(self.accion_deshecha.desapilar())
		return True
			
			

	def obtener_n_siguientes(self, n_canciones):
		""" Devuelve una lista con las siguientes n canciones. Si en la cola de reproduccion 
		quedan menos canciones que las pedidas, la lista contendra menos elementos que los 
		pedidos."""
		lista_canciones_siguientes=[]
		contador=0
		if self.pos_actual is None:
			return lista_canciones_siguientes	 
		for indice in range(self.pos_actual+1,len(self.cola_de_reproduccion)):
			lista_canciones_siguientes.append(self.cola_de_reproduccion[indice])
			contador+=1
			if contador==n_canciones:
				break
		return lista_canciones_siguientes
		

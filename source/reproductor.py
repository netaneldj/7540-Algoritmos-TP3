import pyglet.media as media
from cola_reproduccion import ColaDeReproduccion

class Reproductor(media.Player):
	""" Wrapper de pyglet.media.Player, adaptado para usar una ColaDeReproduccion en lugar de la 
	cola interna. """

	def __init__(self, cola_de_reproduccion):
		super().__init__()
		self.cola_de_reproduccion = cola_de_reproduccion
		self.cargar_cancion(self.cola_de_reproduccion.cancion_actual())

	def agregar_cancion(self, ruta_cancion):
		""" Agrega una cancion a la cola de reproduccion a partir de su ruta. Devuelve True si se 
		agrego correctamente, False en caso contrario."""
		return self.cola_de_reproduccion.agregar_cancion(ruta_cancion)

	def remover_cancion(self, ruta_cancion):
		""" Remueve una cancion a la cola de reproduccion a partir de su ruta. Devuelve True si se 
		agrego correctamente, False en caso contrario."""
		return self.cola_de_reproduccion.remover_cancion(ruta_cancion)

	def deshacer_modificacion(self):
		""" Deshace la ultima accion realizada sobre la cola de reproduccion."""
		return self.cola_de_reproduccion.deshacer_modificacion()

	def rehacer_modificacion(self):
		""" Rehace la ultima accion realizada sobre la cola de reproduccion."""
		return self.cola_de_reproduccion.rehacer_modificacion()

	def obtener_cancion_actual(self):
		""" Devuelve la Cancion que corresponde a la cancion actual en la cola de reproduccion."""
		return self.cola_de_reproduccion.cancion_actual()

	def reproducir(self):
		""" Empieza la reproduccion de las canciones. Si no hay una cancion cargada, intenta 
		cargar la cancion actual."""
		if not self.source:
			self.cargar_cancion(self.cola_de_reproduccion.cancion_actual())
		self.play()

	def pausar(self):
		""" Detiene la reproduccion."""
		self.pause()

	def avanzar(self):
		""" Avanza a la proxima cancion en la cola. Si se encuentra en la ultima cancion, no 
		avanza y detiene la reproduccion."""
		self.cargar_cancion(self.cola_de_reproduccion.cancion_siguiente())
		super().next_source()

	def retroceder(self):
		""" Retrocede a la cancion anterior de la cola. Si se encuentra en la primer cancion de 
		la cola, vuelve al principio de la misma."""
		self.cargar_cancion(self.cola_de_reproduccion.cancion_anterior())
		super().next_source()

	def cargar_cancion(self, cancion):
		""" Carga el archivo que corresponde al objeto Cancion pasado por parametro en la cola 
		interna del reproductor."""
		if cancion:
			self.queue(media.load(cancion.obtener_ruta()))
		
	def next_source(self):
		""" Metodo llamado automaticamente al finalizar una cancion. Avanza en la cola de 
		reproduccion, carga la cancion en la cola interna y dispara un evento on_eos.
		Si se llego al final de la cola y no hay mas canciones, detiene la reproduccion."""
		cancion = self.cola_de_reproduccion.cancion_siguiente()
		if not cancion:
			self.pausar()
		else:
			self.cargar_cancion(cancion)
			self.reproducir()
		self.dispatch_event("on_eos")

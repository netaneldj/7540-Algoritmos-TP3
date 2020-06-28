import pyglet
from cancion import Cancion
from cola_reproduccion import ColaDeReproduccion
from pyglet.window import key

class VentanaReproductor(pyglet.window.Window):
	""" Ventana del reproductor, que permite controlarlo, modificar la cola de reproduccion y 
	muestra la informacion de la cancion actual."""

	# Altura de los labels, util para calcular la posición de los mismos cuando hay varios juntos
	ALTURA_LABELS = 20
	
	MENSAJE_AGREGADA = "Cancion agregada a la cola de reproducción con exito"
	MENSAJE_REMOVIDA = "Cancion removida de la cola de reproducción con exito"
	MENSAJE_DESHECHO = "Se deshizo la modificación"
	MENSAJE_REHECHO = "Se rehizo la modificación"
	MENSAJE_FALLO_MODIFICACION = "No se pudo modificar la cola de reproducción"

	def __init__(self, reproductor):
		super().__init__(caption='Reproductor', height = self.ALTURA_LABELS * (9 + WidgetColaReproduccion.CANTIDAD_CANCIONES_MOSTRADAS), visible=True, resizable=False)
		self.reproductor = reproductor
		self.reproductor.on_eos = self.on_eos
		self.batch = pyglet.graphics.Batch()

		# Label que muestra el estado del reproductor (reproduciendo o detenido)
		self.label_estado = pyglet.text.Label("Estado", y = self.height, anchor_y = "top", height = self.ALTURA_LABELS, batch = self.batch)
		# Labels para mostrar la informacion de la cancion actual
		self.label_titulo = pyglet.text.Label("Titulo", y = self.label_estado.y - self.ALTURA_LABELS, anchor_y = "top", height = self.ALTURA_LABELS, batch = self.batch)
		self.label_autor = pyglet.text.Label("Artista", y = self.label_titulo.y - self.ALTURA_LABELS, anchor_y = "top", height = self.ALTURA_LABELS, batch = self.batch)

		# Seccion de agregar/remover cancion
		self.label_ruta = pyglet.text.Label("Ruta cancion:", y = self.label_autor.y - self.ALTURA_LABELS * 2, anchor_y='top', width = 120, batch=self.batch)
		self.texto_ruta = WidgetTexto(self.label_ruta.width, self.label_ruta.y - self.ALTURA_LABELS, self.width - self.label_ruta.width - 10, self.batch)
		self.label_modificado = pyglet.text.Label("", y = self.label_ruta.y - self.ALTURA_LABELS - WidgetTexto.PAD, anchor_y='top', width = self.width, multiline = True, batch=self.batch)
		self.focus = None

		# Seccion cola de reproduccion
		self.label_cola_reproduccion = pyglet.text.Label("Cola de reproducción:", y = self.label_modificado.y - self.ALTURA_LABELS * 2, anchor_y='top', batch=self.batch)
		self.lista_cola_reproduccion = WidgetColaReproduccion(self.reproductor.cola_de_reproduccion, 0, self.label_cola_reproduccion.y - self.ALTURA_LABELS * 2)

	def actualizar(self):
		""" Actualiza el estado de las labels de estado del reproductor, cancion actual y la 
		lista de la cola de reproduccion."""
		self.label_estado.text = self.obtener_estado_reproductor()
		self.label_titulo.text = self.obtener_titulo_cancion_actual()
		self.label_autor.text = self.obtener_artista_cancion_actual()
		self.lista_cola_reproduccion.actualizar()
		self.dibujar()

	def dibujar(self):
		""" Dibuja en la ventana los elementos de la misma."""
		self.clear()
		self.batch.draw()
		self.lista_cola_reproduccion.dibujar()

	def obtener_estado_reproductor(self):
		""" Devuelve una cadena con el estado del reproductor ("Reproduciendo" o "Detenido")."""
		return "Reproduciendo" if self.reproductor.playing else "Detenido"

	def obtener_titulo_cancion_actual(self):
		""" Devuelve una cadena con el titulo de la cancion actual, o "No hay canciones en la cola" 
		si la cola de reproduccion esta vacia."""
		cancion = self.reproductor.obtener_cancion_actual()
		return cancion.obtener_titulo() if cancion else "No hay canciones en la cola"

	def obtener_artista_cancion_actual(self):
		""" Devuelve una cadena con el artista de la cancion actual, o "No hay canciones en la cola" 
		si la cola de reproduccion esta vacia."""
		cancion = self.reproductor.obtener_cancion_actual()
		return cancion.obtener_artista() if cancion else "No hay canciones en la cola"		

	# Metodos de eventos de Pyglet
	def on_draw(self):
		self.dibujar()

	def on_eos(self):
		self.actualizar()

	def on_key_press(self, symbol, modifiers):
		self.label_modificado.text = ""
		if symbol == key.SPACE and self.focus != self.texto_ruta:
			self.reproductor.reproducir() if not self.reproductor.playing else self.reproductor.pausar()
		elif symbol == key.RIGHT and self.focus != self.texto_ruta:
			self.reproductor.avanzar()
		elif symbol == key.LEFT and self.focus != self.texto_ruta:
			self.reproductor.retroceder()
		elif symbol == key.A and modifiers & key.MOD_CTRL:
			agregada = self.reproductor.agregar_cancion(self.texto_ruta.obtener_texto())
			self.label_modificado.text = self.MENSAJE_AGREGADA if agregada else self.MENSAJE_FALLO_MODIFICACION
		elif symbol == key.R and modifiers & key.MOD_CTRL:
			removida = self.reproductor.remover_cancion(self.texto_ruta.obtener_texto())
			self.label_modificado.text = self.MENSAJE_REMOVIDA if removida else self.MENSAJE_FALLO_MODIFICACION
		elif symbol == key.Z and modifiers & key.MOD_CTRL:
			undo = self.reproductor.deshacer_modificacion()
			self.label_modificado.text = self.MENSAJE_DESHECHO if undo else self.MENSAJE_FALLO_MODIFICACION
		elif symbol == key.Y and modifiers & key.MOD_CTRL:
			redo = self.reproductor.rehacer_modificacion()
			self.label_modificado.text = self.MENSAJE_REHECHO if redo else self.MENSAJE_FALLO_MODIFICACION
		elif symbol == key.ESCAPE:
			self.dispatch_event("on_close")
		self.actualizar()

	def on_close(self):
		self.reproductor.pausar()
		self.close()

	def on_mouse_motion(self, x, y, dx, dy):
		if self.texto_ruta.chequear_superposicion(x, y):
			self.set_mouse_cursor(self.get_system_mouse_cursor('text'))
		else:
			self.set_mouse_cursor(None)

	def on_mouse_press(self, x, y, button, modifiers):
		if self.texto_ruta.chequear_superposicion(x, y):
			self.hacer_foco(self.texto_ruta)
		else:
			self.hacer_foco(None)

		if self.focus:
			self.focus.cursor.on_mouse_press(x, y, button, modifiers)

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if self.focus:
			self.focus.cursor.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

	def on_text(self, text):
		if self.focus:
			self.focus.cursor.on_text(text)

	def on_text_motion(self, motion):
		if self.focus:
			self.focus.cursor.on_text_motion(motion)
      
	def on_text_motion_select(self, motion):
		if self.focus:
			self.focus.cursor.on_text_motion_select(motion)
        
	def hacer_foco(self, focus):
		if self.focus:
			self.focus.cursor.visible = False
			self.focus.cursor.mark = self.focus.cursor.position = 0

		self.focus = focus
		if self.focus:
			self.focus.cursor.visible = True
			self.focus.cursor.mark = 0
			self.focus.cursor.position = len(self.focus.documento.text)

class WidgetTexto():
	""" Widget que permite usar un cuadro de texto, y obtener el contenido ingresado."""

	# Padding del cuadro de texto
	PAD = 5

	def __init__(self, x, y, ancho, batch):
		""" x e y indican la posicion del widget, ancho la cantidad de puntos de ancho que tendra, 
		y batch indica el pyglet.graphics.Batch al que pertenecera el widget."""
		self.documento = pyglet.text.document.UnformattedDocument("")
		self.documento.set_style(0, len(self.documento.text), dict(color=(0, 0, 0, 255)))
		fuente = self.documento.get_font()
		alto = fuente.ascent - fuente.descent

		self.layout = pyglet.text.layout.IncrementalTextLayout(self.documento, ancho, alto, multiline=False, batch=batch)
		self.cursor = pyglet.text.caret.Caret(self.layout)

		self.layout.x = x
		self.layout.y = y

		pad = self.PAD
		batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i', [x - pad, y - pad, x + ancho + pad, y - pad, x + ancho + pad, y + alto + pad, x - pad, y + alto + pad]), ('c4B', [200, 200, 220, 255] * 4))

	def obtener_texto(self):
		""" Devuelve el texto ingresado en el widget."""
		return self.documento.text

	def chequear_superposicion(self, x, y):
		""" Devuelve True si la posicion (x,y) dada se encuentra dentro del espacio del widget."""
		return (0 < x - self.layout.x < self.layout.width and 0 < y - self.layout.y < self.layout.height)

class WidgetColaReproduccion():
	""" Widget que lista las proximas canciones de la cola de reproduccion, mostrandolas como 
	"titulo - artista"."""

	# Numero de canciones a mostrar como maximo
	CANTIDAD_CANCIONES_MOSTRADAS = 10
	
	def __init__(self, cola_de_reproduccion, x, y):
		""" x e y indican la posicion del widget y cola_de_reproduccion una ColaDeReproduccion de 
		la que se quiere mostrar la informacion de las canciones."""
		self.x=x
		self.y=y
		self.cola_de_reproduccion=cola_de_reproduccion
		self.lista_mostrar=[]
		
	def actualizar(self):
		""" Actualiza la informacion de las canciones de la cola de reproduccion que se muestran en el widget."""
		self.lista_mostrar=self.cola_de_reproduccion.obtener_n_siguientes(self.CANTIDAD_CANCIONES_MOSTRADAS)
		

	def dibujar(self):
		""" Dibuja la lista de canciones de la cola de reproduccion en la pantalla."""
		contador=0
		for cancion in self.lista_mostrar:
			cancion_dibujar=pyglet.text.Label(cancion.obtener_titulo()+' - '+cancion.obtener_artista(),x=self.x, y=self.y-contador)
			contador+=20
			cancion_dibujar.draw()

import os
EXTENSIONES_ACEPTADAS = ("wav", "mp3", "flac", "ogg", "wma")

def verificar_ruta(ruta_cancion):
	"""Verifica que la ruta ingresada por parametro sea una ruta existente y de un archivo de 
	extension aceptada por el reproductor. Devuelve True si la ruta es correcta o False en caso contrario."""
	if not os.path.isfile(ruta_cancion):
		return False
	extension=ruta_cancion.split('.')
	return extension[-1] in EXTENSIONES_ACEPTADAS


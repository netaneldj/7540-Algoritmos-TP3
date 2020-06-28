class Pila:
	def __init__(self):
		self.elementos=[]
	def esta_vacia(self):
		return len(self.elementos)==0
	def apilar(self,valor):
		self.elementos.append(valor)
	def desapilar(self):
		if self.esta_vacia():
			raise IndexError('pila vacia')
		return self.elementos.pop()
	def ver_tope(self):
		if self.esta_vacia():
			return None
		return self.elementos[-1]
	def __str__(self):
		final=''
		for x in self.elementos:
			final+=str(x)+'-->'
		return final
		

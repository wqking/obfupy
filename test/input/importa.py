class ClassA :
	def __init__(self) -> None:
		self._prefix = "what"

	def makeMessage(self, tail) :
		return 'makeMessage: ' + self._prefix + ' ' + tail

	def sayHello(self) :
		print("Hello world, " + self.makeMessage('good'))

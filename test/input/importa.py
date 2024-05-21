class ClassA :
	def __init__(self) -> None:
		self._prefix = "what"

	def makeMessage(self, tail) :
		return 'makeMessage: ' + self._prefix + f' {tail}'

	def sayHello(self) :
		(abc) = ('good')
		print("Hello world, " + self.makeMessage('good'))

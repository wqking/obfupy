class ClassA :
	def __init__(self) -> None:
		self._prefix = "what"

	def makeMessage(self, tail) :
		x = 6
		x = x // 3
		return 'makeMessage: ' + self._prefix + str(x) + f' {tail}'

	def sayHello(self) :
		(abc) = ('good')
		print("Hello world, " + self.makeMessage(abc))

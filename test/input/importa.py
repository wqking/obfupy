import os.path
from argparse import ArgumentParser

class ClassA :
	# This is comment
	# another comment
	def __init__(self) -> None:
		'''This is docstring'''
		self._prefix = "what"

	@staticmethod
	def getOne() :
		return 1

	def makeMessage(self, tail) :
		x = 6
		x = x // 3
		return 'makeMessage: ' + self._prefix + str(x) + f' {tail}'

	def sayHello(self) :
		#importa = 5
		path = 6
		(abc) = ('good')
		print("Hello world, " + self.makeMessage(abc))
		anotherTest()

def anotherTest() :
	default = 5
	argumentParser = ArgumentParser()
	#argumentParser.add_argument('-a', '--action', dest = 'action', default = 'service', help = 'Execute the action')

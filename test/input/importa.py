import os.path
from argparse import ArgumentParser

from functools import wraps

def testInnerWraps(a) :
    @wraps(a)
    def b(*args, **kwargs):
        return a()
    return b

def test2(a, b) :
	return a + b

class ClassB :
	def __init__(self, value = 1) :
		self._value = value

	def getValue(self) :
		testInnerWraps(print)
		x = { "a": 1, "b": 2 }
		test2(**x)
		return self._value

class ClassA :
	# This is comment
	# another comment
	def __init__(self) -> None:
		'''This is a docstring'''
		self._prefix = "what"

	@staticmethod
	def getOne() :
		return 1
	
	def getTwo() :
		return 2

	def makeMessage(self, tail, x) :
		b = ClassB(value = 6)
		n = b.getValue()
		n = n // 3
		first = '''
			makeMessage :
		'''
		return 'makeMessage : ' + self._prefix + str(n) + f' {tail} ' + x

	def sayHello(self) :
		importa = 5
		path = 6
		(abc) = ('good')
		if path < 8 and abc is not None and (path == 6 or importa >= 0) or 6 or self.getTwo() :
			abc = "very"
		if abc is None :
			abc = ''
		elif path > 8 :
			abc = ''
		else :
			abc = "Very"
		print("Hello world, " + self.makeMessage(abc, x = "hi"))
		if True :
			anotherTest()

def anotherTest() :
	default = 5
	argumentParser = ArgumentParser()
	#argumentParser.add_argument('-a', '--action', dest = 'action', default = 'service', help = 'Execute the action')
	myMap = {
		'abc' : 2,
		'def' : 5,
	}

a = 0 or 10
assert a == 10

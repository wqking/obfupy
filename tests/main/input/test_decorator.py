def decoratorPrependAbc(func) :
	def wrapper(*args, **kwargs) :
		return "abc_" + str(func(*args, **kwargs))
	return wrapper

@decoratorPrependAbc
def funcA(n) :
	return n + 1

def funcB(a, n) :
	@a.wrapper
	def inner(b) :
		return b - 1
	return inner(n)

def test_funcA() :
	assert funcA(5) == "abc_6"

def test_inner() :
	test_inner.wrapper = decoratorPrependAbc
	assert funcB(test_inner, 8) == "abc_7"

@decoratorPrependAbc
def funcC(n) :
	decoratorPrependAbc = 2
	return n + decoratorPrependAbc

def test_funcC() :
	assert funcC(5) == "abc_7"

class DecoratorClass :
	def __init__(self, v = 0) :
		self._value = v

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, v):
		value = v
		self._value = value

def test_DecoratorClass() :
	obj = DecoratorClass(3)
	assert obj.value == 3
	obj.value = 5
	assert obj.value == 5
	assert obj._value == 5

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

def test_a() :
	assert funcA(5) == "abc_6"

def test_inner() :
	test_inner.wrapper = decoratorPrependAbc
	assert funcB(test_inner, 8) == "abc_7"

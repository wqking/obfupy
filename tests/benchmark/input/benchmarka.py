def benchmark_simpleForRange() :
	n = 0
	for i in range(10) :
		n += i

def benchmark_ifInsideForRange() :
	n = 0
	for i in range(10) :
		n += i
		if i > 0 :
			n += 1
		else :
			n += 2
	return n

def benchmark_concatString() :
	a = "abc"
	b = "bcd"
	c = 'cde'
	value = a + b + c
	assert value is not None

def nestedFunction(a) :
	def inner(b) :
		return a + b
	return inner(5)

def benchmark_nestedFunction() :
	assert nestedFunction(3) == 8
	assert nestedFunction(10) == 15

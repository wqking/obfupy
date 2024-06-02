def funcA(a, b, /, c, d, *, e, f, g, h) :
	assert a < b < c < d < e < f < g < h
	return a + b + c + d + e + f + g + h

#funcA = lambda a, b, /, c, d, *, e, f, g, h : a + b + c + d + e + f + g + h

def funcB(n) :
	n = n + 1
	return n

def funcVarArgsHelper(a, *b) :
	result = a
	previous = a
	for n in b :
		result += n
		assert n > previous
		previous = n
	return result

def funcVarArgs(a, *b) :
	return funcVarArgsHelper(a, *b)

def funcVarKeywordArgsHelper(a, **b) :
	result = str(a)
	for n in b :
		result += n + str(b[n])
	return result

def funcVarKeywordArgs(a, **b) :
	return funcVarKeywordArgsHelper(a, **b)

def funcWithDefaultArgs(a, b, c = 3, d = 4) :
	assert a <= b <= c <= d
	return a + b + c + d

def funcRecursive(a: int, b, depth) :
	if depth <= 0 :
		return a + b
	return funcRecursive(a + 1, b + 1, depth - 1)

def funcWithClassInside(a, b) :
	class X :
		def __init__(self) -> None:
			self._n = 3
		def add(self, a, b, c) :
			return a + b + c + self._n
	x = X()
	return x.add(a, b, 5)

def funcDefaultArgFromLocal() :
	a = 5
	b = 3
	def innerA(x, y = a + b) :
		assert innerA.z is None
		return x + y
	innerA.z = None
	return innerA(1)

def funcDefaultArgFromForLoop() :
	for i in range(5, 10) :
		def inner(x, *args, y = i, **kw) :
			return x + y
		return inner(3)

def test_a() :
	assert funcA(1, 2, 3, d = 4, e = 5, f = 6, g = 7, h = 8) == 36
	assert funcB(5) == 6
	assert funcVarArgs(1, 2, 3) == 6
	assert funcVarKeywordArgs(1, d = 2, e = 3) == "1d2e3"
	assert funcWithDefaultArgs(1, 2) == 10
	assert funcWithDefaultArgs(1, 2, 4) == 11
	assert funcWithDefaultArgs(1, 2, d = 5, c = 4) == 12
	assert funcRecursive(1, 2, 3) == 9
	assert funcWithClassInside(1, 2) == 11
	assert funcDefaultArgFromLocal() == 9
	assert funcDefaultArgFromForLoop() == 8

def funcNestedNested(f) :
	def inner() :
		nonlocal f
		if f is None :
			def f() :
				return 38
		return f
	return inner

def test_funcNestedNested() :
	assert funcNestedNested(None)()() == 38

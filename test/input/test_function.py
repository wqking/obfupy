def funcA(a, b, /, c, d, *, e, f, g, h) :
	assert a < b < c < d < e < f < g < h
	return a + b + c + d + e + f + g + h

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

def funcRecursive(a, b, depth) :
	if depth <= 0 :
		return a + b
	return funcRecursive(a + 1, b + 1, depth - 1)

def test_a() :
	assert funcA(1, 2, 3, d = 4, e = 5, f = 6, g = 7, h = 8) == 36
	assert funcB(5) == 6
	assert funcVarArgs(1, 2, 3) == 6
	assert funcVarKeywordArgs(1, d = 2, e = 3) == "1d2e3"
	assert funcWithDefaultArgs(1, 2) == 10
	assert funcWithDefaultArgs(1, 2, 4) == 11
	assert funcWithDefaultArgs(1, 2, d = 5, c = 4) == 12
	assert funcRecursive(1, 2, 3) == 9

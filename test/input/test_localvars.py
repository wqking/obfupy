

def test_localVariable() :
	a = 1
	assert a == 1
	(a, b) = (2, 3)
	c = a + b
	b = 5
	c += b
	assert c == 10

def test_variableInNestedFunction() :
	a = 5
	def nested(b) :
		nonlocal a
		assert a == b
		a = a + 1
		assert a == b + 1
	nested(5)
	assert a == 6
	a = a + 1
	a += 2
	assert a == 9

globalA = 38
def test_globalVariable() :
	def nested() :
		global globalA
		globalA = 10
	global globalA
	globalA = 0
	nested()
	assert globalA == 10

def test_walrus() :
	a = 1
	b = (a := 2) > 1
	assert b
	assert a == 2
	b = (c := 3) < 0
	assert not b
	assert c == 3
	c = 5
	assert c == 5

def test_fString() :
	a = 1
	s = f"is_{a}"
	assert s == "is_1"
	a += 5
	s = f"is_{a}"
	assert s == "is_6"

def test_useBeforeAssign() :
	n = 0
	for _ in range(2) :
		try :
			n = a
		except :
			pass
		a = 1
	assert n == 1

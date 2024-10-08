def doTestFor() :
	total = 0
	for i in range(5) :
		total += i
	assert total == 10
	assert i == 4
	
	total = 0
	i = 8
	for i in range(6) :
		total += i
	assert total == 15
	assert i == 5
	
	total = 0
	for i, k in [ (1, 2), (3, 4) ] :
		total += i + k
	assert total == 10
	assert i == 3
	assert k == 4

	total = 0
	m = { 'n' : 5 }
	for ttt in range((lambda ttt : ttt['n'])(m)) :
		total += ttt
	assert total == 10

def test_for() :
	doTestFor()

def doTestIf() :
	a = 1
	b = 0
	if a > 0 :
		b = 5
		assert True
	else :
		assert False
	if b == 5 :
		assert True
	else :
		assert False
	if a == 1 and b == 5 :
		assert True
	else :
		assert False

def test_if() :
	doTestIf()

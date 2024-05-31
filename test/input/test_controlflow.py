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

def test_for() :
	doTestFor()

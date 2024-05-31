class ClassA :
	staticA = 5

	def __init__(self) :
		pass

	def computeA(self, n) :
		return n + ClassA.staticA
	
def test_a() :
	a = ClassA()
	assert a.computeA(3) == 8

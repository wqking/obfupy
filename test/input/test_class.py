def duplicatedFunc() :
	return 3

class ClassA :
	staticA = 5

	def __init__(self) :
		self.__mangledA = 1
		self.__mangledB_ = 2
		self._value = 1

	def computeA(self, n) :
		return n + ClassA.staticA + self._value
	
	def getMangled(self) :
		return self.__mangledA + self.__mangledB_
	
	def duplicatedFunc(self) :
		return duplicatedFunc()
	
	def recursive(self, n) :
		if n <= 0 :
			return 0
		return n + self.recursive(n - 1)
	
def test_a() :
	a = ClassA()
	assert a.computeA(3) == 9
	assert a.getMangled() == 3
	assert a.duplicatedFunc() == 3
	assert a.recursive(3) == 6

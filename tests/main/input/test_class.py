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
	
	class X :
		pass
	def getValue(self, unused : X = None, *args, unused2 = staticA) -> X :
		return self._value
	
def test_a() :
	a = ClassA()
	assert a.computeA(3) == 9
	assert a.getMangled() == 3
	assert a.duplicatedFunc() == 3
	assert a.recursive(3) == 6

def funcLocalClassDeriveFromLocalVar(n) :
	cls = ClassA
	class LocalB(cls) :
		def add(self, n) :
			return self.getValue() + n
	b = LocalB()
	return b.add(n)

def test_funcLocalClassDeriveFromLocalVar() :
	assert funcLocalClassDeriveFromLocalVar(5) == 6

def fundLocalClassWithClassAttribute() :
	abc = 5
	class LocalClass :
		xyz = abc
	# This xyz = 10 is here to test the xyz in LocalClass is not renamed
	xyz = 10
	assert 5 == LocalClass.xyz
	LocalClass.xyz = 6
	return LocalClass.xyz

def test_fundLocalClassWithClassAttribute() :
	assert fundLocalClassWithClassAttribute() == 6

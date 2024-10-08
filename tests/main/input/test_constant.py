"""
Module docstring
"""

"""
Second orphan string
"""

def test_int() :
	# Use string to avoid the int being obfuscated
	assert str(19) == '19'

def test_intAndFloat() :
	# 1.0 and 1 should not be replaced as same constant variable,
	a = 1.0
	b = 3
	b = b + 1
	assert isinstance(b, int)

def test_builtinFunction() :
	a = "abc"
	assert isinstance(a, str)

def test_builtinFunctionAsVariable() :
	str = "abc"
	assert str == "abc"
	assert len(str) == 3

def funcBuiltinFunctionAsArgument(str) :
    return len(str)

def test_funcBuiltinFunctionAsArgument() :
	str = "def"
	assert funcBuiltinFunctionAsArgument(str) == 3

def test_unicodeString() :
	a = "\u2028"
	assert len(a) == 1
	assert a == "\u2028"

def test_builtinFunctionAsNestedFunc() :
	def open() :
		return open.value
	open.value = 5
	assert open.value == 5
	assert open() == 5


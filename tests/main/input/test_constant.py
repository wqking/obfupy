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

def test_foldConstantExpression() :
	if 1 and 2 :
		assert True
	if 1 or 2 :
		assert True
	
	a = ~5
	assert a == -6
	a = not True
	assert not a
	a = +5
	assert a == 5
	a = -5
	assert a == -5

	a = 5 + 3
	assert a == 8
	a = 5 - 3
	assert a == 2
	a = 5 * 3
	assert a == 15
	a = 6 / 3
	assert a == 2
	a = 5 % 3
	assert a == 2
	a = 5 ** 3
	assert a == 125
	a = 5 << 3
	assert a == 40
	a = 15 >> 1
	assert a == 7
	a = 1 | 2
	assert a == 3
	a = 3 ^ 1
	assert a == 2
	a = 3 & 1
	assert a == 1
	a = 5 // 3
	assert a == 1

	a = (3 == (1 + 2))
	assert a is True
	a = (3 != (1 + 2))
	assert a is False
	a = (3 < 5)
	assert a is True
	a = (3 <= 5)
	assert a is True
	a = (3 <= 3)
	assert a is True
	a = (3 > 5)
	assert a is not True
	a = (3 >= 5)
	assert a is not True
	a = (3 >= 3)
	assert a is True
	a = 'a' in 'abc'
	assert a is True
	a = 'd' not in 'abc'
	assert a is True
	a = True is True
	assert a is True
	a = True is not True
	assert a is not True

	a = (((5 + 3 - 2) * 3 // 2) << 2) >> 1
	assert a == 18
	a = "abc" + "def"
	assert a == "abcdef"

	a = str()
	assert a == ''
	a = str(3)
	assert a == '3'
	a = str((((5 + 3 - 2) * 3 // 2) << 2) >> 1)
	assert a == '18'

def test_int() :
	# Use string to avoid the int being obfuscated
	assert str(19) == '19'

def test_intAndFloat() :
	# 1.0 and 1 should not be replaced as same constant variable,
	a = 1.0
	b = 3
	b = b + 1
	assert isinstance(b, int)

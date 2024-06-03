def funcException1() :
	e = None
	try :
		1 / 0
	except Exception as e :
		return e
	return None

def test_funcException1() :
	assert funcException1() is not None


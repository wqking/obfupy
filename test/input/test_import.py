def funcLocalImport(n = None) :
	if n is None :
		from os import chdir as n
	return n

def test_import() :
	assert funcLocalImport() is not None

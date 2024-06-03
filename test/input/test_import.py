from __future__ import annotations # This is to test SyntaxError: from __future__ imports must occur at the beginning of the file

def funcLocalImport(n = None) :
	if n is None :
		from os import chdir as n
	return n

def funcLocalImport2() :
	n = None
	if n is None :
		from os import chdir as n
	return n

def funcLocalImport3() :
	chdir = None
	if chdir is None :
		from os import chdir
	return chdir

def test_import() :
	assert funcLocalImport() is not None
	assert funcLocalImport2() is not None
	assert funcLocalImport3() is not None

import ast
import codecs

from ..internal import astutil

def reverse(string) :
	return ast.Subscript(
		value = astutil.makeConstant(string[::-1]),
		slice = ast.Slice(step = astutil.makeConstant(-1)),
		ctx = ast.Load()
	)

def rot13(string) :
	string = codecs.encode(string, 'rot13')
	return ast.Call(
		func = ast.Attribute(
			value = ast.Name(id = 'codecs', ctx = ast.Load()),
			attr = 'decode',
			ctx = ast.Load()
		),
		args = [
			astutil.makeConstant(string),
			astutil.makeConstant('rot13')
		],
		keywords = []
	)
rot13.extraNode = ast.Import(
	names = [ ast.alias(name = 'codecs') ]
)

def hex(string) :
	string = codecs.encode(string.encode('utf-8'), "hex")
	return ast.Call(
		func = ast.Attribute(
			value = ast.Call(
				func = ast.Attribute(
					value = ast.Name(id = 'codecs', ctx = ast.Load()),
					attr = 'decode',
					ctx = ast.Load()
				),
				args = [
					astutil.makeConstant(string),
					astutil.makeConstant('hex')
				],
				keywords = []
			),
			attr = 'decode',
			ctx = ast.Load()
		),
		args = [
			astutil.makeConstant('utf-8')
		],
		keywords = []
	)
hex.extraNode = ast.Import(
	names = [ ast.alias(name = 'codecs') ]
)

defaultEncoders = [
	reverse,
	rot13,
	hex
]

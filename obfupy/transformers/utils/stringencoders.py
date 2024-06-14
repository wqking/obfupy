import ast
import codecs
import random

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

def xor(string) :
	data = bytearray(string.encode('utf-8'))
	value = random.randint(1, 255)
	for i in range(len(data)) :
		data[i] = data[i] ^ value
	data = bytes(data)
	return ast.Call(
		func = ast.Attribute(
			value = ast.Call(
				func = ast.Attribute(
					value = ast.Constant(value = b''),
					attr = 'join',
					ctx = ast.Load()),
				args = [
					ast.ListComp(
						elt = ast.Call(
							func = ast.Attribute(
								value = ast.Call(
									func = ast.Name(id='chr', ctx = ast.Load()),
									args = [
										ast.BinOp(
											left = ast.Name(id = 'i', ctx = ast.Load()),
											op = ast.BitXor(),
											right = ast.Constant(value = value)
										)
									],
									keywords = []
								),
								attr = 'encode',
								ctx = ast.Load()
							),
							args = [
								ast.Constant(value = 'utf-8')],
							keywords = []
						),
						generators = [
							ast.comprehension(
								target = ast.Name(id='i', ctx = ast.Store()),
								iter = ast.Constant(value = data),
								ifs = [],
								is_async = 0
							)
						]
					)
				],
				keywords = []),
			attr = 'decode',
			ctx = ast.Load()
		),
		args = [
			ast.Constant(value = 'utf-8')
		],
		keywords = []
	)

defaultEncoders = [
	reverse,
	rot13,
	hex,
	xor
]

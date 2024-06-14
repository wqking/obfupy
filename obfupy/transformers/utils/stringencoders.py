import ast
import codecs
import random

from ..internal import astutil
from ..internal import util

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
	value = random.randint(1, 0xffff)
	data = [ ord(i) ^ value for i in string ]
	indexName = util.getUnusedRandomSymbol()
	return ast.Call(
		func = ast.Attribute(
			value = ast.Constant(value=''),
			attr = 'join',
			ctx = ast.Load()
		),
		args = [
			ast.ListComp(
				elt = ast.Call(
					func = ast.Name(id='chr', ctx = ast.Load()),
					args = [
						ast.BinOp(
							left = ast.Name(id = indexName, ctx = ast.Load()),
							op = ast.BitXor(),
							right = ast.Constant(value = value)
						)
					],
					keywords = []
				),
				generators = [
					ast.comprehension(
						target = ast.Name(id = indexName, ctx = ast.Store()),
						iter = ast.Constant(data),
						ifs = [],
						is_async = 0
					)
				]
			)
		],
		keywords = []
	)

defaultEncoders = [
	reverse,
	rot13,
	hex,
	xor
]

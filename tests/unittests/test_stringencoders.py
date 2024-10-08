import testutil
import obfupy.transformers.utils.stringencoders as stringencoders
import obfupy.transformers.internal.astutil as astutil

import codecs # used by string encoders

def evalNode(node) :
	return eval(astutil.astToSource(node))

stringList = [
	"",
	"abc", "This is a sentence.",
	"这是中文字符串", "これは日本語の文章です"
]

def test_stringEncoders() :
	for s in stringList :
		assert evalNode(stringencoders.reverse(s)) == s
		assert evalNode(stringencoders.rot13(s)) == s
		assert evalNode(stringencoders.hex(s)) == s
		assert evalNode(stringencoders.xor(s)) == s

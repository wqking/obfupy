import random
import base64

from . import util as util

class _IOperator :
	def __init__(self) :
		pass

	def transform(self, documentManager) :
		for document in documentManager.getDocumentList() :
			self.doTransformDocument(document)

	def doTransformDocument(self, document) :
		operator = random.choice(operatorList)
		content = document.getContent()
		key = random.randint(1, 255)
		encoded = base64.b64encode(operator['encode'](key, bytearray(content, 'utf-8'))).decode('utf-8')
		decoderName = util.getRandomSymbol()
		newContent = template.format(
			name = util.getRandomSymbol(),
			decoderName = decoderName,
			code = encoded,
			decoder = operator['decode'].format(
				decoderName = decoderName,
				dataName = util.getRandomSymbol(),
				key = key
			)
		)
		document.setContent(newContent)

template = '''
import base64
{name} = """{code}"""
{decoder}
eval(compile({decoderName}(bytearray(base64.b64decode({name}))),'<string>','exec'))
'''

def _encodeXor(key, data) :
	for i in range(len(data)) :
		data[i] ^= key
	return data

_decodeXor = '''
def {decoderName}({dataName}) :
	for i in range(len({dataName})) : {dataName}[i] ^= {key}
	return {dataName}
'''

operatorList = [
	{
		'encode' : _encodeXor,
		'decode' : _decodeXor,
	}
]

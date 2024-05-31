import random
import base64

from .internal import util as util

class CodecProvider :
	def __init__(
			self,
			encoder = lambda x : x,
			decoder = '%s',
			extraCode = None
		) :
		self._encoder = encoder
		self._decoder = decoder
		self._extraCode = extraCode

	def reset(self) :
		pass

	def encode(self, data) :
		return self._encoder(data)

	def getDecoder(self, variableName) :
		if callable(self._decoder) :
			return self._decoder(variableName)
		return self._decoder % (variableName)

	def getExtraCode(self, indent) :
		return self._extraCode

class Codec :
	def __init__(self, provider) :
		self._provider = provider

	def transform(self, documentManager) :
		for document in documentManager.getDocumentList() :
			self._doTransformDocument(document)

	def _doTransformDocument(self, document) :
		if hasattr(self._provider, 'reset') :
			self._provider.reset()
		content = document.getContent()
		data = bytearray(content, 'utf-8')
		data = self._provider.encode(data)
		
		encoded = base64.b64encode(data).decode('utf-8')

		indent = '\t' * random.randint(1, 10)
		variableName = util.getRandomSymbol()
		code = ''
		code += "import base64\n"
		extraCode = None
		if hasattr(self._provider, 'getExtraCode') :
			extraCode = self._provider.getExtraCode(indent)
		if extraCode is not None :
			code += f"{extraCode}\n"
		code += f"{variableName} = '{encoded}'\n"
		tempVariableName = util.getRandomSymbol()
		decoder = self._provider.getDecoder(tempVariableName)
		code += f"{tempVariableName} = bytearray(base64.b64decode({variableName}))\n"
		code += f"eval(compile({decoder},'<string>','exec'))\n"
		document.setContent(code)


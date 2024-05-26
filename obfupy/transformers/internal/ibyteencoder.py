import random
import base64

from . import util as util

class _IByteEncoder :
	def __init__(self) :
		pass

	def transform(self, documentManager) :
		for document in documentManager.getDocumentList() :
			self.doTransformDocument(document)

	def doTransformDocument(self, document) :
		operatorCount = len(operatorConfigList)
		operatorList = [] + operatorConfigList
		while len(operatorList) > operatorCount :
			operatorList.pop()
		while len(operatorList) < operatorCount :
			operatorList.append(random.choice(operatorConfigList))
		random.shuffle(operatorList)

		keyList = []
		while len(keyList) < operatorCount :
			keyRange = (1, 255)
			k = len(keyList)
			if 'keyRange' in operatorList[k] :
				keyRange = operatorList[k]['keyRange']
			keyList.append(random.randint(keyRange[0], keyRange[1]))

		content = document.getContent()
		data = bytearray(content, 'utf-8')
		for i in range(len(data)) :
			for k in range(operatorCount - 1, -1, -1) :
				data[i] = operatorList[k]['encode'](data[i], keyList[k])
		encoded = base64.b64encode(data).decode('utf-8')
		decoderName = util.getRandomSymbol()
		dataName = util.getRandomSymbol()
		decoderCode = ''
		indent = '    '
		decoderCode += f"def {decoderName}({dataName}) :\n"
		decoderCode += f"{indent}for i in range(len({dataName})) :\n"
		for k in range(operatorCount) :
			decoderCode += f"{indent}{indent}{dataName}[i] = " + operatorList[k]['decode'].format(
				data = f"{dataName}[i]",
				key = keyList[k],
				keyMinus8 = 8 - keyList[k],
			) + "\n"
		decoderCode += f"{indent}return {dataName}\n"
		newContent = template.format(
			name = util.getRandomSymbol(),
			decoderName = decoderName,
			code = encoded,
			decoder = decoderCode
		)
		document.setContent(newContent)

template = '''
import base64
{name} = """{code}"""
{decoder}
eval(compile({decoderName}(bytearray(base64.b64decode({name}))),'<string>','exec'))
'''

def xor(data, key) :
	return data ^ key

def add(data, key) :
	return (data + key) % 256

def sub(data, key) :
	return (data - key) % 256

def ror(data, key) :
	return ((data >> key) | (data << (8 - key))) & 0xff

def rol(data, key) :
	return ((data << key) | (data >> (8 - key))) & 0xff

def bitNot(data, key) :
	return (~data) & 0xff

operatorConfigList = [
	{
		'encode' : xor,
		'decode' : '{data} ^ {key}',
	},

	{
		'encode' : add,
		'decode' : '({data} - {key}) % 256',
	},

	{
		'encode' : sub,
		'decode' : '({data} + {key}) % 256',
	},

	{
		'encode' : ror,
		'decode' : '(({data} << {key}) | ({data} >> {keyMinus8})) & 0xff',
		'keyRange' : (1, 7)
	},

	{
		'encode' : rol,
		'decode' : '(({data} >> {key}) | ({data} << {keyMinus8})) & 0xff',
		'keyRange' : (1, 7)
	},

	{
		'encode' : bitNot,
		'decode' : '(~{data}) & 0xff',
	},
]

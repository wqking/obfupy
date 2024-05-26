import string
import random

_randomSymbolLeadLetters = 'Il'
_randomSymbolAllLetters = _randomSymbolLeadLetters + '1'
_uniqueSymbolMap = {}

def getRandomSymbol(length = None) :
	if length is None :
		length = random.randint(6, 20)
	result = random.choice(_randomSymbolLeadLetters)
	while len(result) < length :
		result += random.choice(_randomSymbolAllLetters)
	return result

def getUnusedRandomSymbol(usedMap = None) :
	if usedMap is None :
		usedMap = _uniqueSymbolMap
	length = 12
	while True :
		newName = getRandomSymbol(length)
		if newName not in usedMap :
			usedMap[newName] = True
			_uniqueSymbolMap[newName] = True
			return newName
		length = None

class Result :
	def __init__(self, value = None, success = True) :
		self._value = value
		self._success = success

	def getValue(self) :
		return self._value
	
	def isSuccess(self) :
		return self._success

failedResult = Result(success = False)

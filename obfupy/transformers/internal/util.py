import string
import random

class Result :
	def __init__(self, value = None, success = True) :
		self._value = value
		self._success = success

	def getValue(self) :
		return self._value
	
	def isSuccess(self) :
		return self._success

failedResult = Result(success = False)
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

def isUsedRandomSymbol(symbol) :
	return symbol in _uniqueSymbolMap

def hasChance(total, chance = 1) :
	return random.randint(1, total) <= chance

def makeShuffledIndexList(len) :
	result = [ i for i in range(len) ]
	random.shuffle(result)
	return result

def makeListByIndexList(itemList, indexList) :
	return [ itemList[index] for index in indexList ]

def isSpecialFunctionName(name) :
	return (
		len(name) > 4
		and name[0] == '_' and name[1] == '_'
		and name[-1] == '_' and name[-2] == '_'
	)

def isNameMangling(name) :
	if not (len(name) > 2 and name[0] == '_' and name[1] == '_') :
		return False
	if len(name) > 3 and name[-1] == '_' :
		return name[-2] != '_'
	return True

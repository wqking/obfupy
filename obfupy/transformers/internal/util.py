import string
import random
import copy

class ExitGuard :
	def __init__(self, callback) :
		self._callback = callback

	def __enter__(self) :
		pass

	def __exit__(self, type, value, traceBack) :
		self._callback()

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

def getUnusedRandomSymbol(usedMap = None, originalName = None) :
	if usedMap is None :
		usedMap = _uniqueSymbolMap
	length = 12
	while True :
		newName = getRandomSymbol(length)
		if originalName is not None :
			newName = newName + '_' + originalName + '_' + str(random.randint(1, 100000))
		if newName not in usedMap :
			usedMap[newName] = True
			_uniqueSymbolMap[newName] = True
			return newName
		length = None

def isUsedRandomSymbol(symbol) :
	return symbol in _uniqueSymbolMap

def hasChance(total, chance = 1) :
	if total < 1 :
		return False
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

# list.index may raise exception, this function won't
def findItemIndexInList(itemList, item) :
	for i in range(len(itemList)) :
		if itemList[i] == item :
			return i
	return -1

def ensureList(a) :
	if isinstance(a, list) :
		return a
	return [ a ]

def joinList(a, b) :
	return ensureList(a) + ensureList(b)

def makeOptions(options, defaultOptions) :
	result = copy.deepcopy(defaultOptions)
	if options is not None :
		for name in options :
			assert name in defaultOptions
			result[name] = options[name]
	return result


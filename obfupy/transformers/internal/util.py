import string
import random

_randomSymbolLeadLetters = 'Il'
_randomSymbolAllLetters = _randomSymbolLeadLetters + '1'

def getRandomSymbol(length = None) :
	if length is None :
		length = random.randint(6, 20)
	result = random.choice(_randomSymbolLeadLetters)
	while len(result) < length :
		result += random.choice(_randomSymbolAllLetters)
	return result

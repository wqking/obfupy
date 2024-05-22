import string
import random

def getRandomSymbol(length = None) :
	if length is None :
		length = random.randint(8, 32)
	result = ''
	while len(result) < length :
		result += random.choice(string.ascii_letters)
	return result

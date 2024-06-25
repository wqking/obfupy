# obfupy library
#
# Copyright (C) 2024 Wang Qi (wqking)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

_uniqueSymbolMap = {}

def randomSymbolGenerator111(length) :
	result = random.choice(randomSymbolGenerator111._leadLetters)
	while len(result) < length :
		result += random.choice(randomSymbolGenerator111._allLetters)
	return result
randomSymbolGenerator111._leadLetters = 'Il'
randomSymbolGenerator111._allLetters = randomSymbolGenerator111._leadLetters + '1'

def randomSymbolGenerator000(length) :
	result = random.choice(randomSymbolGenerator000._leadLetters)
	while len(result) < length :
		result += random.choice(randomSymbolGenerator000._allLetters)
	return result
randomSymbolGenerator000._leadLetters = 'oO'
randomSymbolGenerator000._allLetters = randomSymbolGenerator000._leadLetters + '0'

def randomSymbolGeneratorUnicode(length) :
	if randomSymbolGeneratorUnicode.charList is None :
		charList = []
		for i in range(0x100, 0x110000) :
			ch = chr(i)
			if ch.isidentifier() :
				charList.append(ch)
		randomSymbolGeneratorUnicode.charList = charList
	result = ''
	while len(result) < length :
		result += random.choice(randomSymbolGeneratorUnicode.charList)
	return result
randomSymbolGeneratorUnicode.charList = None

randomSymbolGenerator = randomSymbolGenerator111

def setRandomSymbolGenerator(generator) :
	global randomSymbolGenerator

	if generator is not None :
		randomSymbolGenerator = generator

def getRandomSymbol(length = None) :
	if length is None :
		length = random.randint(6, 20)
	return randomSymbolGenerator(length)

def getUnusedRandomSymbol(usedMap = None, originalName = None) :
	if usedMap is None :
		usedMap = _uniqueSymbolMap
	length = 8
	countDown = 5
	while True :
		newName = getRandomSymbol(length)
		#if originalName is not None :
		#	newName = newName + '_' + originalName + '_' + str(random.randint(1, 100000))
		if newName not in usedMap :
			usedMap[newName] = True
			_uniqueSymbolMap[newName] = True
			return newName
		if length is not None :
			if countDown > 0 :
				countDown -= 1
			if countDown <= 0 :
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


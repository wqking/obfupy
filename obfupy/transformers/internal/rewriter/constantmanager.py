from .. import util
from .. import astutil

import ast
import random
import enum

@enum.unique
class ItemType(enum.IntEnum) :
	constant = 1
	name = 2

strictValueTrue = '993FA0E09C7749DFA58A6A6BF7BE3DEB.tRue'
strictValueFalse = '616EB37E118B4B9581837807BABE67DA.fAlse'

def valueToStrict(value) :
	if value is True :
		return strictValueTrue
	if value is False :
		return strictValueFalse
	return value

def strictToValue(strict) :
	if strict == strictValueTrue :
		return True
	if strict == strictValueFalse :
		return False
	return strict

class ConstantManager :
	def __init__(self) :
		self._strictValueMap = {}
		self._nameMap = {}
		self._constantValueList = []

	def getConstantValueList(self) :
		return self._constantValueList

	def foundConstant(self, value) :
		strictValue = valueToStrict(value)
		if strictValue not in self._strictValueMap :
			self._strictValueMap[strictValue] = {
				'value' : value,
				'newName' : util.getUnusedRandomSymbol(),
				'type' : ItemType.constant
			}
			self._constantValueList.append(value)
		return self._strictValueMap[strictValue]

	def getConstantReplacedNode(self, value) :
		item = self.foundConstant(value)
		if item is None :
			return None
		return ast.Name(id = item['newName'], ctx = ast.Load())

	def foundName(self, name) :
		if name not in self._nameMap :
			self._nameMap[name] = {
				'value' : name,
				'newName' : util.getUnusedRandomSymbol(),
				'type' : ItemType.name
			}
		return self._nameMap[name]

	def getNameReplacedNode(self, name) :
		item = self.foundName(name)
		if item is None :
			return None
		return ast.Name(id = item['newName'], ctx = ast.Load())

	def getDefineNodes(self) :
		itemList = list(self._strictValueMap.values()) + list(self._nameMap.values())
		random.shuffle(itemList)
		targetList = []
		valueList = []
		for item in itemList :
			targetList.append(ast.Name(id = item['newName'], ctx = ast.Store()))
			valueNode = None
			if item['type'] == ItemType.constant :
				valueNode = astutil.makeConstant(item['value'])
			else :
				valueNode = ast.Name(id = item['value'], ctx = ast.Load())
			valueList.append(valueNode)
		return [ astutil.makeAssignment(targetList, valueList) ]
	

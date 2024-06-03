from .. import util
from .. import astutil
from . import logicmaker

import ast
import random
import enum
import sys

class StringEncoderManager :
	def __init__(self, stringEncoder) :
		self._stringEncoderList = []
		self.doParseStringEncoder(stringEncoder)
		self._encoderIndexList = [ i for i in range(len(self._stringEncoderList)) ]

	def encode(self, string) :
		random.shuffle(self._encoderIndexList)
		for i in self._encoderIndexList :
			encoder = self._stringEncoderList[i]
			node = encoder['encode'](string)
			if node is None :
				continue
			if encoder['extraNode'] is False and encoder['extraNodeGetter'] is not None :
				extraNode = encoder['extraNodeGetter']
				if callable(extraNode) :
					extraNode = extraNode()
				encoder['extraNode'] = extraNode
			return node
		return astutil.makeConstant(string)

	def loadExtraNode(self, extraNodeManager) :
		for encoder in self._stringEncoderList :
			if not encoder['extraNode'] :
				continue
			extraNodeManager.addNode(encoder['extraNode'])

	def doParseStringEncoder(self, stringEncoder) :
		if stringEncoder is None :
			return
		if isinstance(stringEncoder, list) :
			for item in stringEncoder :
				self.doParseStringEncoder(item)
			return
		extraNodeGetter = None
		encode = None
		if callable(stringEncoder) :
			encode = stringEncoder
		elif hasattr(stringEncoder, 'encode') :
			encode = stringEncoder.encode
		if encode is None :
			return
		if hasattr(stringEncoder, 'extraNode') :
			extraNodeGetter = stringEncoder.extraNode
		self._stringEncoderList.append({
			'encode' : encode,
			'extraNodeGetter' : extraNodeGetter,
			'extraNode' : False
		})

@enum.unique
class ItemType(enum.IntEnum) :
	constant = 1
	name = 2

strictValuePrefix = '616EB37E118B4B9581837807BABE67DA'

def valueToStrict(value) :
	return strictValuePrefix + type(value).__name__ + str(value)

class ConstantManager :
	def __init__(self, stringEncoders) :
		self._strictValueMap = {}
		self._nameMap = {}
		self._constantValueList = []
		self._stringEncoderManager = StringEncoderManager(stringEncoders)

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

	def loadExtraNode(self, extraNodeManager) :
		itemList = list(self._strictValueMap.values()) + list(self._nameMap.values())
		random.shuffle(itemList)
		targetList = []
		valueList = []
		for item in itemList :
			targetList.append(ast.Name(id = item['newName'], ctx = ast.Store()))
			valueNode = None
			if item['type'] == ItemType.constant :
				valueNode = self._doMakeConstantNode(item['value'])
			else :
				valueNode = ast.Name(id = item['value'], ctx = ast.Load())
			valueList.append(valueNode)
		self._stringEncoderManager.loadExtraNode(extraNodeManager)
		extraNodeManager.addNode(astutil.makeAssignment(targetList, valueList))

	def _doMakeConstantNode(self, value) :
		if isinstance(value, str) :
			return self._stringEncoderManager.encode(value)
		if value is True or value is False :
			return self._doMakeBoolNode(value)
		if isinstance(value, int) :
			return self._doMakeIntNode(value)
		return astutil.makeConstant(value)
	
	def _doMakeBoolNode(self, value) :
		node = logicmaker.LogicMaker().makeTrue(None, 1)
		if not value :
			node = astutil.makeNegation(node)
		return astutil.ensureLogicalNode(node)

	def _doMakeIntNode(self, value, depth = 3) :
		minValue = 1000000
		maxValue = 100000000
		if value < -sys.maxsize + maxValue or value > sys.maxsize - maxValue :
			return astutil.makeConstant(value)
		if depth <= 1 :
			return astutil.makeConstant(value)
		opTypeList = [
			ast.Add, ast.Sub,
			ast.BitXor, ast.BitXor, ast.BitXor, # more chance
			ast.Invert,
		]
		opType = random.choice(opTypeList)
		isUnaryOp = (opType == ast.Invert)
		requirePositive = (opType == ast.BitXor or opType == ast.Invert)
		needUnarySub = requirePositive and (value < 0)
		a = random.randint(minValue, maxValue)
		b = 0
		if opType == ast.Add :
			b = value - a
		elif opType == ast.Sub :
			b = a - value
		elif opType == ast.BitXor :
			b = a ^ abs(value)
		elif opType == ast.Invert :
			a = ~abs(value)
		else :
			raise Exception("Unknown operator")
		node = None
		if isUnaryOp :
			node = ast.UnaryOp(
				op = opType(),
				operand = self._doMakeIntNode(a, depth - 1)
			)
		else :
			node = ast.BinOp(
				left = self._doMakeIntNode(a, depth - 1),
				op = opType(),
				right = self._doMakeIntNode(b, depth - 1),
			)
		if needUnarySub :
			node = ast.UnaryOp(
				op = ast.USub(),
				operand = node
			)
		return node

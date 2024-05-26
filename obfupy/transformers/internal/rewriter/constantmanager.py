from .. import util

import ast

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
	def __init__(self, options) :
		self._enabled = False
		self._candidateMap = None
		self._strictValueIndexMap = {}
		self._valueList = []
		self._name = None
		option = options['constantAsVariable']
		if isinstance(option, list) :
			self._enabled = True
			for item in option :
				self._candidateMap[valueToStrict(item)] = None
		else :
			self._enabled = option

	def isEnabled(self) :
		return self._enabled
	
	def foundConstant(self, value) :
		if not self._enabled :
			return -1
		strictValue = valueToStrict(value)
		if self._candidateMap is not None and strictValue not in self._candidateMap :
			return -1
		if strictValue not in self._strictValueIndexMap :
			self._strictValueIndexMap[strictValue] = len(self._valueList)
			self._valueList.append(value)
		index = self._strictValueIndexMap[strictValue]
		return index

	def getReplacedNode(self, value) :
		if not self._enabled :
			return None
		index = self.foundConstant(value)
		if index < 0 :
			return None
		return ast.Subscript(
			value = ast.Name(id = self._doGetName(), ctx = ast.Load()),
			slice = ast.Constant(value = index),
			ctx = ast.Load()
		)

	def getDefineNodes(self) :
		if self._name is None :
			return []
		valueList = []
		for value in self._valueList :
			valueList.append(ast.Constant(value = value))
		newNode = ast.Assign(
			targets = [ ast.Name(id = self._doGetName(), ctx = ast.Store()) ],
			value = ast.List(elts = valueList, ctx = ast.Load())
		)
		return [ newNode ]
	
	def _doGetName(self) :
		if self._name is None :
			self._name = util.getUnusedRandomSymbol()
		return self._name


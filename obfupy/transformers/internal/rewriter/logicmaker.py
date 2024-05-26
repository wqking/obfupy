from .. import astutil
from .. import util

import random
import ast

class LogicMaker :
	def __init__(self, nopMaker = None, symbols = [], strings = []) :
		self._nopMaker = nopMaker
		self._symbols = symbols
		self._strings = strings

	def makeTrue(self, node, depth = 3) :
		return self._doMakeTrue(node, depth)

	def _doMakeTrue(self, node, depth) :
		if node is None :
			node = self._doMakePrimaryTrue()
		if depth <= 0 :
			return node
		operatorList = [ ast.And, ast.Or ]
		opType = random.choice(operatorList)
		nodeList = [
			self._doMakeTrue(node, depth - 1),
			self._doMakeTrue(None, depth - 1)
		]
		if opType == ast.Or :
			nodeList[1] = astutil.makeNegation(nodeList[1])
		if util.hasChance(2) :
			nodeList[0], nodeList[1] = nodeList[1], nodeList[0]
		return ast.BoolOp(
			op = opType(),
			values = nodeList
		)

	def _doMakePrimaryTrue(self) :
		callbackList = []
		callbackList.append(self._doMakePrimaryTrueFromConstantCompare)
		callbackList.append(self._doMakePrimaryTrueFromConstant)
		if self._nopMaker is not None :
			callbackList.append(self._doMakePrimaryTrueFromNopMaker)
		callback = random.choice(callbackList)
		return callback()

	def _doMakePrimaryTrueFromConstantCompare(self) :
		operatorList = [
			[ ast.Lt, 0, 1 ],
			[ ast.LtE, 0, 1 ],
			[ ast.Gt, 1, 0 ],
			[ ast.GtE, 1, 0 ],
			[ ast.Eq, 0, 0 ],
			[ ast.NotEq, 0, 1 ],
		]
		operator = random.choice(operatorList)
		smallValue = random.randint(0, 50)
		largeValue = random.randint(smallValue + 1, 100)
		values = [ 0, 0 ]
		for i in range(1, 3, 1) :
			n = operator[i]
			if n == 0 :
				values[i - 1] = smallValue
			else :
				values[i - 1] = largeValue
		opType = operator[0]
		if util.hasChance(2) and opType == ast.NotEq :
			values[0], values[1] = values[1], values[0]

		return ast.Compare(
			left = ast.Constant(value = values[0]),
			ops = [ opType() ],
			comparators = [ ast.Constant(value = values[1]) ]
		)

	def _doMakePrimaryTrueFromConstant(self) :
		return ast.Constant(value = random.randint(1, 50))

	def _doMakePrimaryTrueFromNopMaker(self) :
		return self._nopMaker.makeTrueNode(ast.Constant(value = random.randint(1, 50)))

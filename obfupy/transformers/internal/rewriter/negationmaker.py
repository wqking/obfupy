from .. import astutil
from .. import util

import ast

class NegationMaker :
	def __init__(self, useCompareWrapper) :
		self._useCompareWrapper = useCompareWrapper
		self._compareWrapperMap = {}

	def setUseCompareWrapper(self, useCompareWrapper) :
		self._useCompareWrapper = useCompareWrapper

	def makeNegation(self, node) :
		if isinstance(node, ast.Compare) :
			newNode = self._doMakeCompareNegation(node)
			if newNode is not None :
				return newNode
		if isinstance(node, ast.BoolOp) :
			newNode = self._doMakeBoolOpNegation(node)
			if newNode is not None :
				return newNode
		if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not) :
			return node.operand
		if isinstance(node, ast.Constant) :
			if node.value is True :
				return astutil.makeConstant(False)
			elif node.value is False :
				return astutil.makeConstant(True)
		return astutil.addNot(node)
		
	def loadExtraNode(self, extraNodeManager) :
		for name in self._compareWrapperMap :
			extraNodeManager.addNode(self._compareWrapperMap[name])

	# a < b -> a >= b
	def _doMakeCompareNegation(self, node) :
		if len(node.ops) > 1 :
			values = []
			left = node.left
			for i in range(len(node.ops)) :
				right = node.comparators[i]
				op = node.ops[i]
				newCompare = ast.Compare(
					left = left,
					ops = [ op ],
					comparators = [ right ]
				)
				left = right
				values.append(newCompare)
			newNode = ast.BoolOp(
				op = ast.And(),
				values = values
			)
			return self.makeNegation(newNode)
		if self._needToMakeCompareWrapper(node) :
			return self._doMakeCompareWrapper(node)
		else :
			opType = type(node.ops[0])
			newOpType = astutil.getNegationLogicalOp(opType)
			if newOpType is None :
				return None
			return ast.Compare(
				left = node.left,
				ops = [ newOpType() ],
				comparators = node.comparators
			)

	# a and b -> ~a or ~b
	def _doMakeBoolOpNegation(self, node) :
		newValues = []
		for value in node.values :
			newNode = self.makeNegation(value)
			if newNode is None :
				return None
			newValues.append(newNode)
		newOpType = ast.Or
		if type(node.op) == ast.Or :
			newOpType = ast.And
		return ast.BoolOp(
			op = newOpType(),
			values = newValues
		)

	def _needToMakeCompareWrapper(self, node) :
		if not self._useCompareWrapper :
			return False
		for op in node.ops :
			if type(op) not in [ ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Eq, ast.NotEq ] :
				return False
		return True

	def _doMakeCompareWrapper(self, node) :
		opType = type(node.ops[0])
		negativeOpType = astutil.getNegationLogicalOp(opType)
		opFunc = self._doGetCompareWrapperForOp(negativeOpType)
		return ast.Call(
			func = ast.Name(id = opFunc.name, ctx = ast.Load()),
			args = [
				node.left,
				node.comparators[0]
			],
			keywords = []
		)

	def _doGetCompareWrapperForOp(self, opType) :
		name = opType.__name__
		if name not in self._compareWrapperMap :
			self._compareWrapperMap[name] = self._doMakeCompareWrapperForOp(opType)
		return self._compareWrapperMap[name]

	def _doMakeCompareWrapperForOp(self, opType) :
		negativeOpType = astutil.getNegationLogicalOp(opType)
		funcName = util.getUnusedRandomSymbol()
		argLeft = util.getUnusedRandomSymbol()
		argRight = util.getUnusedRandomSymbol()
		return ast.FunctionDef(
			name = funcName,
			args = ast.arguments(
				posonlyargs=[],
				args=[
					ast.arg(arg = argLeft),
					ast.arg(arg = argRight),
				],
				kwonlyargs = [],
				kw_defaults = [],
				defaults = []
			),
			body = [
				ast.Try(
                    body = [
						ast.Return(
							value = ast.Compare(
								left = ast.Name(id = argLeft, ctx = ast.Load()),
								ops = [
									opType()
								],
								comparators = [
									ast.Name(id = argRight, ctx = ast.Load())
								]
							)
						)
					],
					handlers = [
						ast.ExceptHandler(
							body = [
								ast.Return(
									value = ast.UnaryOp(
										op = ast.Not(),
										operand = ast.Compare(
											left = ast.Name(id = argLeft, ctx = ast.Load()),
											ops = [
												negativeOpType()
											],
											comparators = [
												ast.Name(id = argRight, ctx = ast.Load())
											]
										)
									)
								)
							]
						)
					],
					orelse = [],
					finalbody = []
					)
			],
			decorator_list = []
		)

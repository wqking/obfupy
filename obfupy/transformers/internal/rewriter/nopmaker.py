from .. import astutil
from .. import util

import random
import ast

class NopWithClass :
	def __init__(self) :
		self._className = util.getUnusedRandomSymbol()
		self._trueMethodName = util.getUnusedRandomSymbol()
		self._returnAsMethodName = util.getUnusedRandomSymbol()
		self._argName = util.getUnusedRandomSymbol()

	def makeTrueNode(self, argNode) :
		return self.doGetUseNode(self._trueMethodName, argNode)

	def makeReturnAsNode(self, argNode) :
		return self.doGetUseNode(self._returnAsMethodName, argNode)
	
	def getDefineNodes(self) :
		result = [
			ast.ClassDef(
				name = self._className,
				bases = [],
				keywords = [],
				body=[
					self.doMakeFunctionDef(self._trueMethodName, ast.Constant(value = True)),
					self.doMakeFunctionDef(self._returnAsMethodName, ast.Name(id = self._argName, ctx = ast.Load()))
				],
				decorator_list = []
			)
		]
		return result
	
	def doMakeFunctionDef(self, funcName, returnValueNode) :
		return ast.FunctionDef(
			name = funcName,
			args = ast.arguments(
				posonlyargs=[],
				args=[
					ast.arg(arg = self._argName)
				],
				kwonlyargs = [],
				kw_defaults = [],
				defaults = []
			),
			body = [
				ast.Return(value = returnValueNode)],
			decorator_list = [
				ast.Name(id = 'staticmethod', ctx = ast.Load())
			]
		)

	def doGetUseNode(self, funcName, argNode) :
		return ast.Call(
			func = ast.Attribute(
				value = ast.Name(id = self._className, ctx = ast.Load()),
				attr = funcName
			),
			args = [ argNode ],
			keywords = []
		)

class NopWithFunction :
	def __init__(self) :
		self._trueMethodName = util.getUnusedRandomSymbol()
		self._returnAsMethodName = util.getUnusedRandomSymbol()
		self._argName = util.getUnusedRandomSymbol()

	def makeTrueNode(self, argNode) :
		return self.doGetUseNode(self._trueMethodName, argNode)

	def makeReturnAsNode(self, argNode) :
		return self.doGetUseNode(self._returnAsMethodName, argNode)
	
	def getDefineNodes(self) :
		result = [
			self.doMakeFunctionDef(self._trueMethodName, ast.Constant(value = True)),
			self.doMakeFunctionDef(self._returnAsMethodName, ast.Name(id = self._argName, ctx = ast.Load()))
		]
		return result
	
	def doMakeFunctionDef(self, funcName, returnValueNode) :
		return ast.FunctionDef(
			name = funcName,
			args = ast.arguments(
				posonlyargs=[],
				args=[
					ast.arg(arg = self._argName)
				],
				kwonlyargs = [],
				kw_defaults = [],
				defaults = []
			),
			body = [
				ast.Return(value = returnValueNode)],
			decorator_list = []
		)

	def doGetUseNode(self, funcName, argNode) :
		return ast.Call(
			func = ast.Name(id = funcName, ctx = ast.Load()),
			args = [ argNode ],
			keywords = []
		)

class NopWithLambda :
	def __init__(self) :
		self._trueMethodName = util.getUnusedRandomSymbol()
		self._returnAsMethodName = util.getUnusedRandomSymbol()
		self._argName = util.getUnusedRandomSymbol()

	def makeTrueNode(self, argNode) :
		return self.doGetUseNode(self._trueMethodName, argNode)

	def makeReturnAsNode(self, argNode) :
		return self.doGetUseNode(self._returnAsMethodName, argNode)
	
	def getDefineNodes(self) :
		result = [
			self.doMakeAssign(self._trueMethodName, ast.Constant(value = True)),
			self.doMakeAssign(self._returnAsMethodName, ast.Name(id = self._argName, ctx = ast.Load()))
		]
		return result
	
	def doMakeAssign(self, varName, returnValueNode) :
		return ast.Assign(
			targets = [ ast.Name(id = varName, ctx = ast.Store) ],
			value = self.doMakeLambda(returnValueNode)
		)
	def doMakeLambda(self, returnValueNode) :
		return ast.Lambda(
			args = ast.arguments(
				posonlyargs=[],
				args=[
					ast.arg(arg = self._argName)
				],
				kwonlyargs = [],
				kw_defaults = [],
				defaults = []
			),
			body = returnValueNode
		)

	def doGetUseNode(self, funcName, argNode) :
		return ast.Call(
			func = ast.Name(id = funcName, ctx = ast.Load()),
			args = [ argNode ],
			keywords = []
		)

class NopMaker :
	def __init__(self) :
		self._makerClassList = [ NopWithClass, NopWithFunction, NopWithLambda ]
		random.shuffle(self._makerClassList)
		self._makerCount = len(self._makerClassList)
		self._makerList = [ None for _ in range(self._makerCount) ]

	def makeTrueNode(self, argNode) :
		return self.doGetMaker().makeTrueNode(argNode)

	def makeReturnAsNode(self, argNode) :
		return self.doGetMaker().makeReturnAsNode(argNode)
	
	def getDefineNodes(self) :
		result = []
		for maker in self._makerList :
			if maker is None :
				continue
			result += maker.getDefineNodes()
		return result

	def doGetMaker(self) :
		index = random.randint(0, self._makerCount - 1)
		if self._makerList[index] is None :
			self._makerList[index] = self._makerClassList[index]()
		return self._makerList[index]

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
		return self._doGetUseNode(self._trueMethodName, argNode)

	def makeReturnAsNode(self, argNode) :
		return self._doGetUseNode(self._returnAsMethodName, argNode)
	
	def getDefineNodes(self) :
		result = [
			ast.ClassDef(
				name = self._className,
				bases = [],
				keywords = [],
				body=[
					self._doMakeFunctionDef(self._trueMethodName, astutil.makeConstant(True)),
					self._doMakeFunctionDef(self._returnAsMethodName, ast.Name(id = self._argName, ctx = ast.Load()))
				],
				decorator_list = []
			)
		]
		return result
	
	def _doMakeFunctionDef(self, funcName, returnValueNode) :
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

	def _doGetUseNode(self, funcName, argNode) :
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
		return self._doGetUseNode(self._trueMethodName, argNode)

	def makeReturnAsNode(self, argNode) :
		return self._doGetUseNode(self._returnAsMethodName, argNode)
	
	def getDefineNodes(self) :
		result = [
			self._doMakeFunctionDef(self._trueMethodName, astutil.makeConstant(True)),
			self._doMakeFunctionDef(self._returnAsMethodName, ast.Name(id = self._argName, ctx = ast.Load()))
		]
		return result
	
	def _doMakeFunctionDef(self, funcName, returnValueNode) :
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

	def _doGetUseNode(self, funcName, argNode) :
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
		return self._doGetUseNode(self._trueMethodName, argNode)

	def makeReturnAsNode(self, argNode) :
		return self._doGetUseNode(self._returnAsMethodName, argNode)
	
	def getDefineNodes(self) :
		result = [
			self._doMakeAssign(self._trueMethodName, astutil.makeConstant(True)),
			self._doMakeAssign(self._returnAsMethodName, ast.Name(id = self._argName, ctx = ast.Load()))
		]
		return result
	
	def _doMakeAssign(self, varName, returnValueNode) :
		return ast.Assign(
			targets = [ ast.Name(id = varName, ctx = ast.Store) ],
			value = self._doMakeLambda(returnValueNode)
		)
	def _doMakeLambda(self, returnValueNode) :
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

	def _doGetUseNode(self, funcName, argNode) :
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
		node = self._doGetMaker().makeTrueNode(argNode)
		return astutil.fixMissingLocations(node)

	def makeReturnAsNode(self, argNode) :
		node = self._doGetMaker().makeReturnAsNode(argNode)
		return astutil.fixMissingLocations(node)
	
	def loadExtraNode(self, extraNodeManager) :
		result = []
		for maker in self._makerList :
			if maker is None :
				continue
			result += maker.getDefineNodes()
		extraNodeManager.addNode(result)

	def _doGetMaker(self) :
		index = random.randint(0, self._makerCount - 1)
		if self._makerList[index] is None :
			self._makerList[index] = self._makerClassList[index]()
		return self._makerList[index]

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

from . import context
from . import rewriterutil
from .. import astutil
from .. import util
from ... import rewriter

import ast
import copy
import random

class FunctionRewriter :
	def __init__(self, visitor) :
		self._visitor = visitor

	def rewriteFunction(self, node) :
		with self._visitor._contextStack.pushContext(rewriterutil.getNodeContext(node)) as currentContext :
			if self._visitor._shouldSkip() :
				return node
			node = self._visitor._removeDocString(node)
			node.decorator_list = self._visitor._doVisit(node.decorator_list, context.Section.decorator)
			newNode = self._doExtractFunction(node)
			if newNode is not None :
				node = newNode
			else :
				node = self._doAliasFunctionArguments(node)
		node = astutil.fixMissingLocations(node)
		return node
	
	def _doAliasFunctionArguments(self, node) :
		currentContext = self._visitor.getCurrentContext()
		node.name = currentContext.getParent().findRenamedName(node.name) or node.name
		renamedArgs = self._doCreateRenamedArgs(node)
		for item in renamedArgs['renamedArgList'] :
			currentContext.renameSymbol(item['argName'], item['newName'])
		node.body = self._visitor._doVisit(node.body, context.Section.body)
		if renamedArgs['node'] is not None :
			index = rewriterutil.findFirstInsertableIndex(node)
			node.body.insert(index, renamedArgs['node'])
		node.args = self._visitor._doVisitArgumentDefaults(node.args)
		return node
	
	def _canExtractFunction(self, node) :
		# Don't extract special names such as __cast, which name is mangled.
		if util.isNameMangling(node.name) :
			return False
		if isinstance(node, ast.AsyncFunctionDef) :
			return False
		currentContext = rewriterutil.getNodeContext(node)
		# If the function contains any managed names, don't extract because the names are not accessible outside of the class
		for name in currentContext.getSeenNameSet() :
			if util.isNameMangling(name) :
				return False
		if currentContext.isNameSeen('super') :
			return False
		if currentContext.isFeatureSeen(rewriterutil.featureYield) :
			return False
		if self._visitor._needToKeepLocalVariables() :
			return False
		parentContext = currentContext
		while True :
			parentContext = parentContext.getParent()
			if parentContext is None :
				break
			if not (parentContext.isModule() or parentContext.isClass()) :
				return False
		return True

	def _doExtractFunction(self, node) :
		if not self._visitor._getOptions().extractFunction :
			return None
		if not self._canExtractFunction(node) :
			return None
		newName = util.getUnusedRandomSymbol()
		newFuncNode = ast.FunctionDef(
			name = newName,
			args = copy.deepcopy(node.args),
			body = copy.deepcopy(node.body),
			decorator_list = [],
			returns = copy.deepcopy(node.returns),
		)
		newFuncNode.args.defaults = []
		newFuncNode.returns = None
		# The default has to be there but it may contain symbols not known in the new function.
		# So we just change the default to 0. It's fine since the value is always provided by the forward call.
		newFuncNode.args.kw_defaults = [0] * len(newFuncNode.args.kw_defaults)
		# Don't deep copy to newContext, otherwise the nested functions won't work because the 'parent' context has issue.
		newContext = rewriterutil.getNodeContext(node)
		rewriterutil.setNodeContext(newFuncNode, newContext)

		posonlyargsIndexList = util.makeShuffledIndexList(len(newFuncNode.args.posonlyargs))
		argsIndexList = util.makeShuffledIndexList(len(newFuncNode.args.args))
		kwonlyargsIndexList = util.makeShuffledIndexList(len(newFuncNode.args.kwonlyargs))
		newFuncNode.args.posonlyargs = util.makeListByIndexList(newFuncNode.args.posonlyargs, posonlyargsIndexList)
		newFuncNode.args.args = util.makeListByIndexList(newFuncNode.args.args, argsIndexList)
		newFuncNode.args.kwonlyargs = util.makeListByIndexList(newFuncNode.args.kwonlyargs, kwonlyargsIndexList)

		def callback(argItem) :
			argItem.arg = newContext.renameSymbol(argItem.arg)
			argItem.annotation = None
		astutil.enumerateArguments(newFuncNode.args, callback)

		self._visitor._contextStack.saveAndReset()
		with self._visitor._contextStack.pushContext(newContext) :
			newFuncNode.body = self._visitor._doVisit(newFuncNode.body, context.Section.body)
		self._visitor._contextStack.restore()

		newCall = self._doCreateForwardCall(
			newFuncNode.name,
			newContext,
			util.makeListByIndexList(node.args.posonlyargs, posonlyargsIndexList),
			util.makeListByIndexList(node.args.args, argsIndexList),
			node.args.vararg,
			util.makeListByIndexList(node.args.kwonlyargs, kwonlyargsIndexList),
			node.args.kwarg
		)
		newBody = ast.Return(
			value = newCall
		)
		if astutil.isChildDocString(node) :
			node.body = [ node.body[0] ]
		else :
			node.body = []
		node.body += [ newBody ]
		self._visitor._contextStack.getTopScopedContext().addSiblingNode(newFuncNode)
		return node
	
	def _doCreateForwardCall(
			self,
			newFuncName,
			newContext,
			posonlyargs,
			args,
			vararg,
			kwonlyargs,
			kwarg
		) :
		callArgs = []
		callKeywords = []
		argList = [ posonlyargs, args ]
		for itemList in argList :
			for argItem in itemList :
				if argItem is None :
					continue
				callArgs.append(ast.Name(id = argItem.arg, ctx = ast.Load()))
		if vararg :
			callArgs.append(ast.Starred(
				value = ast.Name(id = vararg.arg, ctx = ast.Load()),
				ctx = ast.Load()
			))
		for argItem in kwonlyargs :
			if argItem is None :
				continue
			callKeywords.append(
				ast.keyword(
					arg = newContext.findRenamedName(argItem.arg) or argItem.arg,
					value = ast.Name(id = argItem.arg, ctx = ast.Load())
				)
			)
		if kwarg :
			callKeywords.append(ast.keyword(value = ast.Name(id = kwarg.arg, ctx = ast.Load())))
		return ast.Call(
			func = ast.Name(newFuncName, ctx = ast.Load()),
			args = callArgs,
			keywords = callKeywords
		)

	def _doCreateRenamedArgs(self, node) :
		currentContext = self._visitor.getCurrentContext()
		canRename = True
		if not self._visitor._getOptions().aliasFunctionArgument :
			canRename = False
		if self._visitor._needToKeepLocalVariables() :
			canRename = False
		if not canRename :
			return {
				'node' : None,
				'renamedArgList' : [],
			}

		renamedArgList = []
		
		def callback(argItem) :
			renamedArgList.append({
				'newName' : currentContext.createNewName(argItem.arg),
				'argName' : argItem.arg
			})
		astutil.enumerateArguments(node.args, callback)

		newNode = None
		if len(renamedArgList) > 0 :
			random.shuffle(renamedArgList)
			targetList = []
			valueList = []
			for item in renamedArgList :
				targetList.append(ast.Name(id = item['newName'], ctx = ast.Store()))
				valueList.append(ast.Name(id = item['argName'], ctx = ast.Load()))
			newNode = astutil.makeAssignment(targetList, valueList)
		return {
			'node' : newNode,
			'renamedArgList' : renamedArgList,
		}

	def _convertFunctionToLambda(self, node) :
		if type(node) != ast.FunctionDef :
			return None
		if len(node.decorator_list) > 0 :
			return None
		if len(node.body) != 1 :
			return None
		if util.isSpecialFunctionName(node.name) :
			return None
		bodyNode = node.body[0]
		lambdaBody = None
		if isinstance(bodyNode, ast.Pass) :
			lambdaBody = bodyNode
		elif isinstance(bodyNode, ast.Return) :
			lambdaBody = bodyNode.value
		else :
			return None

		arguments = copy.deepcopy(node.args)
		def callback(argItem) :
			argItem.annotation = None
			argItem.type_comment = None
		astutil.enumerateArguments(arguments, callback)

		lambdaNode = ast.Lambda(
			args = arguments,
			body = lambdaBody
		)
		return astutil.makeAssignment(ast.Name(id = node.name, ctx = ast.Store()), lambdaNode)


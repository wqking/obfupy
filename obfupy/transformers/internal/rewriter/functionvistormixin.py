from . import context
from . import rewriterutil
from .. import astutil
from .. import util
from ... import rewriter

import ast
import copy
import random

class FunctionVistorMixin :
	def _doVisitFunction(self, node) :
		node = astutil.removeDocString(node)
		# Visiting decorator_list must be outside of the function context
		node.decorator_list = self._doVisitNodeList(node.decorator_list)
		with context.ContextGuard(self._contextStack, rewriterutil.getNodeContext(node)) as currentContext :
			newNode = self._doExtractFunction(node)
			if newNode is not None :
				node = newNode
			else :
				node = self._doAliasFunctionArguments(node)
		return node
	
	def _doAliasFunctionArguments(self, node) :
		currentContext = self._contextStack.getCurrentContext()
		node.name = currentContext.getParentContext().findRenamedName(node.name) or node.name
		renamedArgs = self._doCreateRenamedArgs(node)
		for item in renamedArgs['renamedArgList'] :
			currentContext.renameSymbol(item['argName'], item['newName'])
		node.body = self._doVisitNodeList(node.body)
		if renamedArgs['node'] is not None :
			node.body.insert(0, renamedArgs['node'])
		node.args = self._doVisitArgumentDefaults(node.args)
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
		for name in currentContext.getSeenAttributeSet() :
			if util.isNameMangling(name) :
				return False
		if currentContext.isNameSeen('super') :
			return False
		if currentContext.isFeatureSeen(rewriterutil.featureYield) :
			return False
		parentContext = currentContext
		while True :
			parentContext = parentContext.getParentContext()
			if parentContext is None :
				break
			if not (parentContext.isModule() or parentContext.isClass()) :
				return False
		return True

	def _doExtractFunction(self, node) :
		if not self._getOption(rewriter.OptionNames.extractFunction) :
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

		self._contextStack.saveAndReset()
		with context.ContextGuard(self._contextStack, newContext) :
			newFuncNode.body = self._doVisitNodeList(newFuncNode.body)
		self._contextStack.restore()

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
		node.body = [ newBody ]
		self._contextStack.getTopScopedContext().addSiblingNode(newFuncNode)
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
		renamedArgList = []
		currentContext = self.getCurrentContext()
		
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


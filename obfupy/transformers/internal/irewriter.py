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

import ast
import random
import copy

from . import util
from . import astutil
from . import reentryguard
from . import builtinfunctions
from .rewriter import constantmanager
from .rewriter import truemaker
from .rewriter import nopmaker
from .rewriter import context
from .rewriter import codeblockmaker
from .rewriter import extranodemanager
from .rewriter import functionrewriter
from .rewriter import ifrewriter
from .rewriter import rewriterutil
from .rewriter import negationmaker
from .. import rewriter
from . import callbackdata

def _ctxToNameType(ctx) :
	if isinstance(ctx, ast.Store) :
		return context.NameType.store
	if isinstance(ctx, ast.Del) :
		return context.NameType.delete
	return context.NameType.load

class _CallbackContext :
	def __init__(self, currentContext) :
		self._currentContext = currentContext
		self._parent = False

	def isModule(self) :
		return self._currentContext.isModule()

	def isClass(self) :
		return self._currentContext.isClass()

	def isFunction(self) :
		return self._currentContext.isFunction()
	
	def getName(self) :
		return self._currentContext.getContextName()
	
	def getParent(self) :
		if self._parent is False :
			parentContext = self._currentContext.getParent()
			if parentContext is None :
				self._parent = None
			else :
				self._parent = _CallbackContext(parentContext)
		return self._parent

class _RewriterCallbackData(callbackdata._OptionCallbackData) :
	def __init__(self, fileName, options, currentContext) :
		super().__init__(fileName, options)
		self._currentContext = currentContext
		self._callbackContext = None

	def isFile(self) :
		return self._currentContext is None
	
	def getContext(self) :
		if self._callbackContext is None and not self.isFile() :
			self._callbackContext = _CallbackContext(self._currentContext)
		return self._callbackContext
	
def _invokeCallback(callback, fileName, options, currentContext) :
	if callback is None :
		return None
	data = _RewriterCallbackData(fileName, options, currentContext)
	return callbackdata._invokeCallback(callback, data)

class _BaseAstVistor(ast.NodeTransformer) :
	def __init__(self, contextStack, options, specialOptions, fileName, callback) :
		super().__init__()
		self._contextStack = contextStack
		self._options = options
		self._specialOptions = specialOptions
		self._fileName = fileName
		self._callback = callback
		self._reentryGuard = reentryguard.ReentryGuard()

	def getCurrentContext(self, adjustBySection = True) :
		currentContext = self._contextStack.getCurrentContext()
		if adjustBySection :
			section = currentContext.getCurrentSection()
			if section not in [ None, context.Section.body ] :
				parent = currentContext.getParent()
				if parent is None :
					print(currentContext.getContextName(), section)
					assert parent is not None
				currentContext = parent
		return currentContext
	
	def _getOptions(self) :
		currentContext = self.getCurrentContext(False)
		options = currentContext.getOptions()
		return options

	def _shouldSkip(self) :
		return not self._getOptions().enabled

	def _doVisit(self, nodeList, section = None) :
		if nodeList is None :
			return nodeList
		with self.getCurrentContext(False).pushSection(section) :
			if not isinstance(nodeList, list) :
				return self.visit(nodeList)
			result = []
			for node in nodeList :
				if node is None :
					result.append(node)
					continue
				newNode = self.visit(node)
				if newNode is not None :
					result.append(newNode)
			return result

	def _doGenericVisit(self, node, section = None) :
		with self.getCurrentContext(False).pushSection(section) :
			return self.generic_visit(node)

	def _doVisitArgumentDefaults(self, arguments) :
		arguments.kw_defaults = self._doVisit(arguments.kw_defaults, context.Section.argument)
		arguments.defaults = self._doVisit(arguments.defaults, context.Section.argument)
		return arguments
	
	def _prepareNodeContext(self, node, currentContext) :
		rewriterutil.setNodeContext(node, currentContext)
		options = _invokeCallback(self._callback, self._fileName, currentContext.getOptions(), currentContext)
		if options is not None :
			currentContext.setOptions(options)

	def _needToKeepLocalVariables(self) :
		return self.getCurrentContext().isNameSeen('locals')

class _AstVistorPreprocess(_BaseAstVistor) :
	def __init__(self, contextStack, options, specialOptions, fileName, callback) :
		super().__init__(contextStack, options, specialOptions, fileName, callback)

	def visit_Module(self, node) :
		with self._contextStack.pushContext(context.ModuleContext(self._fileName, copy.deepcopy(self._options))) as currentContext :
			self._prepareNodeContext(node, currentContext)
			rewriterutil.markNodeDocString(node)
			return self._doGenericVisit(node)

	def visit_ClassDef(self, node):
		with self._contextStack.pushContext(context.ClassContext(node.name)) as currentContext :
			self._prepareNodeContext(node, currentContext)
			rewriterutil.markNodeDocString(node)
			return self._doGenericVisit(node)

	def visit_AsyncFunctionDef(self, node):
		return self._doVisitFunctionDef(node)

	def visit_FunctionDef(self, node) :
		return self._doVisitFunctionDef(node)

	def _doVisitFunctionDef(self, node) :
		with self._contextStack.pushContext(context.FunctionContext(node.name)) as currentContext :
			self._prepareNodeContext(node, currentContext)
			rewriterutil.markNodeDocString(node)
			currentContext.seeName(node.name, context.NameType.store)
			# Function name is visible in both the function scope and outter scope
			currentContext.getParent().seeName(node.name, context.NameType.store)
			node.decorator_list = self._doVisit(node.decorator_list, context.Section.decorator)
			self._doVisitArguments(node.args)
			node.body = self._doVisit(node.body, context.Section.body)
			node.args = self._doVisitArgumentDefaults(node.args)
			return node
		
	def visit_Lambda(self, node) :
		with self._contextStack.pushContext(context.FunctionContext('#lambda')) as currentContext :
			self._prepareNodeContext(node, currentContext)
			self._doVisitArguments(node.args)
			return self._doGenericVisit(node)

	def _doVisitArguments(self, arguments) :
		currentContext = self.getCurrentContext()
		def callback(argItem) :
			currentContext.seeName(argItem.arg, context.NameType.argument)
		astutil.enumerateArguments(arguments, callback)

	def visit_Name(self, node) :
		self.getCurrentContext().seeName(node.id, _ctxToNameType(node.ctx))
		if self._getOptions().renameLocalVariable and self._canRenameNameNode(node) :
			self.getCurrentContext().renameSymbol(node.id)
		return node
	
	def visit_Attribute(self, node) :
		self.getCurrentContext().seeName(node.attr, context.NameType.attribute)
		return self._doGenericVisit(node)

	def visit_Global(self, node) :
		for name in node.names :
			self.getCurrentContext().seeName(name, context.NameType.globalScope)
		return self._doGenericVisit(node)

	def visit_Nonlocal(self, node) :
		currentContext = self.getCurrentContext()
		for i in range(len(node.names)) :
			name = node.names[i]
			currentContext.seeName(name, context.NameType.nonlocalScope)
		return self._doGenericVisit(node)

	def visit_Yield(self, node) :
		currentContext = self.getCurrentContext()
		currentContext.seeFeature(rewriterutil.featureYield)
		return self._doGenericVisit(node)

	def visit_YieldFrom(self, node) :
		currentContext = self.getCurrentContext()
		currentContext.seeFeature(rewriterutil.featureYield)
		return self._doGenericVisit(node)

	def _canRenameNameNode(self, node) :
		currentContext = self.getCurrentContext()
		if not currentContext.isFunction() :
			return False
		if not isinstance(node.ctx, ast.Store) :
			return False
		if currentContext.isNameSeen(node.id, [
			context.NameType.globalScope, context.NameType.nonlocalScope, context.NameType.argument
		]) :
			return False
		if node.id in self._specialOptions.preservedNames :
			return False
		return True

class _AstVistorRewrite(_BaseAstVistor) :
	def __init__(self, contextStack, options, specialOptions, fileName, callback) :
		super().__init__(contextStack, options, specialOptions, fileName, callback)
		self._functionRewriter = functionrewriter.FunctionRewriter(self)
		self._ifRewriter = ifrewriter.IfRewriter(self)
		self._constantManager = constantmanager.ConstantManager(self._specialOptions.stringEncoders)
		self._nopMaker = nopmaker.NopMaker()
		self._trueMaker = truemaker.TrueMaker(self._nopMaker, constants = self._constantManager.getConstantValueList())
		self._codeBlockMaker = codeblockmaker.CodeBlockMaker(self._trueMaker)
		self._negationMaker = None

	def visit_Module(self, node) :
		with self._contextStack.pushContext(rewriterutil.getNodeContext(node)) :
			if self._shouldSkip() :
				return node
			node = self._removeDocString(node)
			node = self._doGenericVisit(node)
			extraNodeManager = extranodemanager.ExtraNodeManager()
			extraNodeSourceList = [ self._constantManager, self._nopMaker, self._negationMaker ]
			for item in extraNodeSourceList :
				if item is not None :
					item.loadExtraNode(extraNodeManager)
			index = rewriterutil.findFirstInsertableIndex(node)
			self._prependNodes(node.body, extraNodeManager.getNodeList(), self._findIndexNotImport(node.body, index))
			return node

	# This is to avoid SyntaxError: from __future__ imports must occur at the beginning of the file
	def _findIndexNotImport(self, nodeList, index) :
		for node in nodeList :
			index += 1
			if isinstance(node, ast.Constant) :
				continue
			if isinstance(node, ast.Import) :
				continue
			if isinstance(node, ast.ImportFrom) :
				continue
			index -= 1
			break
		return index

	def _makeResultNode(self, node) :
		context = rewriterutil.getNodeContext(node)
		siblingList = context.getSiblingNodeList()
		if len(siblingList)  == 0 :
			return node
		return siblingList + [ node ]

	def visit_ClassDef(self, node):
		with self._contextStack.pushContext(rewriterutil.getNodeContext(node)) :
			if self._shouldSkip() :
				return node
			node = self._removeDocString(node)
			node.bases = self._doVisit(node.bases, context.Section.baseClass)
			node.keywords = self._doVisit(node.keywords, context.Section.metaClass)
			node.decorator_list = self._doVisit(node.decorator_list, context.Section.decorator)
			node.body = self._doVisit(node.body, context.Section.body)
			return self._makeResultNode(node)

	def visit_AsyncFunctionDef(self, node):
		node.body = self._eliminateDeadCodeForNodeList(node.body)
		node = self._functionRewriter.rewriteFunction(node)
		return self._makeResultNode(node)

	def visit_FunctionDef(self, node) :
		node.body = self._eliminateDeadCodeForNodeList(node.body)
		node = self._functionRewriter.rewriteFunction(node)
		return self._makeResultNode(node)
		
	def visit_Lambda(self, node) :
		with self._contextStack.pushContext(rewriterutil.getNodeContext(node)) :
			if self._shouldSkip() :
				return node
			return self._doGenericVisit(node)

	def visit_Name(self, node) :
		if self._getOptions().extractBuiltinFunction and node.id in builtinfunctions.builtinFunctionMap :
			currentContext = self.getCurrentContext()
			if not currentContext.isNameSeen(node.id, [ context.NameType.store, context.NameType.argument ]) :
				node = self._constantManager.getNameReplacedNode(node.id) or node
		if self._canFindRenamedName(node) :
			node.id = self.getCurrentContext().findRenamedName(node.id) or node.id
		return node

	def _canFindRenamedName(self, node) :
		currentContext = self.getCurrentContext()
		if currentContext.isClass() and isinstance(node.ctx, ast.Store) :
			return False
		if self._needToKeepLocalVariables() :
			return False
		return True

	def visit_Nonlocal(self, node) :
		currentContext = self.getCurrentContext()
		for i in range(len(node.names)) :
			name = node.names[i]
			node.names[i] = currentContext.findRenamedName(name) or name
		return self._doGenericVisit(node)

	def visit_Import(self, node) :
		node = self._doRenameImport(node)
		return self._doGenericVisit(node)
	
	def visit_ImportFrom(self, node) :
		node = self._doRenameImport(node)
		return self._doGenericVisit(node)
	
	def visit_Call(self, node) :
		node = self._doGenericVisit(node)
		node = self._precomputeConstantFunctionCall(node) or node
		return node

	def visit_Constant(self, node) :
		if self._reentryGuard.isEntered(rewriterutil.guardId_constant) :
			return self._doGenericVisit(node)
		if not self._getOptions().removeDocString and rewriterutil.isConstantNodeMarkedDocString(node) :
			return self._doGenericVisit(node)
		with reentryguard.AutoReentryGuard(self._reentryGuard, rewriterutil.guardId_constant) :
			if self._getOptions().extractConstant :
				node = self._constantManager.getConstantReplacedNode(node.value) or node
			return node

	def visit_Match(self, node):
		with reentryguard.AutoReentryGuard(self._reentryGuard, rewriterutil.guardId_constant) :
			return self._doGenericVisit(node)

	def visit_JoinedStr(self, node) :
		# Don't obfuscate constants in f-string (JoinedStr), otherwise ast.unparse will give error
		with reentryguard.AutoReentryGuard(self._reentryGuard, rewriterutil.guardId_constant) :
			return self._doGenericVisit(node)

	def visit_Compare(self, node) :
		if self._reentryGuard.isEntered([ rewriterutil.guardId_compare, rewriterutil.guardId_boolOp ]) :
			node = self._doGenericVisit(node)
		else :
			with reentryguard.AutoReentryGuard(self._reentryGuard, rewriterutil.guardId_compare) :
				node = self._doInvertBoolOperator(node)
				node = self._doGenericVisit(node)
		if isinstance(node, ast.Compare) :
			node = self._precomputeConstantCompareExpression(node) or node
		return node

	def visit_BoolOp(self, node) :
		if self._reentryGuard.isEntered(rewriterutil.guardId_boolOp) :
			node = self._doGenericVisit(node)
		else :
			with reentryguard.AutoReentryGuard(self._reentryGuard, rewriterutil.guardId_boolOp) :
				node = self._doInvertBoolOperator(node)
				node = self._doGenericVisit(node)
		if isinstance(node, ast.BoolOp) :
			node = self._precomputeConstantExpression(node.op, node.values) or node
		return node
	
	def visit_UnaryOp(self, node) :
		node = self._doGenericVisit(node)
		if isinstance(node, ast.UnaryOp) :
			node = self._precomputeConstantExpression(node.op, [ node.operand ]) or node
		return node

	def visit_BinOp(self, node) :
		node = self._doGenericVisit(node)
		if isinstance(node, ast.BinOp) :
			node = self._precomputeConstantExpression(node.op, [ node.left, node.right ]) or node
		return node

	def visit_For(self, node):
		node.body = self._eliminateDeadCodeForNodeList(node.body)
		node.orelse = self._eliminateDeadCodeForNodeList(node.orelse)
		node = self._doMakeCodeBlock(node, allowOuterBlock = True)
		return self._doGenericVisit(node)

	def visit_While(self, node):
		node.body = self._eliminateDeadCodeForNodeList(node.body)
		node.orelse = self._eliminateDeadCodeForNodeList(node.orelse)
		node = self._doMakeCodeBlock(node, allowOuterBlock = True)
		return self._doGenericVisit(node)

	def visit_If(self, node) :
		node.body = self._eliminateDeadCodeForNodeList(node.body)
		node.orelse = self._eliminateDeadCodeForNodeList(node.orelse)
		node = self._ifRewriter.rewriteIf(node)
		if isinstance(node, ast.If) :
			node = self._eliminateDeadCodeForIfCondition(node)
		return node
	
	def visit_With(self, node) :
		node.body = self._eliminateDeadCodeForNodeList(node.body)
		return self._doGenericVisit(node)
	
	def visit_Try(self, node) :
		node = self._doRewriteTry(node)
		return self._doGenericVisit(node)

	def visit_TryStar(self, node) :
		node = self._doRewriteTry(node)
		return self._doGenericVisit(node)
	
	def _eliminateDeadCodeForNodeList(self, nodeList) :
		if not self._getOptions().eliminateDeadCode :
			return nodeList
		if nodeList is None :
			return None
		if not isinstance(nodeList, list) :
			return nodeList
		for i in range(len(nodeList)) :
			node = nodeList[i]
			if isinstance(node, (ast.Return, ast.Break, ast.Continue, ast.Raise)) :
				return nodeList[: i + 1]
		return nodeList

	def _eliminateDeadCodeForIfCondition(self, node) :
		if not self._getOptions().eliminateDeadCode :
			return node
		if not isinstance(node.test, ast.Constant) :
			return node
		if node.test.value :
			return node.body
		else :
			return node.orelse

	def _precomputeConstantFunctionCall(self, node) :
		if not self._getOptions().foldConstantExpression :
			return None
		if not isinstance(node.func, ast.Name) :
			return None
		funcName = node.func.id
		func = None
		funcNameMap = {
			'abs' : abs,
			'ascii' : ascii,
			'bin' : bin,
			'bool' : bool,
			'bytes' : bytes,
			'chr' : chr,
			'float' : float,
			'int' : int,
			'max' : max,
			'min' : min,
			'len' : len,
			'oct' : oct,
			'ord' : ord,
			'pow' : pow,
			'str' : str,
		}
		if funcName in funcNameMap :
			func = funcNameMap[funcName]
		if func is not None :
			args = []
			keywords = {}
			for arg in node.args :
				if not isinstance(arg, ast.Constant) :
					return None
				args.append(arg.value)
			for keyword in node.keywords :
				if not isinstance(keyword.value, ast.Constant) :
					return None
				keywords[keyword.arg] = keyword.value.value
			try :
				value = func(*args, **keywords)
				return astutil.makeConstant(value)
			except :
				pass
		return None

	def _precomputeConstantCompareExpression(self, node) :
		if not self._getOptions().foldConstantExpression :
			return None
		if not isinstance(node.left, ast.Constant) :
			return None
		for operand in node.comparators :
			if not isinstance(operand, ast.Constant) :
				return None

		compareMap = {
			ast.Eq : lambda left, right : left.value == right.value,
			ast.NotEq : lambda left, right : left.value != right.value,
			ast.Lt : lambda left, right : left.value < right.value,
			ast.LtE : lambda left, right : left.value <= right.value,
			ast.Gt : lambda left, right : left.value > right.value,
			ast.GtE : lambda left, right : left.value >= right.value,
			ast.Is : lambda left, right : left.value is right.value,
			ast.IsNot : lambda left, right : left.value is not right.value,
			ast.In : lambda left, right : left.value in right.value,
			ast.NotIn : lambda left, right : left.value not in right.value,
		}
		try :
			value = True
			left = node.left
			for i in range(len(node.comparators)) :
				op = node.ops[i]
				if op.__class__ not in compareMap :
					return None
				right = node.comparators[i]
				value = compareMap[op.__class__](left, right)
				if not value :
					break
				left = right
			return astutil.makeConstant(value)
		except :
			pass
		return None

	def _precomputeConstantExpression(self, operator, operandList) :
		if not self._getOptions().foldConstantExpression :
			return None
		for operand in operandList :
			if not isinstance(operand, ast.Constant) :
				return None

		def _precomputerAnd(operandList) :
			for operand in operandList :
				if not operand.value :
					return operand.value
			return operandList[-1].value
		def _precomputerOr(operandList) :
			for operand in operandList :
				if operand.value :
					return operand.value
			return operandList[-1].value
		precomputerMap = {
			# boolean
			ast.And : _precomputerAnd,
			ast.Or : _precomputerOr,
			# unary
			ast.Invert : lambda operands : ~operands[0].value,
			ast.Not : lambda operands : not operands[0].value,
			ast.UAdd : lambda operands : +operands[0].value,
			ast.USub : lambda operands : -operands[0].value,
			# binary, ignore ast.MatMult
			ast.Add : lambda operands : operands[0].value + operands[1].value,
			ast.Sub : lambda operands : operands[0].value - operands[1].value,
			ast.Mult : lambda operands : operands[0].value * operands[1].value,
			ast.Div : lambda operands : operands[0].value / operands[1].value,
			ast.Mod : lambda operands : operands[0].value % operands[1].value,
			ast.Pow : lambda operands : operands[0].value ** operands[1].value,
			ast.LShift : lambda operands : operands[0].value << operands[1].value,
			ast.RShift : lambda operands : operands[0].value >> operands[1].value,
			ast.BitOr : lambda operands : operands[0].value | operands[1].value,
			ast.BitXor : lambda operands : operands[0].value ^ operands[1].value,
			ast.BitAnd : lambda operands : operands[0].value & operands[1].value,
			ast.FloorDiv : lambda operands : operands[0].value // operands[1].value,
		}
		if operator.__class__ in precomputerMap :
			try :
				return astutil.makeConstant(precomputerMap[operator.__class__](operandList))
			except :
				pass
		return None

	def _doRewriteTry(self, node) :
		node.body = self._eliminateDeadCodeForNodeList(node.body)
		node.orelse = self._eliminateDeadCodeForNodeList(node.orelse)
		node.finalbody = self._eliminateDeadCodeForNodeList(node.finalbody)
		currentContext = self.getCurrentContext()
		for handler in node.handlers :
			if handler.name is not None :
				handler.name = currentContext.findRenamedName(handler.name) or handler.name
		return node

	def _doMakeCodeBlock(self, node, allowOuterBlock) :
		if not self._getOptions().addNopControlFlow :
			return node
		if not self._reentryGuard.isEntered(rewriterutil.guardId_makeCodeBlock) :
			with reentryguard.AutoReentryGuard(self._reentryGuard, rewriterutil.guardId_makeCodeBlock) :
				return self._codeBlockMaker.makeCodeBlock(node, allowOuterBlock)
		return node

	def _doInvertBoolOperator(self, node) :
		if not self._getOptions().invertBoolOperator :
			return node
		# Don't invert if it's not bool node, since the result value may be used for non-bool purpose. For example, x = 5 or 6
		if not astutil.isLogicalNode(node) :
			return node
		newNode = self.getNegationMaker().makeNegation(node)
		newNode = astutil.addNot(newNode)
		return newNode
	
	def _doRenameImport(self, node) :
		currentContext = self.getCurrentContext()
		for alias in node.names :
			if alias.asname is not None :
				alias.asname = currentContext.findRenamedName(alias.asname) or alias.asname
			elif alias.name is not None :
				currentContext.cancelRename(alias.name)
		return node

	def _prependNodes(self, body, nodeList, index = 0) :
		if nodeList is None :
			return
		if isinstance(nodeList, list) :
			for node in reversed(nodeList) :
				self._prependNodes(body, node, index)
		else :
			body.insert(index, nodeList)

	def _removeDocString(self, node) :
		if self._getOptions().removeDocString :
			node = astutil.removeDocString(node)
		return node
	
	def getNegationMaker(self) :
		if self._negationMaker is None :
			self._negationMaker = negationmaker.NegationMaker()
		self._negationMaker.setOptions(self._getOptions())
		return self._negationMaker
	
	def getTrueMaker(self) :
		return self._trueMaker

astVistorClassList = [ _AstVistorPreprocess, _AstVistorRewrite ]
specialOptionNames = [ 'preservedNames', 'stringEncoders' ]
class _IRewriter :
	def __init__(self, options, callback) :
		super().__init__()
		self._options = options
		self._callback = callback
		def x() :
			pass
		self._specialOptions = x
		for name in specialOptionNames :
			setattr(self._specialOptions, name, getattr(self._options, name))
			setattr(self._options, name, None)
		self._options._setReadonlyNames([ 'stringEncoders', 'preservedNames' ])
		self._doInitOptions()

	def _doInitOptions(self) :
		names = self._specialOptions.preservedNames
		if names is None :
			names = {}
		elif isinstance(names, (list, tuple)) :
			names = { n: 1 for n in names }
		elif isinstance(names, str) :
			names = { names: 1 }
		self._specialOptions.preservedNames = names

	def transform(self, documentManager) :
		for document in documentManager.getDocumentList() :
			fileName = document.getFileName()
			contextStack = context.ContextStack()
			rootNode = ast.parse(document.getContent(), fileName)
			options = _invokeCallback(self._callback, fileName, self._options, None) or self._options
			if not options.enabled :
				continue
			for visitorClass in astVistorClassList :
				visitor = visitorClass(
					contextStack = contextStack,
					options = options,
					specialOptions = self._specialOptions,
					fileName = fileName,
					callback = self._callback
				)
				visitor.visit(rootNode)
			document.setContent(astutil.astToSource(rootNode))

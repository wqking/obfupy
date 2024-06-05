import ast
import random
import copy

from . import util
from . import astutil
from . import reentryguard
from . import builtinfunctions
from .rewriter import constantmanager
from .rewriter import logicmaker
from .rewriter import nopmaker
from .rewriter import context
from .rewriter import codeblockmaker
from .rewriter import extranodemanager

guardId_compare = 1
guardId_boolOp = 2
guardId_constant = 3
guardId_makeCodeBlock = 4
guardId_extactFunction = 5

featureYield = "yield"

class _BaseAstVistor(ast.NodeTransformer) :
	def __init__(self, contextStack, options) :
		super().__init__()
		self._options = options
		self._contextStack = contextStack
		self._reentryGuard = reentryguard.ReentryGuard()

	def getCurrentContext(self) :
		return self._contextStack.getCurrentContext()

	def _doVisitNodeList(self, nodeList) :
		result = []
		for node in nodeList :
			if node is None :
				result.append(node)
				continue
			newNode = self.visit(node)
			if newNode is not None :
				result.append(newNode)
		return result

	def _doVisitArgumentDefaults(self, arguments) :
		arguments.kw_defaults = self._doVisitNodeList(arguments.kw_defaults)
		arguments.defaults = self._doVisitNodeList(arguments.defaults)
		return arguments

def getNodeContext(node) :
	assert hasattr(node, 'visitorContext')
	assert node.visitorContext is not None
	return node.visitorContext

def setNodeContext(node, context) :
	assert not hasattr(node, 'visitorContext')
	node.visitorContext = context

class _AstVistorFirst(_BaseAstVistor) :
	def __init__(self, contextStack, options) :
		super().__init__(contextStack, options)

	def visit_Module(self, node) :
		with context.ContextGuard(self._contextStack, context.ModuleContext()) as currentContext :
			setNodeContext(node, currentContext)
			return self.generic_visit(node)

	def visit_ClassDef(self, node):
		with context.ContextGuard(self._contextStack, context.ClassContext(node.name)) as currentContext :
			setNodeContext(node, currentContext)
			return self.generic_visit(node)

	def visit_AsyncFunctionDef(self, node):
		return self._doVisitFunctionDef(node)

	def visit_FunctionDef(self, node) :
		return self._doVisitFunctionDef(node)
		
	def _doVisitFunctionDef(self, node) :
		node.decorator_list = self._doVisitNodeList(node.decorator_list)
		with context.ContextGuard(self._contextStack, context.FunctionContext(node.name)) as currentContext :
			setNodeContext(node, currentContext)
			currentContext.seeName(node.name)
			self._doVisitArguments(node.args)
			node.body = self._doVisitNodeList(node.body)
			node.args = self._doVisitArgumentDefaults(node.args)
			return node
		
	def _doVisitArguments(self, arguments) :
		currentContext = self.getCurrentContext()
		def callback(argItem) :
			currentContext.addArgument(argItem.arg)
			currentContext.seeName(argItem.arg)
		astutil.enumerateArguments(arguments, callback)

	def visit_Lambda(self, node) :
		with context.ContextGuard(self._contextStack, context.FunctionContext('lambda')) as currentContext :
			setNodeContext(node, currentContext)
			self._doVisitArguments(node.args)
			return self.generic_visit(node)

	def visit_Name(self, node) :
		self.getCurrentContext().seeName(node.id)
		if self._canRenameNameNode(node) :
			self.getCurrentContext().renameSymbol(node.id)
		return node
	
	def visit_Attribute(self, node) :
		self.getCurrentContext().seeAttribute(node.attr)
		return self.generic_visit(node)

	def visit_Global(self, node) :
		for name in node.names :
			self.getCurrentContext().useGlobalName(name)
		return self.generic_visit(node)

	def visit_Nonlocal(self, node) :
		currentContext = self.getCurrentContext()
		for i in range(len(node.names)) :
			name = node.names[i]
			currentContext.useNonlocalName(name)
		return self.generic_visit(node)

	def visit_Yield(self, node) :
		currentContext = self.getCurrentContext()
		currentContext.seeFeature(featureYield)
		return self.generic_visit(node)

	def visit_YieldFrom(self, node) :
		currentContext = self.getCurrentContext()
		currentContext.seeFeature(featureYield)
		return self.generic_visit(node)

	def _canRenameNameNode(self, node) :
		currentContext = self.getCurrentContext()
		if not currentContext.isFunction() :
			return False
		if not isinstance(node.ctx, ast.Store) :
			return False
		if currentContext.isGlobalOrNonlocal(node.id) :
			return False
		if currentContext.isArgument(node.id) :
			return False
		return True
	
class _AstVistorSecond(_BaseAstVistor) :
	def __init__(self, contextStack, options) :
		super().__init__(contextStack, options)
		self._constantManager = constantmanager.ConstantManager(self._options['stringEncoders'])
		self._nopMaker = nopmaker.NopMaker()

	def visit_Module(self, node) :
		node = astutil.removeDocString(node)
		with context.ContextGuard(self._contextStack, getNodeContext(node)) :
			node = self.generic_visit(node)
			extraNodeManager = extranodemanager.ExtraNodeManager()
			self._constantManager.loadExtraNode(extraNodeManager)
			self._nopMaker.loadExtraNode(extraNodeManager)
			self._prependNodes(node.body, extraNodeManager.getNodeList(), self._findIndexNotImport(node.body))
			return node
	
	# This is to avoid SyntaxError: from __future__ imports must occur at the beginning of the file
	def _findIndexNotImport(self, nodeList) :
		index = 0
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
		context = getNodeContext(node)
		siblingList = context.getSiblingNodeList()
		if len(siblingList)  == 0 :
			return node
		return siblingList + [ node ]

	def visit_ClassDef(self, node):
		node = astutil.removeDocString(node)
		node.bases = self._doVisitNodeList(node.bases)
		node.keywords = self._doVisitNodeList(node.keywords)
		node.decorator_list = self._doVisitNodeList(node.decorator_list)
		with context.ContextGuard(self._contextStack, getNodeContext(node)) :
			node.body = self._doVisitNodeList(node.body)
			return self._makeResultNode(node)

	def visit_AsyncFunctionDef(self, node):
		node = self._doRewriteFunction(node)
		return self._makeResultNode(node)

	def visit_FunctionDef(self, node) :
		node = self._doRewriteFunction(node)
		return self._makeResultNode(node)
		
	def _doRewriteFunction(self, node) :
		node = astutil.removeDocString(node)
		# Visiting decorator_list must be outside of the function context
		node.decorator_list = self._doVisitNodeList(node.decorator_list)
		with context.ContextGuard(self._contextStack, getNodeContext(node)) as currentContext :
			newNode = self._doExtractFunction(node)
			if newNode is not None :
				return newNode
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
		currentContext = getNodeContext(node)
		# If the function contains any managed names, don't extract because the names are not accessible outside of the class
		for name in currentContext.getSeenNameSet() :
			if util.isNameMangling(name) :
				return False
		for name in currentContext.getSeenAttributeSet() :
			if util.isNameMangling(name) :
				return False
		if currentContext.isNameSeen('super') :
			return False
		if currentContext.isFeatureSeen(featureYield) :
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
		newContext = getNodeContext(node)
		setNodeContext(newFuncNode, newContext)

		def callback(argItem) :
			argItem.arg = newContext.renameSymbol(argItem.arg)
			argItem.annotation = None
		astutil.enumerateArguments(newFuncNode.args, callback)

		self._contextStack.saveAndReset()
		with context.ContextGuard(self._contextStack, newContext) :
			newFuncNode.body = self._doVisitNodeList(newFuncNode.body)
		self._contextStack.restore()

		newBody = ast.Return(
			value = self._doCreateForwardCall(node, newFuncNode.name, newContext)
		)
		node.body = [ newBody ]
		#node = self._convertFunctionToLambda(node) or node
		topScopedContext = self._contextStack.getTopScopedContext()
		topScopedContext.addSiblingNode(newFuncNode)
		return node
	
	def _doCreateForwardCall(self, node, newFuncName, newContext) :
		callArgs = []
		callKeywords = []
		argList = [ node.args.posonlyargs, node.args.args ]
		for itemList in argList :
			for argItem in itemList :
				if argItem is None :
					continue
				callArgs.append(ast.Name(id = argItem.arg, ctx = ast.Load()))
		if node.args.vararg :
			callArgs.append(ast.Starred(
				value = ast.Name(id = node.args.vararg.arg, ctx = ast.Load()),
				ctx = ast.Load()
			))
		for argItem in node.args.kwonlyargs :
			if argItem is None :
				continue
			callKeywords.append(
				ast.keyword(
					arg = newContext.findRenamedName(argItem.arg) or argItem.arg,
					value = ast.Name(id = argItem.arg, ctx = ast.Load())
				)
			)
		if node.args.kwarg :
			callKeywords.append(ast.keyword(value = ast.Name(id = node.args.kwarg.arg, ctx = ast.Load())))
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

	def visit_Lambda(self, node) :
		with context.ContextGuard(self._contextStack, getNodeContext(node)) :
			return self.generic_visit(node)

	def visit_Name(self, node) :
		if self._canFindRenamedName(node) :
			node.id = self.getCurrentContext().findRenamedName(node.id) or node.id
		return node

	def _canFindRenamedName(self, node) :
		currentContext = self.getCurrentContext()
		if currentContext.isClass() and isinstance(node.ctx, ast.Store) :
			return False
		return True

	def visit_Nonlocal(self, node) :
		currentContext = self.getCurrentContext()
		for i in range(len(node.names)) :
			name = node.names[i]
			node.names[i] = currentContext.findRenamedName(name) or name
		return self.generic_visit(node)

	def visit_Import(self, node) :
		node = self._doRenameImport(node)
		return self.generic_visit(node)
	
	def visit_ImportFrom(self, node) :
		node = self._doRenameImport(node)
		return self.generic_visit(node)
	
	def visit_Call(self, node) :
		if isinstance(node.func, ast.Name) and node.func.id in builtinfunctions.builtinFunctionMap :
			node.func = self._constantManager.getNameReplacedNode(node.func.id)
		return self.generic_visit(node)

	def visit_Constant(self, node) :
		if self._reentryGuard.isEntered(guardId_constant) :
			return self.generic_visit(node)
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_constant) :
			newNode = self._constantManager.getConstantReplacedNode(node.value)
			if newNode is not None :
				return newNode
			return node

	def visit_Match(self, node):
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_constant) :
			return self.generic_visit(node)

	def visit_JoinedStr(self, node) :
		# Don't obfuscate constants in f-string (JoinedStr), otherwise ast.unparse will give error
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_constant) :
			return self.generic_visit(node)

	def visit_Compare(self, node) :
		if self._reentryGuard.isEntered([ guardId_compare, guardId_boolOp ]) :
			return self.generic_visit(node)
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_compare) :
			node = self._doRewriteLogicalOperator(node)
			return self.generic_visit(node)

	def visit_BoolOp(self, node) :
		if self._reentryGuard.isEntered(guardId_boolOp) :
			return self.generic_visit(node)
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_boolOp) :
			node = self._doRewriteLogicalOperator(node)
			return self.generic_visit(node)

	def visit_For(self, node):
		node = self._doMakeCodeBlock(node, allowOuterBlock = True)
		return self.generic_visit(node)

	def visit_While(self, node):
		node = self._doMakeCodeBlock(node, allowOuterBlock = True)
		return self.generic_visit(node)

	def visit_If(self, node) :
		with reentryguard.AutoReentryGuard(self._reentryGuard, [ guardId_compare, guardId_boolOp ]) :
			node = self._doRewriteIf(node)
			return self.generic_visit(node)
	
	def visit_Try(self, node) :
		node = self._doRewriteTry(node)
		return self.generic_visit(node)

	def visit_TryStar(self, node) :
		node = self._doRewriteTry(node)
		return self.generic_visit(node)

	def _doRewriteTry(self, node) :
		currentContext = self.getCurrentContext()
		for handler in node.handlers :
			if handler.name is not None :
				handler.name = currentContext.findRenamedName(handler.name) or handler.name
		return node

	def _doRewriteIf(self, node) :
		if not astutil.isLogicalNode(node.test) :
			return node
		newTest = astutil.makeNegation(node.test)
		if newTest is not None :
			newTest = self._createLogicMaker().makeTrue(newTest)
			node.test = newTest
			node.body, node.orelse = node.orelse, node.body
			if len(node.body) == 0 :
				node.body.append(ast.Pass())
		return node

	def _doMakeCodeBlock(self, node, allowOuterBlock) :
		if not self._reentryGuard.isEntered(guardId_makeCodeBlock) :
			with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_makeCodeBlock) :
				return self._createCodeBlockMaker().makeCodeBlock(node, allowOuterBlock)
		return node

	def _doRewriteLogicalOperator(self, node) :
		if not astutil.isLogicalNode(node) :
			return node
		newNode = astutil.makeNegation(node)
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

	def _createLogicMaker(self) :
		return logicmaker.LogicMaker(self._nopMaker, constants = self._constantManager.getConstantValueList())

	def _createCodeBlockMaker(self) :
		return codeblockmaker.CodeBlockMaker(self._createLogicMaker())

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

astVistorClassList = [ _AstVistorFirst, _AstVistorSecond ]
class _IRewriter :
	def __init__(self, options) :
		super().__init__()
		self._options = options
		self._documentManager = None

	def _getDocumentList(self) :
		return self._documentManager.getDocumentList()

	def transform(self, documentManager) :
		self._documentManager = documentManager
		for document in self._getDocumentList() :
			contextStack = context.ContextStack()
			rootNode = ast.parse(document.getContent(), document.getFileName())
			for visitorClass in astVistorClassList :
				visitor = visitorClass(contextStack = contextStack, options = self._options)
				visitor.visit(rootNode)
			document.setContent(astutil.astToSource(rootNode))

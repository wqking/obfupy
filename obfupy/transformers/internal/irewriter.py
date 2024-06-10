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
from .rewriter import functionvistormixin
from .rewriter import rewriterutil
from .. import rewriter

guardId_compare = 1
guardId_boolOp = 2
guardId_constant = 3
guardId_makeCodeBlock = 4
guardId_extactFunction = 5

class _BaseAstVistor(ast.NodeTransformer) :
	def __init__(self, contextStack, options) :
		super().__init__()
		self._options = options
		self._contextStack = contextStack
		self._reentryGuard = reentryguard.ReentryGuard()

	def getCurrentContext(self) :
		return self._contextStack.getCurrentContext()
	
	def _getOption(self, name) :
		return self._options[name]

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

class _AstVistorPreprocess(_BaseAstVistor) :
	def __init__(self, contextStack, options) :
		super().__init__(contextStack, options)

	def visit_Module(self, node) :
		with context.ContextGuard(self._contextStack, context.ModuleContext()) as currentContext :
			rewriterutil.setNodeContext(node, currentContext)
			return self.generic_visit(node)

	def visit_ClassDef(self, node):
		with context.ContextGuard(self._contextStack, context.ClassContext(node.name)) as currentContext :
			rewriterutil.setNodeContext(node, currentContext)
			return self.generic_visit(node)

	def visit_AsyncFunctionDef(self, node):
		return self._doVisitFunctionDef(node)

	def visit_FunctionDef(self, node) :
		return self._doVisitFunctionDef(node)
		
	def _doVisitFunctionDef(self, node) :
		node.decorator_list = self._doVisitNodeList(node.decorator_list)
		with context.ContextGuard(self._contextStack, context.FunctionContext(node.name)) as currentContext :
			rewriterutil.setNodeContext(node, currentContext)
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
			rewriterutil.setNodeContext(node, currentContext)
			self._doVisitArguments(node.args)
			return self.generic_visit(node)

	def visit_Name(self, node) :
		self.getCurrentContext().seeName(node.id)
		if self._getOption(rewriter.OptionNames.renameLocalVariable) and self._canRenameNameNode(node) :
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
		currentContext.seeFeature(rewriterutil.featureYield)
		return self.generic_visit(node)

	def visit_YieldFrom(self, node) :
		currentContext = self.getCurrentContext()
		currentContext.seeFeature(rewriterutil.featureYield)
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

class _AstVistorRewrite(_BaseAstVistor, functionvistormixin.FunctionVistorMixin) :
	def __init__(self, contextStack, options) :
		super().__init__(contextStack, options)
		self._constantManager = constantmanager.ConstantManager(self._options['stringEncoders'])
		self._nopMaker = nopmaker.NopMaker()
		self._trueMaker = truemaker.TrueMaker(self._nopMaker, constants = self._constantManager.getConstantValueList())
		self._codeBlockMaker = codeblockmaker.CodeBlockMaker(self._trueMaker)

	def visit_Module(self, node) :
		node = astutil.removeDocString(node)
		with context.ContextGuard(self._contextStack, rewriterutil.getNodeContext(node)) :
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
		context = rewriterutil.getNodeContext(node)
		siblingList = context.getSiblingNodeList()
		if len(siblingList)  == 0 :
			return node
		return siblingList + [ node ]

	def visit_ClassDef(self, node):
		node = astutil.removeDocString(node)
		node.bases = self._doVisitNodeList(node.bases)
		node.keywords = self._doVisitNodeList(node.keywords)
		node.decorator_list = self._doVisitNodeList(node.decorator_list)
		with context.ContextGuard(self._contextStack, rewriterutil.getNodeContext(node)) :
			node.body = self._doVisitNodeList(node.body)
			return self._makeResultNode(node)

	def visit_AsyncFunctionDef(self, node):
		node = self._doVisitFunction(node)
		return self._makeResultNode(node)

	def visit_FunctionDef(self, node) :
		node = self._doVisitFunction(node)
		return self._makeResultNode(node)
		
	def visit_Lambda(self, node) :
		with context.ContextGuard(self._contextStack, rewriterutil.getNodeContext(node)) :
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
			if self._getOption(rewriter.OptionNames.extractBuiltinFunction) :
				node.func = self._constantManager.getNameReplacedNode(node.func.id) or node.func
		return self.generic_visit(node)

	def visit_Constant(self, node) :
		if self._reentryGuard.isEntered(guardId_constant) :
			return self.generic_visit(node)
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_constant) :
			if self._getOption(rewriter.OptionNames.extractConstant) :
				node = self._constantManager.getConstantReplacedNode(node.value) or node
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
			node = self._doReverseIfElse(node)
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

	def _doReverseIfElse(self, node) :
		if not self._getOption(rewriter.OptionNames.reverseIfElse) :
			return node
		if not astutil.isLogicalNode(node.test) :
			return node
		newTest = astutil.makeNegation(node.test)
		if newTest is not None :
			newTest = self._trueMaker.makeTrue(newTest)
			node.test = newTest
			node.body, node.orelse = node.orelse, node.body
			if len(node.body) == 0 :
				node.body.append(ast.Pass())
		return node

	def _doMakeCodeBlock(self, node, allowOuterBlock) :
		if not self._getOption(rewriter.OptionNames.addNopControlFlow) :
			return node
		if not self._reentryGuard.isEntered(guardId_makeCodeBlock) :
			with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_makeCodeBlock) :
				return self._codeBlockMaker.makeCodeBlock(node, allowOuterBlock)
		return node

	def _doRewriteLogicalOperator(self, node) :
		if not self._getOption(rewriter.OptionNames.rewriteConditionalExpression) :
			return node
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

astVistorClassList = [ _AstVistorPreprocess, _AstVistorRewrite ]
class _IRewriter :
	def __init__(self, options) :
		super().__init__()
		self._options = options

	def transform(self, documentManager) :
		for document in documentManager.getDocumentList() :
			contextStack = context.ContextStack()
			rootNode = ast.parse(document.getContent(), document.getFileName())
			for visitorClass in astVistorClassList :
				visitor = visitorClass(contextStack = contextStack, options = self._options)
				visitor.visit(rootNode)
			document.setContent(astutil.astToSource(rootNode))

import ast
import enum

from . import util
from . import astutil
from .rewriter import constantmanager
from . import reentryguard

@enum.unique
class _ScopeType(enum.IntEnum) :
	globalScope = 1
	functionScope = 2
	classScope = 3

@enum.unique
class _AstVistorPhase(enum.IntEnum) :
	first = 1
	second = 2

class _Scope :
	def __init__(self, type) :
		self._type = type
		self._nameReplaceMap = {}
		self._usedNameSet = {}

	def isGlobal(self) :
		return self._type == _ScopeType.globalScope

	def isFunction(self) :
		return self._type == _ScopeType.functionScope

	def isClass(self) :
		return self._type == _ScopeType.classScope

	def getNewName(self, name) :
		if name not in self._nameReplaceMap :
			self._nameReplaceMap[name] = util.getUnusedRandomSymbol(self._usedNameSet)
		return self._nameReplaceMap[name]
	
	def findNewName(self, name) :
		if name in self._nameReplaceMap :
			return self._nameReplaceMap[name]
		return None
	
class _ScopeStack :
	def __init__(self, globalScope) :
		self._localScopeStack = [ globalScope ]

	def getCurrentScope(self) :
		assert len(self._localScopeStack) > 0
		return self._localScopeStack[-1]
	
	def pushScope(self, type) :
		scope = _Scope(type)
		self._localScopeStack.append(scope)
		return scope
	
	def popScope(self) :
		assert len(self._localScopeStack) > 1
		self._localScopeStack.pop()

	def findNewName(self, name, returnNameIfNotFound = True) :
		newName = None
		for i in range(len(self._localScopeStack) - 1, -1, -1) :
			newName = self._localScopeStack[i].findNewName(name)
			if newName is not None :
				break
		if returnNameIfNotFound and newName is None :
			return name
		return newName
	
class ProjectContext :
	def __init__(self) :
		self._keptNameMap = {}

	def addKeptName(self, name, scopeName = '') :
		if scopeName not in self._keptNameMap :
			self._keptNameMap[scopeName] = {}
		self._keptNameMap[scopeName][name] = True

	def shouldKeepName(self, name, scopeName = '') :
		if scopeName not in self._keptNameMap :
			return False
		return name in self._keptNameMap[scopeName]
	
guardId_compare = 1
guardId_boolOp = 2
guardId_constant = 3

class _AstVistor(ast.NodeTransformer) :
	def __init__(self, options, globalScope, projectContext) :
		super().__init__()
		self._options = options
		self._scopeStack = _ScopeStack(globalScope)
		self._projectContext = projectContext
		self._constantManager = constantmanager.ConstantManager(self._options)
		self.reset(_AstVistorPhase.first)

	def reset(self, phase) :
		self._phase = phase
		self._reentryGuard = reentryguard.ReentryGuard()

	def isPreprocessPhase(self) :
		return self._phase == _AstVistorPhase.first

	def isRewritePhase(self) :
		return self._phase == _AstVistorPhase.second

	def visit_Module(self, node) :
		self.doRemoveDocString(node)
		node = self.generic_visit(node)
		if self.isRewritePhase() :
			for newNode in reversed(self._constantManager.makeDefineNodes()) :
				node.body.insert(0, newNode)
		return node

	def visit_ClassDef(self, node):
		self.doRemoveDocString(node)
		return self.generic_visit(node)

	def visit_AsyncFunctionDef(self, node):
		self.doRemoveDocString(node)
		return self.generic_visit(node)

	def visit_FunctionDef(self, node) :
		self.doRemoveDocString(node)
		scope = self._scopeStack.pushScope(_ScopeType.functionScope)
		if self.isRewritePhase() :
			funcName = node.name
			for arg in node.args.args :
				if not self._projectContext.shouldKeepName(arg.arg, funcName) :
					arg.arg = scope.getNewName(arg.arg)
		node.body = self.doVisitNodeList(node.body)
		self._scopeStack.popScope()
		return node
	
	def visit_Name(self, node) :
		if self.isRewritePhase() :
			node.id = self._scopeStack.findNewName(node.id)
		return node
	
	def visit_Call(self, node) :
		if self.isPreprocessPhase() :
			self.doParseCallKeywordArguments(node)
		return self.generic_visit(node)

	def visit_Compare(self, node) :
		if self._reentryGuard.isEntered([ guardId_compare, guardId_boolOp ]) :
			return self.generic_visit(node)
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_compare) :
			node = self.doRewriteLogicalOperator(node)
			return self.generic_visit(node)

	def visit_BoolOp(self, node) :
		if self._reentryGuard.isEntered(guardId_boolOp) :
			return self.generic_visit(node)
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_boolOp) :
			node = self.doRewriteLogicalOperator(node)
			return self.generic_visit(node)

	def visit_If(self, node) :
		with reentryguard.AutoReentryGuard(self._reentryGuard, [ guardId_compare, guardId_boolOp ]) :
			return self.doRewriteIf(node)

	def visit_Constant(self, node) :
		if self._reentryGuard.isEntered(guardId_constant) :
			return self.generic_visit(node)
		return self.doRewriteConstant(node)

	def visit_JoinedStr(self, node) :
		# Don't obfuscate constants in f-string (JoinedStr), otherwise ast.unparse will give error
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_constant) :
			return self.generic_visit(node)

	def doVisitNodeList(self, nodeList) :
		result = []
		for node in nodeList :
			newNode = self.visit(node)
			if newNode is not None :
				result.append(newNode)
		return result

	def doRewriteIf(self, node) :
		if not self.isRewritePhase() :
			return node
		newTest = astutil.makeNegation(node.test)
		if newTest is not None :
			node.test = newTest
			node.body, node.orelse = node.orelse, node.body
			if len(node.body) == 0 :
				node.body.append(ast.Pass())
		return self.generic_visit(node)

	def doRewriteConstant(self, node) :
		if self.isPreprocessPhase() :
			self._constantManager.foundConstant(node.value)
		elif self.isRewritePhase() :
			newNode = self._constantManager.getReplacedNode(node.value)
			if newNode is not None :
				return newNode
		return node

	def doRewriteLogicalOperator(self, node) :
		if not self.isRewritePhase() :
			return node
		newNode = astutil.makeNegation(node)
		newNode = astutil.addNot(newNode)
		return newNode
	
	def doRemoveDocString(self, node) :
		if not self.isRewritePhase() :
			return
		# See get_raw_docstring in Python built-in ast.py
		if len(node.body) == 0 :
			return
		if not isinstance(node.body[0], ast.Expr) :
			return
		if not isinstance(node, ast.Constant) or not isinstance(node.value, str) :
			return
		node.body = node.body[1 : ]
		if len(node.body) == 0 :
			node.body.append(ast.Pass())

	def doParseCallKeywordArguments(self, node) :
		funcName = None
		if isinstance(node.func, ast.Name) :
			funcName = node.func.id
		elif isinstance(node.func, ast.Attribute) :
			funcName = node.func.attr
		if funcName is None :
			return
		if node.keywords is None or len(node.keywords) == 0 :
			return
		for keyword in node.keywords :
			self._projectContext.addKeptName(keyword.arg, funcName)
	
class _IRewriter :
	def __init__(self, options) :
		super().__init__()
		self._options = options
		self._documentManager = None
		self._globalScope = _Scope(_ScopeType.globalScope)
		self._projectContext = ProjectContext()

	def getDocumentList(self) :
		return self._documentManager.getDocumentList()

	def transform(self, documentManager) :
		self._documentManager = documentManager
		astMap = {}
		visitorMap = {}
		for document in self.getDocumentList() :
			rootNode = ast.parse(document.getContent(), document.getFileName())
			astMap[document.getUid()] = rootNode
			visitor = _AstVistor(
				options = self._options,
				globalScope = self._globalScope,
				projectContext = self._projectContext
			)
			visitorMap[document.getUid()] = visitor
			visitor.visit(rootNode)
		for document in self.getDocumentList() :
			rootNode = astMap[document.getUid()]
			visitor = visitorMap[document.getUid()]
			visitor.reset(_AstVistorPhase.second)
			visitor.visit(rootNode)
			document.setContent(ast.unparse(ast.fix_missing_locations(rootNode)))

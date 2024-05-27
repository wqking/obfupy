import ast
import enum
import re

from . import util
from . import astutil
from . import reentryguard
from .rewriter import constantmanager
from .rewriter import logicmaker
from .rewriter import nopmaker

@enum.unique
class ScopeType(enum.IntEnum) :
	globalScope = 1
	functionScope = 2
	classScope = 3

astMaxPhaseCount = 2

class Scope :
	def __init__(self, type, name = None) :
		self._type = type
		self._name = name
		self._nameReplaceMap = {}
		self._usedNameSet = {}

	def isGlobal(self) :
		return self._type == ScopeType.globalScope

	def isFunction(self) :
		return self._type == ScopeType.functionScope

	def isClass(self) :
		return self._type == ScopeType.classScope
	
	def getScopeName(self) :
		return self._name

	def getNewName(self, name) :
		if name not in self._nameReplaceMap :
			self._nameReplaceMap[name] = util.getUnusedRandomSymbol(self._usedNameSet)
		return self._nameReplaceMap[name]
	
	def findNewName(self, name) :
		if name in self._nameReplaceMap :
			return self._nameReplaceMap[name]
		return None
	
class ScopeStack :
	def __init__(self, globalScope) :
		self._localScopeStack = [ globalScope ]

	def getCurrentScope(self) :
		assert len(self._localScopeStack) > 0
		return self._localScopeStack[-1]
	
	def pushScope(self, type, name) :
		scope = Scope(type, name)
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
	
	def getEnclosedClassScope(self) :
		for i in range(len(self._localScopeStack) - 1, -1, -1) :
			if self._localScopeStack[i].isClass() :
				return self._localScopeStack[i]
		return None
	
class ProjectContext :
	def __init__(self) :
		self._keptNameMap = {}
		self._noneScopeKeptNameMap = {}

	def addKeptName(self, name, scopeName = '') :
		if scopeName is None :
			self._noneScopeKeptNameMap[name] = True
		else :
			if scopeName not in self._keptNameMap :
				self._keptNameMap[scopeName] = {}
			self._keptNameMap[scopeName][name] = True

	def shouldKeepName(self, name, scopeName = '') :
		if name in self._noneScopeKeptNameMap :
			return True
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
		self._renameArgument = self._options['renameArgument']
		self._scopeStack = ScopeStack(globalScope)
		self._projectContext = projectContext
		self._constantManager = constantmanager.ConstantManager(self._options)
		self._nopMaker = nopmaker.NopMaker()
		self._logicMaker = logicmaker.LogicMaker(self._nopMaker)
		self.reset(0)

	def reset(self, phase) :
		self._phase = phase
		self._reentryGuard = reentryguard.ReentryGuard()

	def isPreprocessPhase(self) :
		return self._phase == 0

	def isRewritePhase(self) :
		return self._phase == 1

	def prependNodes(self, body, nodeList) :
		if nodeList is None :
			return
		if isinstance(nodeList, list) :
			for node in reversed(nodeList) :
				self.prependNodes(body, node)
		else :
			body.insert(0, nodeList)

	def visit_Module(self, node) :
		self.doRemoveDocString(node)
		node = self.generic_visit(node)
		if self.isRewritePhase() :
			self.prependNodes(node.body, self._nopMaker.getDefineNodes())
			self.prependNodes(node.body, self._constantManager.getDefineNodes())
		return node

	def visit_ClassDef(self, node):
		scope = self._scopeStack.pushScope(ScopeType.classScope, node.name)
		self.doRemoveDocString(node)
		node = self.generic_visit(node)
		self._scopeStack.popScope()
		return node

	def visit_AsyncFunctionDef(self, node):
		self.doRemoveDocString(node)
		return self.generic_visit(node)

	def visit_FunctionDef(self, node) :
		self.doRemoveDocString(node)
		scope = self._scopeStack.pushScope(ScopeType.functionScope, node.name)
		if self.isRewritePhase() and self._renameArgument :
			funcName = node.name
			# Don't rename arguments in __init__, __call__, etc
			if re.match(r'__\w+__', funcName) is None :
				for arg in node.args.args :
					if not self._projectContext.shouldKeepName(arg.arg, funcName) :
						arg.arg = scope.getNewName(arg.arg)
		node.body = self.doVisitNodeList(node.body)
		node.decorator_list = self.doVisitNodeList(node.decorator_list)
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
			return self.generic_visit(node)
		if not astutil.isLogicalNode(node.test) :
			return self.generic_visit(node)
		newTest = astutil.makeNegation(node.test)
		if newTest is not None :
			newTest = self._logicMaker.makeTrue(newTest)
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
		if not astutil.isLogicalNode(node) :
			return node
		newNode = astutil.makeNegation(node)
		newNode = astutil.addNot(newNode)
		return newNode
	
	def doRemoveDocString(self, node) :
		# Do it in preprocess phase otherwise it will be taken out as constant
		if not self.isPreprocessPhase() :
			return
		# See get_raw_docstring in Python built-in ast.py
		if len(node.body) == 0 :
			return
		child = node.body[0]
		if not isinstance(child, ast.Expr) :
			return
		child = child.value
		if not isinstance(child, ast.Constant) or not isinstance(child.value, str) :
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
			self._projectContext.addKeptName(keyword.arg, None)
	
class _IRewriter :
	def __init__(self, options) :
		super().__init__()
		self._options = options
		self._documentManager = None
		self._globalScope = Scope(ScopeType.globalScope)
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

		for document in self.getDocumentList() :
			rootNode = astMap[document.getUid()]
			visitor = visitorMap[document.getUid()]
			for i in range(astMaxPhaseCount) :
				visitor.reset(i)
				visitor.visit(rootNode)
				if i == astMaxPhaseCount - 1 :
					document.setContent(ast.unparse(ast.fix_missing_locations(rootNode)))

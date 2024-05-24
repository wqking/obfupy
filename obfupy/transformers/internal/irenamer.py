import ast
import enum

from . import util

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
			self._nameReplaceMap[name] = util.getUniqueRandomSymbol(self._usedNameSet)
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

class _AstVistor(ast.NodeTransformer) :
	def __init__(self, scopeStack, projectContext, phase) :
		super().__init__()
		self._scopeStack = scopeStack
		self._projectContext = projectContext
		self._phase = phase

	def visit_ClassDef(self, node):
		self.doRemoveDocString(node)
		return self.generic_visit(node)

	def visit_AsyncFunctionDef(self, node):
		self.doRemoveDocString(node)
		return self.generic_visit(node)

	def visit_Module(self, node):
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
		node.body = [ self.visit(n) for n in node.body ]
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
	
	def doRemoveDocString(self, node) :
		if not self.isRewritePhase() :
			return
		# https://gist.github.com/phpdude/1ae6f19de213d66286c8183e9e3b9ec1
		if len(node.body) == 0 :
			return
		if not isinstance(node.body[0], ast.Expr) :
			return
		if not hasattr(node.body[0], 'value') or not isinstance(node.body[0].value, ast.Str) :
			return
		node.body = node.body[1 : ]
		#add "pass" statement here
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
	
	def isPreprocessPhase(self) :
		return self._phase == _AstVistorPhase.first

	def isRewritePhase(self) :
		return self._phase == _AstVistorPhase.second

class _IRenamer :
	def __init__(self) :
		super().__init__()
		self._documentManager = None
		self._globalScope = _Scope(_ScopeType.globalScope)
		self._projectContext = ProjectContext()

	def getDocumentList(self) :
		return self._documentManager.getDocumentList()

	def transform(self, documentManager) :
		self._documentManager = documentManager
		astMap = {}
		for document in self.getDocumentList() :
			rootNode = ast.parse(document.getContent(), document.getFileName())
			astMap[document.getUid()] = rootNode
			visitor = _AstVistor(
				scopeStack = _ScopeStack(self._globalScope),
				projectContext = self._projectContext, 
				phase = _AstVistorPhase.first
			)
			visitor.visit(rootNode)
		for document in self.getDocumentList() :
			rootNode = astMap[document.getUid()]
			visitor = _AstVistor(
				scopeStack = _ScopeStack(self._globalScope),
				projectContext = self._projectContext, 
				phase = _AstVistorPhase.second
			)
			visitor.visit(rootNode)
			document.setContent(ast.unparse(rootNode))

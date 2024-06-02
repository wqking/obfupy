from .. import util

import enum

@enum.unique
class ContextType(enum.IntEnum) :
	functionContext = 1
	classContext = 2
	moduleContext = 3

class BaseContext :
	def __init__(self) :
		self._seenNameSet = {}
		self._seenAttributeSet = {}

	def seeName(self, name) :
		self._seenNameSet[name] = True

	def isNameSeen(self, name) :
		return name in self._seenNameSet
	
	def getSeenNameSet(self) :
		return self._seenNameSet
	
	def seeAttribute(self, attribute) :
		self._seenAttributeSet[attribute] = True

	def isAttributeSeen(self, attribute) :
		return attribute in self._seenAttributeSet
	
	def getSeenAttributeSet(self) :
		return self._seenAttributeSet

class PersistentContext(BaseContext) :
	def __init__(self):
		super().__init__()

class _RenameMixin :
	def renameSymbol(self, name) :
		if name not in self._renameMap :
			self._renameMap[name] = util.getUnusedRandomSymbol(self._usedNewNameSet, originalName = name)
		return self._renameMap[name]

	def findRenamedName(self, name) :
		if name in self._renameMap :
			return self._renameMap[name]
		return None
	
	def findRenamedNameInChain(self, name) :
		if name in self._renameMap :
			return self._renameMap[name]
		if self._parent is not None :
			return self._parent.findRenamedNameInChain(name)
		return None

	def isRenamed(self, name) :
		return name in self._renameMap
	
class Context(BaseContext, _RenameMixin) :
	def __init__(self, type, contextName) :
		super().__init__()

		self._type = type
		self._contextName = contextName
		self._parent = None
		self._owner = None
		self._persistentContext = None
		self._globalNonlocalSet = {}
		self._siblingNodeList = []

		# _RenameMixin
		self._renameMap = {}
		self._usedNewNameSet = {}

	def initialize(self, parent, owner) :
		self._parent = parent
		self._owner = owner

	def getContextName(self) :
		return self._contextName

	def isModule(self) :
		return self._type == ContextType.moduleContext

	def isClass(self) :
		return self._type == ContextType.classContext

	def isFunction(self) :
		return self._type == ContextType.functionContext

	def getPersistentContext(self) :
		if self._persistentContext is None :
			self._persistentContext = self._owner._doGetPersistentContext(self.getQualifiedName())
		return self._persistentContext
	
	def getQualifiedName(self) :
		nameList = []
		currentContext = self
		while currentContext is not None :
			nameList.insert(0, currentContext.getContextName())
			currentContext = currentContext._parent
		return ".".join(nameList)
	
	def getParentContext(self) :
		return self._parent

	def useGlobalName(self, name) :
		self._globalNonlocalSet[name] = True

	def useNonlocalName(self, name) :
		self._globalNonlocalSet[name] = True

	def isGlobalOrNonlocal(self, name) :
		return name in self._globalNonlocalSet

	def addSiblingNode(self, node) :
		self._siblingNodeList.append(node)

	def getSiblingNodeList(self) :
		return self._siblingNodeList
	
class ModuleContext(Context) :
	def __init__(self) :
		super().__init__(ContextType.moduleContext, "module")

class FunctionContext(Context) :
	def __init__(self, funcName) :
		super().__init__(ContextType.functionContext, funcName)
		self._argumentNameSet = {}

	def addArgument(self, name) :
		self._argumentNameSet[name] = True

	def isArgument(self, name) :
		return name in self._argumentNameSet
	
class ClassContext(Context) :
	def __init__(self, className) :
		super().__init__(ContextType.classContext, className)

class ContextStack :
	def __init__(self) :
		self._contextList = []
		self._persistentContextMap = {}

	def getCurrentContext(self) :
		assert len(self._contextList) > 0
		return self._contextList[-1]
	
	def getModuleContext(self) :
		assert len(self._contextList) > 0
		return self._contextList[0]
	
	def getTopScopedContext(self) :
		if len(self._contextList) > 1 :
			return self._contextList[1]
		return None
	
	def pushContext(self, context) :
		parent = None
		if len(self._contextList) > 0 :
			parent = self._contextList[-1]
		context.initialize(parent, self)
		self._contextList.append(context)
		return context
	
	def popContext(self) :
		assert len(self._contextList) > 0
		self._contextList[-1].initialize(None, None)
		self._contextList.pop()

	def isWithinFunction(self) :
		return self.getCurrentContext().isFunction()

	def _doGetPersistentContext(self, qualifiedName) :
		if qualifiedName not in self._persistentContextMap :
			self._persistentContextMap[qualifiedName] = PersistentContext()
		return self._persistentContextMap[qualifiedName]

class ContextGuard :
	def __init__(self, contextStack, context) :
		self._contextStack = contextStack
		self._context = context

	def __enter__(self) :
		return self._contextStack.pushContext(self._context)

	def __exit__(self, type, value, traceBack) :
		self._contextStack.popContext()


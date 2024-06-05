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
		self._seenFeatureSet = {}

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
	
	def seeFeature(self, feature) :
		self._seenFeatureSet[feature] = True

	def isFeatureSeen(self, feature) :
		return feature in self._seenFeatureSet

class _RenameMixin :
	def findRenamedName(self, name) :
		return self._doFindRenamedName(name)

	def _doFindRenamedName(self, name) :
		if name in self._renameMap :
			return self._renameMap[name]
		return None

	def renameSymbol(self, name, newName = None) :
		if name not in self._renameMap :
			if newName is None :
				newName = self.createNewName(name)
			self._renameMap[name] = newName
		return self._renameMap[name]
	
	def createNewName(self, name = None) :
		return util.getUnusedRandomSymbol(self._usedNewNameSet, originalName = name)

	def cancelRename(self, name) :
		if name in self._renameMap :
			del self._renameMap[name]

	def isRenamed(self, name) :
		return name in self._renameMap
	
class Context(BaseContext, _RenameMixin) :
	def __init__(self, type, contextName) :
		super().__init__()

		self._type = type
		self._contextName = contextName
		self._parent = None
		self._owner = None
		self._globalNonlocalSet = {}
		self._siblingNodeList = []

		# _RenameMixin
		self._renameMap = {}
		self._usedNewNameSet = {}

	def reset(self, parent = None, owner = None) :
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

	def findRenamedName(self, name) :
		newName = self._doFindRenamedName(name)
		if newName is not None :
			return newName
		if self.isArgument(name) :
			return None
		parent = self._parent
		while parent is not None :
			if parent.isFunction() or parent.isModule() :
				return parent.findRenamedName(name)
			parent = parent._parent
		return None

class ClassContext(Context) :
	def __init__(self, className) :
		super().__init__(ContextType.classContext, className)

	def findRenamedName(self, name) :
		newName = self._doFindRenamedName(name)
		if newName is not None :
			return newName
		parent = self._parent
		while parent is not None :
			if parent.isFunction() or parent.isModule() :
				return parent.findRenamedName(name)
			parent = parent._parent
		return None

class ContextStack :
	def __init__(self) :
		self._contextList = []
		self._savedContextList = []

	def saveAndReset(self) :
		assert len(self._contextList) > 0
		moduleContext = self._contextList[0]
		self._savedContextList.append(self._contextList)
		self._contextList = [ moduleContext ]
	
	def restore(self) :
		assert len(self._savedContextList) > 0
		self._contextList = self._savedContextList[-1]
		self._savedContextList.pop()

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
		context.reset(parent, self)
		self._contextList.append(context)
		return context

	def popContext(self) :
		assert len(self._contextList) > 0
		self._contextList.pop()

class ContextGuard :
	def __init__(self, contextStack, context) :
		self._contextStack = contextStack
		self._context = context

	def __enter__(self) :
		return self._contextStack.pushContext(self._context)

	def __exit__(self, type, value, traceBack) :
		self._contextStack.popContext()


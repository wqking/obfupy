from .. import util

import enum

@enum.unique
class ContextType(enum.IntEnum) :
	functionContext = 1
	globalContext = 2

class Context :
	def __init__(self, type) :
		self._type = type
		self._nameReplaceMap = {}
		self._usedNewNameSet = {}
		self._disabledNameSet = {}
		self._globalNonlocalSet = {}
		self._seenNameSet = {}
		self._argumentNameSet = {}

	def isGlobal(self) :
		return self._type == ContextType.globalContext

	def isFunction(self) :
		return self._type == ContextType.functionContext

	def getNewName(self, name) :
		if name not in self._nameReplaceMap :
			self._nameReplaceMap[name] = util.getUnusedRandomSymbol(self._usedNewNameSet)
		return self._nameReplaceMap[name]

	def findNewName(self, name, returnOriginIfNotFound = True) :
		if name in self._nameReplaceMap and not self.isNameDisabled(name) :
			return self._nameReplaceMap[name]
		if returnOriginIfNotFound :
			return name
		return None

	def isRenamed(self, name) :
		return name in self._nameReplaceMap
	
	def addGlobalName(self, name) :
		self._globalNonlocalSet[name] = True

	def addNonlocal(self, name) :
		self._globalNonlocalSet[name] = True

	def isGlobalOrNonlocal(self, name) :
		return name in self._globalNonlocalSet
	
	def seeName(self, name) :
		self._seenNameSet[name] = True

	def isNameSeen(self, name) :
		return name in self._seenNameSet
	
	def addArgument(self, name) :
		self._argumentNameSet[name] = True
	
	def isArgument(self, name) :
		return name in self._argumentNameSet
	
	def disableName(self, name) :
		if name not in self._disabledNameSet :
			self._disabledNameSet[name] = 0
		self._disabledNameSet[name] += 1
	
	def enableName(self, name) :
		if name in self._disabledNameSet :
			self._disabledNameSet[name] -= 1
			if self._disabledNameSet[name] < 0 :
				self._disabledNameSet[name] = 0
	
	def isNameDisabled(self, name) :
		return name in self._disabledNameSet and self._disabledNameSet[name] > 0
	
class GlobalContext(Context) :
	def __init__(self) :
		super().__init__(ContextType.globalContext)

class FunctionContext(Context) :
	def __init__(self) :
		super().__init__(ContextType.functionContext)

class ContextStack :
	def __init__(self) :
		self._contextList = []

	def getCurrentContext(self) :
		assert len(self._contextList) > 0
		return self._contextList[-1]
	
	def pushContext(self, context) :
		self._contextList.append(context)
		return context
	
	def popContext(self) :
		assert len(self._contextList) > 0
		self._contextList.pop()

	def isWithinFunction(self) :
		return self.getCurrentContext().isFunction()

	def findNewName(self, name, returnOriginIfNotFound = True) :
		for i in range(len(self._contextList) - 1, -1, -1) :
			newName = self._contextList[i].findNewName(name, False)
			if newName is not None :
				return newName
		if returnOriginIfNotFound :
			return name
		return None
			
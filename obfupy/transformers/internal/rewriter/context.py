from .. import util

import enum

@enum.unique
class ContextType(enum.IntEnum) :
	globalContext = 1
	functionContext = 2
	classContext = 3

class Context :
	def __init__(self, type) :
		self._type = type
		self._nameReplaceMap = {}
		self._usedNameSet = {}

	def isGlobal(self) :
		return self._type == ContextType.globalContext

	def isFunction(self) :
		return self._type == ContextType.functionContext

	def isClass(self) :
		return self._type == ContextType.classContext
	
	def getNewName(self, name) :
		if name not in self._nameReplaceMap :
			self._nameReplaceMap[name] = util.getUnusedRandomSymbol(self._usedNameSet)
		return self._nameReplaceMap[name]
	
	def findNewName(self, name, default = None) :
		if name in self._nameReplaceMap :
			return self._nameReplaceMap[name]
		return default
	
class GlobalContext(Context) :
	def __init__(self) :
		super().__init__(ContextType.globalContext)

class ClassContext(Context) :
	def __init__(self) :
		super().__init__(ContextType.classContext)

class FunctionContext(Context) :
	def __init__(self) :
		super().__init__(ContextType.functionContext)

class ContextStack :
	def __init__(self, globalContext) :
		self._contextList = [ globalContext ]

	def getCurrentContext(self) :
		assert len(self._contextList) > 0
		return self._contextList[-1]
	
	def pushContext(self, context) :
		self._contextList.append(context)
		return context
	
	def popContext(self) :
		assert len(self._contextList) > 1
		self._contextList.pop()


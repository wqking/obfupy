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

from .. import util

import enum

@enum.unique
class ContextType(enum.IntEnum) :
	functionContext = 1
	classContext = 2
	moduleContext = 3

@enum.unique
class NameType(enum.IntEnum) :
	load = 1
	store = 2
	delete = 3
	argument = 4
	attribute = 5
	globalScope = 6
	nonlocalScope = 7

@enum.unique
class Section(enum.IntEnum) :
	body = 1
	argument = 2
	decorator = 3
	baseClass = 4
	metaClass = 5

class _NameMixin :
	def seeName(self, name, type) :
		if name not in self._seenNameSet :
			self._seenNameSet[name] = [ type ]
		elif type not in self._seenNameSet[name] :
			self._seenNameSet[name].append(type)

	def isNameSeen(self, name, type = None) :
		if name not in self._seenNameSet :
			return False
		if type is None :
			return True
		if isinstance(type, (list, tuple)) :
			for t in type :
				if t in self._seenNameSet[name] :
					return True
		else :
			return type in self._seenNameSet[name]

	def getSeenNameSet(self) :
		return self._seenNameSet
	
	def seeFeature(self, feature) :
		self._seenFeatureSet[feature] = True

	def isFeatureSeen(self, feature) :
		return feature in self._seenFeatureSet

class _RenameMixin :
	def findRenamedName(self, name) :
		newName = self._doFindRenamedName(name)
		if newName is not None :
			return newName
		if self.isNameSeen(name, NameType.argument) :
			return None
		parent = self._parent
		while parent is not None :
			if parent.isFunction() or parent.isModule() :
				return parent.findRenamedName(name)
			parent = parent._parent
		return None

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
		return util.getUnusedRandomSymbol(usedMap = None, originalName = name)

	def cancelRename(self, name) :
		if name in self._renameMap :
			del self._renameMap[name]

	def isRenamed(self, name) :
		return name in self._renameMap

class _SiblingMixin :
	def addSiblingNode(self, node) :
		self._siblingNodeList.append(node)

	def getSiblingNodeList(self) :
		return self._siblingNodeList

class _SectionMixin :
	def getCurrentSection(self) :
		if len(self._sectionList) == 0 :
			return None
		return self._sectionList[-1]

	def pushSection(self, section) :
		return SectionGuard(self, section)

	def _pushSection(self, section) :
		self._sectionList.append(section)
		return section
	
	def _popSection(self) :
		assert len(self._sectionList) > 0
		self._sectionList.pop()

class _OptionMixin :
	def setOptions(self, options) :
		self._options = options

	def getOptions(self) :
		if self._options is not None :
			return self._options
		assert self._parent is not None
		return self._parent.getOptions()

class Context(_NameMixin, _RenameMixin, _SiblingMixin, _SectionMixin, _OptionMixin) :
	def __init__(self, type, contextName) :
		self._type = type
		self._contextName = contextName
		self._parent = None

		# _NameMixin
		self._seenNameSet = {}
		self._seenFeatureSet = {}

		# _SiblingMixin
		self._siblingNodeList = []

		# _RenameMixin
		self._renameMap = {}

		# _SectionMixin
		self._sectionList = []

		# _OptionMixin
		self._options = None

	def setParent(self, parent = None) :
		self._parent = parent

	def getContextName(self) :
		return self._contextName

	def isModule(self) :
		return self._type == ContextType.moduleContext

	def isClass(self) :
		return self._type == ContextType.classContext

	def isFunction(self) :
		return self._type == ContextType.functionContext
	
	def getParent(self) :
		return self._parent

class ModuleContext(Context) :
	def __init__(self, fileName, options) :
		super().__init__(ContextType.moduleContext, fileName)
		self.setOptions(options)

class FunctionContext(Context) :
	def __init__(self, funcName) :
		super().__init__(ContextType.functionContext, funcName)

class ClassContext(Context) :
	def __init__(self, className) :
		super().__init__(ContextType.classContext, className)

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
	
	def getTopScopedContext(self) :
		if len(self._contextList) > 1 :
			return self._contextList[1]
		return None
	
	def pushContext(self, context) :
		return ContextGuard(self, context)

	def _pushContext(self, context) :
		parent = None
		if len(self._contextList) > 0 :
			parent = self._contextList[-1]
		context.setParent(parent)
		self._contextList.append(context)
		return context

	def _popContext(self) :
		assert len(self._contextList) > 0
		self._contextList.pop()

class ContextGuard :
	def __init__(self, contextStack, context) :
		self._contextStack = contextStack
		self._context = context

	def __enter__(self) :
		return self._contextStack._pushContext(self._context)

	def __exit__(self, type, value, traceBack) :
		self._contextStack._popContext()

class SectionGuard :
	def __init__(self, context, section) :
		self._context = context
		self._section = section

	def __enter__(self) :
		if self._section is not None :
			return self._context._pushSection(self._section)
		return None

	def __exit__(self, type, value, traceBack) :
		if self._section is not None :
			self._context._popSection()


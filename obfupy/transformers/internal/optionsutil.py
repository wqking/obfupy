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

import copy

class _BaseOptions :
	__slots__ = ('_modified', '_data', '_readonlyNames')
	def __init__(self, data, **kwargs) :
		self._modified = False
		self._data = data
		self._readonlyNames = []
		for name in kwargs :
			setattr(self, name, kwargs[name])

	def _setReadonlyNames(self, readonlyNames) :
		self._readonlyNames = copy.deepcopy(readonlyNames)

	def _isModified(self) :
		return self._modified

	def _resetModified(self) :
		self._modified = False

	def __bool__(self) :
		return self.enabled

	def __copy__(self):
		cls = self.__class__
		result = cls.__new__(cls)
		result.__slots__ = self.__slots__
		result._modified = self._modified
		result._data = self._data
		result._readonlyNames = self._readonlyNames
		return result

	def __deepcopy__(self, memo):
		cls = self.__class__
		result = cls.__new__(cls)
		memo[id(self)] = result
		result._modified = self._modified
		result._data = copy.deepcopy(self._data, memo)
		result._readonlyNames = copy.deepcopy(self._readonlyNames, memo)
		return result

def _createOptionsClass(fullData) :
	if 'enabled' not in fullData :
		fullData['enabled'] = True
	data = {}
	for name in fullData :
		value = fullData[name]
		if isinstance(value, tuple) :
			value = value[0]
		elif isinstance(value, dict) :
			value = value['default']
		data[name] = value

	class _Options(_BaseOptions) :
		__slots__ = ()
		def __init__(self, _noCollideData = data, **kwargs):
			super().__init__(_noCollideData, **kwargs)
	_Options._fullData = fullData
	slots = [ '_data' ]
	for optionName in data :
		propertyName = optionName
		keyName = propertyName
		@property
		def prop(self, keyName = keyName):
			return self._data[keyName]
		
		if isinstance(data[optionName], _BaseOptions) :
			pass
			'''
			@prop.setter
			def prop(self, value, keyName = keyName):
				if isinstance(value, _BaseOptions) :
					# This happens during copy.deepcopy
					self._data[keyName] = value
				else :
					self._data[keyName].enabled = value
			'''
		else :
			@prop.setter
			def prop(self, value, keyName = keyName):
				if keyName in self._readonlyNames :
					raise AttributeError("Can't set readonly option: %s" % (keyName))
				self._data[keyName] = value
				self._modified = True
		setattr(_Options, propertyName, prop)
		slots.append(propertyName)
	setattr(_Options, '__slots__', slots)
	return _Options

def _createOptionsObject(data) :
	return _createOptionsClass(data)()

EmptyOptions = _createOptionsClass({})

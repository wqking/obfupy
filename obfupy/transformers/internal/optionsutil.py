import copy

class _BaseOptions :
	__slots__ = ('_modified', '_data')
	def __init__(self, data = None) :
		self._modified = False
		self._data = data or {}

	def _isModified(self) :
		return self._modified

	def _resetModified(self) :
		self._modified = False

	def __bool__(self) :
		return self.enabled

def _createOptionsClass(data) :
	data = copy.deepcopy(data)
	if 'enabled' not in data :
		data['enabled'] = True
	class _Options(_BaseOptions) :
		__slots__ = ()
		def __init__(self, data = data):
			super().__init__(data)
	slots = [ '_data' ]
	for optionName in data :
		propertyName = optionName
		keyName = propertyName
		@property
		def prop(self, keyName = keyName):
			return self._data[keyName]
		
		if False and isinstance(data[optionName], _BaseOptions) :
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
				self._data[keyName] = value
				self._modified = True
		setattr(_Options, propertyName, prop)
		slots.append(propertyName)
	setattr(_Options, '__slots__', slots)
	return _Options

def _createOptionsObject(data) :
	return _createOptionsClass(data)()

EmptyOptions = _createOptionsClass({})

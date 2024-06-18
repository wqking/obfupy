import copy

_optionNameSkip = '_skip'

def _shouldSkip(options) :
	return (
		options is not None
		and _optionNameSkip in options
		and options[_optionNameSkip]
	)

def _shouldSkipFile(callback, fileName) :
	options = _invokeCallback(callback, _FileCallbackData(fileName))
	return _shouldSkip(options)

def _invokeCallback(callback, data) :
	if callback is None :
		return None
	callback(data)
	if data._isModified() :
		return data._makeOptions()
	return None

class _FileCallbackData :
	def __init__(self, fileName) :
		self._fileName = fileName
		self._skip = False
		self._modified = False

	def getFileName(self) :
		return self._fileName
	
	def isFile(self) :
		return True

	def skip(self) :
		self._willModifyOptions()
		self._skip = True
	
	def _shouldSkip(self) :
		return self._skip

	def _willModifyOptions(self) :
		self._modified = True

	def _isModified(self) :
		return self._modified
	
	def _makeOptions(self) :
		return {
			_optionNameSkip : self._skip
		}

class _OptionCallbackData(_FileCallbackData) :
	def __init__(self, fileName, options) :
		super().__init__(fileName)
		self._options = options
		self._needCopy = True

	def getOption(self, name) :
		return self._options[name]
	
	def setOption(self, name, value) :
		self._willModifyOptions()
		self._options[name] = value

	def _willModifyOptions(self) :
		super()._willModifyOptions()
		if self._needCopy :
			self._needCopy = False
			self._options = copy.deepcopy(self._options)

	def _makeOptions(self) :
		self._options[_optionNameSkip] = self._skip
		return self._options


import copy

_optionNameSkip = '_skip'

def _shouldSkip(options) :
	return (
		options is not None
		and options._skip
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

	def getFileName(self) :
		return self._fileName
	
	def isFile(self) :
		return True

	def skip(self) :
		self._skip = True
	
	def _shouldSkip(self) :
		return self._skip

	def _isModified(self) :
		return self._skip
	
	def _makeOptions(self) :
		def x() :
			pass
		x._skip = self._skip
		return x

class _OptionCallbackData(_FileCallbackData) :
	def __init__(self, fileName, options) :
		super().__init__(fileName)
		options._resetModified()
		self._original = options
		self._options = None
		self._needCopy = True

	@property
	def options(self) :
		if self._options is None :
			self._options = copy.deepcopy(self._original)
		return self._options

	def _isModified(self) :
		return self._options is not None and self._options._isModified()

	def _makeOptions(self) :
		return self._options


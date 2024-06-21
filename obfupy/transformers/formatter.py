from .internal.iformatter import _IFormatter
from .internal import util as util

import copy

class Options :
	def __init__(self) :
		self._modified = False
		self._data = {
			'_skip' : False,
			'removeComment' : True,
			'expandIndent' : True,
			'addExtraSpaces' : True,
			'addExtraNewLines' : True,
		}

	def _isModified(self) :
		return self._modified

	def _resetModified(self) :
		self._modified = False
util.addOptionPropertiesToClass(Options, Options()._data)

class Formatter :
	def __init__(self, options = None, callback = None) :
		if options is None :
			options = Options()
		self._options = copy.deepcopy(options)
		self._callback = callback

	def transform(self, documentManager) :
		_IFormatter(options = self._options, callback = self._callback).transform(documentManager)

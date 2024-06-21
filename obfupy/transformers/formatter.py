from .internal.iformatter import _IFormatter
from .internal import util
from .internal import optionsutil

import copy

Options = optionsutil._createOptionsClass({
	'removeComment' : True,
	'expandIndent' : True,
	'addExtraSpaces' : True,
	'addExtraNewLines' : True,
})

class Formatter :
	def __init__(self, options = None, callback = None) :
		if options is None :
			options = Options()
		self._options = copy.deepcopy(options)
		self._callback = callback

	def transform(self, documentManager) :
		_IFormatter(options = self._options, callback = self._callback).transform(documentManager)

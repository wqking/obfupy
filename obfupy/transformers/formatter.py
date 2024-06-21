from .internal.iformatter import _IFormatter
from .internal import util as util

import enum

class OptionNames(str, enum.Enum) :
	removeComment = 'removeComment'
	expandIndent = 'expandIndent'
	addExtraSpaces = 'addExtraSpaces'
	addExtraNewLines = 'addExtraNewLines'

_defaultOptions = {
	OptionNames.removeComment : True,
	OptionNames.expandIndent : True,
	OptionNames.addExtraSpaces : True,
	OptionNames.addExtraNewLines : True,
}

class Formatter :
	def __init__(self, options = None, callback = None) :
		util.verifyOptionsKeyType(options, OptionNames, "formatter.OptionNames")
		self._options = util.makeOptions(options, _defaultOptions)
		self._callback = callback

	def transform(self, documentManager) :
		_IFormatter(options = self._options, callback = self._callback).transform(documentManager)

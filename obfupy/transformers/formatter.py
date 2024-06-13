from .internal.iformatter import _IFormatter

class Formatter :
	def __init__(
			self,
			removeComment = True,
			expandIndent = True,
			addExtraSpaces = True,
			addExtraNewLines = True
		) :
		self._options = {
			'removeComment' : removeComment,
			'expandIndent' : expandIndent,
			'addExtraSpaces' : addExtraSpaces,
			'addExtraNewLines' : addExtraNewLines,
		}

	def transform(self, documentManager) :
		_IFormatter(self._options).transform(documentManager)

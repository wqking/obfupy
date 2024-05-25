from .internal.iliteral import _ILiteral

class Literal :
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
		_ILiteral(self._options).transform(documentManager)

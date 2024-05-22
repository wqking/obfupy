from .internal.irenamer import _IRenamer

class Renamer :
	def __init__(
			self,
			removeComment = True,
			removeDocString = True,
			expandIndent = True,
			addExtraSpaces = True
		) :
		self._removeComment = removeComment
		self._removeDocString = removeDocString
		self._expandIndent = expandIndent
		self._addExtraSpaces = addExtraSpaces

	def transform(self, documentManager) :
		_IRenamer(
			removeComment = self._removeComment,
			removeDocString = self._removeDocString,
			expandIndent = self._expandIndent,
			addExtraSpaces = self._addExtraSpaces
		).transform(documentManager)

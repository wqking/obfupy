from .internal.irewriter import _IRewriter

class Rewriter :
	def __init__(self) :
		self._options = {
			'constantAsVariable' : True
		}

	def transform(self, documentManager) :
		_IRewriter(self._options).transform(documentManager)

from .internal.irewriter import _IRewriter

class Rewriter :
	def __init__(self, constantAsVariable = True) :
		self._options = {
			'constantAsVariable' : constantAsVariable,
			'renameArgument' : False
		}

	def transform(self, documentManager) :
		_IRewriter(self._options).transform(documentManager)

from .internal.irewriter import _IRewriter

class Rewriter :
	def transform(self, documentManager) :
		_IRewriter().transform(documentManager)

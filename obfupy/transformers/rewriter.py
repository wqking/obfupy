from .internal.irewriter import _IRewriter
from .utils import stringencoders

class Rewriter :
	def __init__(self,
			  stringEncoders = stringencoders.defaultEncoders
		) :
		self._options = {
			'renameArgument' : True,
			'stringEncoders' : stringEncoders
		}

	def transform(self, documentManager) :
		_IRewriter(self._options).transform(documentManager)

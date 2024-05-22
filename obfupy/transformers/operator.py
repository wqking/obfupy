from .internal.ioperator import _IOperator

class Operator :
	def transform(self, documentManager) :
		_IOperator().transform(documentManager)

from .internal.irenamer import _IRenamer

class Renamer :
	def transform(self, documentManager) :
		_IRenamer().transform(documentManager)

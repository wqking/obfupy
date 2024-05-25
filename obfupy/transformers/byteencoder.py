from .internal.ibyteencoder import _IByteEncoder

class ByteEncoder :
	def transform(self, documentManager) :
		_IByteEncoder().transform(documentManager)

class DocumentManager :
	def __init__(self) :
		self._documentList = []

	def getDocumentList(self) :
		return self._documentList

	def addDocument(self, document) :
		if isinstance(document, list) :
			self._documentList += document
		else :
			self._documentList.append(document)

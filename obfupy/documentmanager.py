class DocumentManager :
	def __init__(self) :
		self._documentList = []
		self._uidDocumentMap = {}

	def getDocumentList(self) :
		return self._documentList

	def addDocument(self, document) :
		if isinstance(document, list) :
			self._documentList += document
			for doc in document :
				self._uidDocumentMap[doc.getUid()] = doc
		else :
			self._documentList.append(document)
			self._uidDocumentMap[document.getUid()] = document

	def getDocumentByUid(self, uid) :
		return self._uidDocumentMap[uid]

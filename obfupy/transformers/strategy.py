class Strategy :
	def __init__(self) :
		self._documentManager = None

	def getDocumentManager(self) :
		return self._documentManager
	
	def process(self, documentManager) :
		self._documentManager = documentManager
		self.doProcess()

	def doProcess(self) :
		documentManager = self.getObfuscator().getDocumentManager()
		for document in documentManager.getDocumentList() :
			self.doProcessDocument(document)

	def doProcessDocument(self, doc) :
		pass

import os

class Document :
	def __init__(self) :
		self._fileName = ''
		self._content = ''

	def loadFromFile(self, fileName) :
		fileName = os.path.abspath(fileName)
		with open(fileName, "r") as file :
			self._content = file.read()
			self._fileName = fileName
		return self

	def getContent(self) :
		return self._content

	def setContent(self, content) :
		self._content = str(content)

	def getFileName(self) :
		return self._fileName

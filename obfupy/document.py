import os
import codecs

class Document :
	_uidSeed = 1

	def __init__(self) :
		self._fileName = ''
		self._content = ''
		self._uid = 'uid_%d' % (Document._uidSeed)
		Document._uidSeed += 1

	def loadFromFile(self, fileName) :
		file = codecs.open(fileName, "r", "utf-8")
		self._content = file.read()
		file.close()
		self._fileName = fileName
		return self

	def getContent(self) :
		return self._content

	def setContent(self, content) :
		self._content = str(content)

	def getFileName(self) :
		return self._fileName

	def getUid(self) :
		return self._uid

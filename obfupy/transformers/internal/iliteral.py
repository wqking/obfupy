import re
import ast
import tokenize
import random
import io
from collections import namedtuple

from . import util

class _ILiteral :
	def __init__(self, options) :
		self._options = options
		self._documentManager = None
		self._uidTokenListMap = {}

	def transform(self, documentManager) :
		self._documentManager = documentManager
		self.buildUidTokenListMap()
		if self._options['removeComment'] :
			self.removeComment()
		if self._options['expandIndent'] :
			self.expandIndent()
		if self._options['addExtraSpaces'] :
			self.addExtraSpaces()
		if self._options['addExtraNewLines'] :
			self.addExtraNewLines()
		self.finalize()

	def getDocumentList(self) :
		return self._documentManager.getDocumentList()
	
	def hashSymbolPosition(self, document, line, column) :
		return f"{document.getUid()}_{line}_{column}"

	def buildUidTokenListMap(self) :
		for document in self.getDocumentList() :
			content = document.getContent()
			generator = tokenize.tokenize(io.BytesIO(content.encode('utf-8')).readline)
			tokenList = []
			for tokenType, tokenValue, _,  _, _ in generator:
				tokenList.append((tokenType, tokenValue))
			self._uidTokenListMap[document.getUid()] = tokenList

	def addExtraSpaces(self) :
		for document in self.getDocumentList() :
			tokenList = self._uidTokenListMap[document.getUid()]
			enumerator = TokenEnumerator(tokenList)
			while True :
				token = enumerator.nextToken()
				if token is None :
					break
				if token.type == tokenize.OP :
					tokenValue = token.value
					extraSpaces = self.getRandomSpaces()
					tokenValue += extraSpaces
					if not enumerator.isPreviousTokenIndentOrNewLine() :
						tokenValue = extraSpaces + tokenValue
					enumerator.setCurrentValue(tokenValue)

	def addExtraNewLines(self) :
		for document in self.getDocumentList() :
			tokenList = self._uidTokenListMap[document.getUid()]
			enumerator = TokenEnumerator(tokenList)
			while True :
				token = enumerator.nextToken()
				if token is None :
					break
				if token.type == tokenize.NEWLINE :
					enumerator.setCurrentValue(token.value * random.randint(1, 10))

	def expandIndent(self) :
		for document in self.getDocumentList() :
			self.expandIndentForDocument(document)

	def expandIndentForDocument(self, document) :
		minIndentLength = 0
		tokenList = self._uidTokenListMap[document.getUid()]
		enumerator = TokenEnumerator(tokenList)
		while True :
			token = enumerator.nextToken()
			if token is None :
				break
			if token.type == tokenize.INDENT :
				if minIndentLength == 0 or len(token.value) < minIndentLength :
					minIndentLength = len(token.value)
				if minIndentLength > 0 and len(token.value) % minIndentLength != 0 :
					return
		if minIndentLength == 0 :
			return
		newIndent = self.getRandomSpaces()
		enumerator = TokenEnumerator(tokenList)
		while True :
			token = enumerator.nextToken()
			if token is None :
				break
			if token.type == tokenize.INDENT :
				enumerator.setCurrentValue(newIndent * (len(token.value) // minIndentLength))

	def getRandomSpaces(self) :
		if random.randint(0, 1) == 0 :
			return '\t' * random.randint(8, 16)
		else :
			return ' ' * random.randint(16, 32)
		
	def removeComment(self) :
		for document in self.getDocumentList() :
			tokenList = self._uidTokenListMap[document.getUid()]
			for i in range(len(tokenList)) :
				enumerator = TokenEnumerator(tokenList)
				while True :
					token = enumerator.nextToken()
					if token is None :
						break
					if token.type == tokenize.COMMENT :
						enumerator.setCurrentValue('')

	def finalize(self) :
		for document in self.getDocumentList() :
			tokenList = self._uidTokenListMap[document.getUid()]
			content = tokenize.untokenize(tokenList).decode('utf-8')
			document.setContent(content)

Token = namedtuple("Token", "type value")

class TokenEnumerator :
	def __init__(self, tokenList) :
		self._tokenList = tokenList
		self._previousTokenType = None
		self._currentTokenType = None
		self._currentTokenValue = None
		self._currentIndex = -1
		self._inImportLine = False

	def nextToken(self) :
		self._currentIndex += 1
		if self._currentIndex >= len(self._tokenList) :
			self._currentIndex -= 1
			return None
		self._previousTokenType = self._currentTokenType
		self._currentTokenType, self._currentTokenValue = self._tokenList[self._currentIndex]
		if self._currentTokenType == tokenize.NAME and self._currentTokenValue in [ 'import', 'from' ] :
			if self.isPreviousTokenIndentOrNewLine() :
				self._inImportLine = True
		if self._currentTokenType == tokenize.NEWLINE :
			self._inImportLine = False
		return Token(type = self._currentTokenType, value = self._currentTokenValue)
	
	def isPreviousTokenIndentOrNewLine(self) :
		return self._previousTokenType in [ tokenize.ENCODING, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.NL ]
	
	def isInImportLine(self) :
		return self._inImportLine
	
	def setCurrentValue(self, tokenValue) :
		self._tokenList[self._currentIndex] = (self._currentTokenType, tokenValue)
	
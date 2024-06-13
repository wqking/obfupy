import re
import ast
import tokenize
import random
import io
from collections import namedtuple

from . import util

class _IFormatter :
	def __init__(self, options) :
		self._options = options
		self._documentManager = None
		self._uidTokenListMap = {}

	def transform(self, documentManager) :
		self._documentManager = documentManager
		self._buildUidTokenListMap()
		self._doLiteral()
		self._finalize()

	def _getDocumentList(self) :
		return self._documentManager.getDocumentList()
	
	def _buildUidTokenListMap(self) :
		for document in self._getDocumentList() :
			content = document.getContent()
			generator = tokenize.tokenize(io.BytesIO(content.encode('utf-8')).readline)
			tokenList = []
			for tokenType, tokenValue, _,  _, _ in generator:
				tokenList.append((tokenType, tokenValue))
			self._uidTokenListMap[document.getUid()] = tokenList

	def _doLiteral(self) :
		for document in self._getDocumentList() :
			self._doLiteralForDocument(document)

	def _doLiteralForDocument(self, document) :
		minIndentLength = 0
		canExpandIndent = True
		tokenList = self._uidTokenListMap[document.getUid()]
		enumerator = TokenEnumerator(tokenList)
		while True :
			token = enumerator.nextToken()
			if token is None :
				break

			if token.type == tokenize.OP and self._options['addExtraSpaces'] and token.value not in [ '!' ] :
				tokenValue = token.value
				extraSpaces = self._getRandomSpaces()
				tokenValue += extraSpaces
				if not enumerator.isPreviousTokenIndentOrNewLine() :
					tokenValue = extraSpaces + tokenValue
				enumerator.setCurrentValue(tokenValue)

			if token.type == tokenize.NEWLINE and self._options['addExtraNewLines']:
				enumerator.setCurrentValue(token.value * random.randint(1, 10))

			if token.type == tokenize.COMMENT and self._options['removeComment']:
				enumerator.setCurrentValue('')

			if token.type == tokenize.INDENT :
				if minIndentLength == 0 or len(token.value) < minIndentLength :
					minIndentLength = len(token.value)
				if minIndentLength > 0 and len(token.value) % minIndentLength != 0 :
					canExpandIndent = False

		if self._options['expandIndent'] and canExpandIndent and minIndentLength > 0 :
			newIndent = self._getRandomSpaces()
			enumerator = TokenEnumerator(tokenList)
			while True :
				token = enumerator.nextToken()
				if token is None :
					break
				if token.type == tokenize.INDENT :
					enumerator.setCurrentValue(newIndent * (len(token.value) // minIndentLength))

	def _getRandomSpaces(self) :
		if random.randint(0, 1) == 0 :
			return '\t' * random.randint(8, 16)
		else :
			return ' ' * random.randint(16, 32)
		
	def _finalize(self) :
		for document in self._getDocumentList() :
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

	def nextToken(self) :
		self._currentIndex += 1
		if self._currentIndex >= len(self._tokenList) :
			self._currentIndex -= 1
			return None
		self._previousTokenType = self._currentTokenType
		self._currentTokenType, self._currentTokenValue = self._tokenList[self._currentIndex]
		return Token(type = self._currentTokenType, value = self._currentTokenValue)
	
	def isPreviousTokenIndentOrNewLine(self) :
		return self._previousTokenType in [ tokenize.ENCODING, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.NL ]
	
	def setCurrentValue(self, tokenValue) :
		self._tokenList[self._currentIndex] = (self._currentTokenType, tokenValue)
	
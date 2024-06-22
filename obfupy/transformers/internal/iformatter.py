# obfupy library
#
# Copyright (C) 2024 Wang Qi (wqking)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import ast
import tokenize
import random
import io
from collections import namedtuple

from . import util
from . import callbackdata
from .. import formatter

class _IFormatter :
	def __init__(self, options, callback) :
		self._options = options
		self._callback = callback

	def transform(self, documentManager) :
		for document in documentManager.getDocumentList() :
			options = callbackdata._invokeCallback(self._callback, callbackdata._OptionCallbackData(document.getFileName(), self._options)) or self._options
			if not options.enabled :
				continue
			generator = tokenize.tokenize(io.BytesIO(document.getContent().encode('utf-8')).readline)
			tokenList = []
			for tokenType, tokenValue, _,  _, _ in generator:
				tokenList.append((tokenType, tokenValue))
			self._doFormatForDocument(tokenList, options)
			content = tokenize.untokenize(tokenList).decode('utf-8')
			document.setContent(content)

	def _doFormatForDocument(self, tokenList, options) :
		minIndentLength = 0
		canExpandIndent = True
		enumerator = TokenEnumerator(tokenList)
		while True :
			token = enumerator.nextToken()
			if token is None :
				break

			if token.type == tokenize.OP and options.addExtraSpaces and token.value not in [ '!' ] :
				tokenValue = token.value
				extraSpaces = self._getRandomSpaces()
				tokenValue += extraSpaces
				if not enumerator.isPreviousTokenIndentOrNewLine() :
					tokenValue = extraSpaces + tokenValue
				enumerator.setCurrentValue(tokenValue)

			if token.type == tokenize.NEWLINE and options.addExtraNewLines:
				enumerator.setCurrentValue(token.value * random.randint(1, 10))

			if token.type == tokenize.COMMENT and options.removeComment:
				enumerator.setCurrentValue('')

			if token.type == tokenize.INDENT :
				if minIndentLength == 0 or len(token.value) < minIndentLength :
					minIndentLength = len(token.value)
				if minIndentLength > 0 and len(token.value) % minIndentLength != 0 :
					canExpandIndent = False

		if options.expandIndent and canExpandIndent and minIndentLength > 0 :
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
	
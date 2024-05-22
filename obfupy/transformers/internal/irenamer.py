import re
import ast
import tokenize
import random
import io
from collections import namedtuple

class _IRenamer :
	def __init__(
			self,
			removeComment = True,
			removeDocString = True,
			expandIndent = True,
			addExtraSpaces = True
		) :
		self._removeComment = removeComment
		self._removeDocString = removeDocString
		self._expandIndent = expandIndent
		self._addExtraSpaces = addExtraSpaces
		self._documentManager = None
		self._randomSymbolLeadLetters = 'Il'
		self._randomSymbolAllLetters = self._randomSymbolLeadLetters + '1'
		self._symbolMap = {}
		self._uidTokenListMap = {}

	def transform(self, documentManager) :
		self._documentManager = documentManager
		self.buildUidTokenListMap()
		if self._removeComment :
			self.removeComment()
		if self._removeDocString :
			self.removeDocString()
		if self._expandIndent :
			self.expandIndent()
		if self._addExtraSpaces :
			self.addExtraSpaces()
		self.extractAllSymbols()
		self.doFilterSymbols()
		self.generateNewSymbols()
		self.rename()
		self.finalize()
		#print(self._symbolMap)

	def getDocumentList(self) :
		return self._documentManager.getDocumentList()

	def extractAllSymbols(self) :
		for document in self.getDocumentList() :
			parsedAst = ast.parse(document.getContent())
			for node in ast.walk(parsedAst) :
				if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef) :
					print(node.lineno, node.col_offset)
					self._symbolMap[node.name] = None
					if node.args.args :
						for arg in node.args.args :
							self._symbolMap[arg.arg] = None
				if isinstance(node, ast.ClassDef) :
					print(node.lineno, node.col_offset)
					self._symbolMap[node.name] = None
				if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load) :
					print(node.lineno, node.col_offset, node.id)
					self._symbolMap[node.id] = None
				#if isinstance(node, ast.Attribute) and not isinstance(node.ctx, ast.Load) :
				#	self._symbolMap[node.attr] = None

	def doFilterSymbols(self) :
		result = {}
		reservedMap = {}
		self.buildReservedSymbols(reservedMap)
		for name in self._symbolMap :
			if name in reservedMap :
				continue
			if not self.isValidSymbolName(name) :
				continue
			result[name] = self._symbolMap[name]
		self._symbolMap = result

	def isValidSymbolName(self, name) :
		if re.match(r'^__.*__$', name) :
			return False
		return True

	def generateNewSymbols(self) :
		usedMap = {}
		for name in self._symbolMap :
			length = 12
			while True :
				newName = self.generateSingleNewSymbol(length)
				if newName not in usedMap :
					usedMap[newName] = True
					self._symbolMap[name] = newName
					break
				length = None

	def generateSingleNewSymbol(self, length = None) :
		if length is None :
			length = random.randint(6, 20)
		result = random.choice(self._randomSymbolLeadLetters)
		while len(result) < length :
			result += random.choice(self._randomSymbolAllLetters)
		return result
	
	def buildUidTokenListMap(self) :
		for document in self.getDocumentList() :
			content = document.getContent()
			generator = tokenize.tokenize(io.BytesIO(content.encode('utf-8')).readline)
			tokenList = []
			for tokenType, tokenValue, start,  end, line in generator:
				tokenList.append((tokenType, tokenValue, start, end, line))
			self._uidTokenListMap[document.getUid()] = tokenList

	def buildReservedSymbols(self, reservedMap) :
		for document in self.getDocumentList() :
			tokenList = self._uidTokenListMap[document.getUid()]
			enumerator = TokenEnumerator(tokenList)
			while True :
				token = enumerator.nextToken()
				if token is None :
					break
				tokenValue = token.value
				needReserve = False
				if token.type == tokenize.STRING and len(tokenValue) > 2 and tokenValue[0] == 'f' :
					needReserve = True
				if enumerator.isInImportLine() :
					needReserve = True
				if needReserve :
					symbols = re.findall(r'\b[\w\d_]+\b', tokenValue)
					for name in symbols :
						reservedMap[name] = None

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

	def expandIndent(self) :
		for document in self.getDocumentList() :
			self.expandIndentForDocument(document)

	def expandIndentForDocument(self, document) :
		newIndent = self.getRandomSpaces()
		minIndentLength = 0
		tokenList = self._uidTokenListMap[document.getUid()]
		for i in range(len(tokenList)) :
			tokenType, tokenValue = tokenList[i]
			if tokenType == tokenize.INDENT :
				if minIndentLength == 0 or len(tokenValue) < minIndentLength :
					minIndentLength = len(tokenValue)
				if minIndentLength > 0 and len(tokenValue) % minIndentLength != 0 :
					return
		if minIndentLength == 0 :
			return
		for i in range(len(tokenList)) :
			tokenType, tokenValue = tokenList[i]
			if tokenType == tokenize.INDENT :
				tokenValue = newIndent * (len(tokenValue) // minIndentLength)
				tokenList[i] = (tokenType, tokenValue)

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

	def removeDocString(self) :
		for document in self.getDocumentList() :
			tokenList = self._uidTokenListMap[document.getUid()]
			enumerator = TokenEnumerator(tokenList)
			while True :
				token = enumerator.nextToken()
				if token is None :
					break
				if token.type == tokenize.STRING :
					if enumerator.isPreviousTokenIndentOrNewLine() :
						enumerator.setCurrentValue('')

	def rename(self) :
		for document in self.getDocumentList() :
			tokenList = self._uidTokenListMap[document.getUid()]
			enumerator = TokenEnumerator(tokenList)
			while True :
				token = enumerator.nextToken()
				if token is None :
					break
				if not enumerator.isInImportLine() :
					if token.type == tokenize.NAME :
						if token.value in self._symbolMap :
							print(token.value, token.start)
							enumerator.setCurrentValue(self._symbolMap[token.value])

	def finalize(self) :
		for document in self.getDocumentList() :
			tokenList = self._uidTokenListMap[document.getUid()]
			content = tokenize.untokenize(tokenList).decode('utf-8')
			document.setContent(content)

Token = namedtuple("Token", "type value start")

class TokenEnumerator :
	def __init__(self, tokenList) :
		self._tokenList = tokenList
		self._previousTokenType = None
		self._currentTokenType = None
		self._currentTokenValue = None
		self._currentTokenStart = None
		self._currentTokenEnd = None
		self._currentTokenLine = None
		self._currentIndex = -1
		self._inImportLine = False

	def nextToken(self) :
		self._currentIndex += 1
		if self._currentIndex >= len(self._tokenList) :
			self._currentIndex -= 1
			return None
		self._previousTokenType = self._currentTokenType
		self._currentTokenType, self._currentTokenValue, self._currentTokenStart, self._currentTokenEnd, self._currentTokenLine = self._tokenList[self._currentIndex]
		if self._currentTokenType == tokenize.NAME and self._currentTokenValue in [ 'import', 'from' ] :
			if self.isPreviousTokenIndentOrNewLine() :
				self._inImportLine = True
		if self._currentTokenType == tokenize.NEWLINE :
			self._inImportLine = False
		return Token(type = self._currentTokenType, value = self._currentTokenValue, start = self._currentTokenStart)
	
	def isPreviousTokenIndentOrNewLine(self) :
		return self._previousTokenType in [ tokenize.ENCODING, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.NL ]
	
	def isInImportLine(self) :
		return self._inImportLine
	
	def setCurrentValue(self, tokenValue) :
		self._tokenList[self._currentIndex] = (self._currentTokenType, tokenValue, self._currentTokenStart, self._currentTokenEnd, self._currentTokenLine)
	
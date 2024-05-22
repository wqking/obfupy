import re
import ast
import tokenize
import random
import io

class _IRenamer :
	def __init__(self) :
		self._documentManager = None
		self._randomSymbolLeadLetters = 'Il'
		self._randomSymbolAllLetters = self._randomSymbolLeadLetters + '1'
		self._symbolMap = {}
		self._uidTokenListMap = {}

	def transform(self, documentManager) :
		self._documentManager = documentManager
		self.buildUidTokenListMap()
		self.extractAllSymbols()
		self.doFilterSymbols()
		self.generateNewSymbols()
		self.removeComment()
		self.removeDocString()
		self.expandIndent()
		self.insertExtraSpaces()
		self.rename()
		self.finalize()
		print(self._symbolMap)

	def getDocumentList(self) :
		return self._documentManager.getDocumentList()

	def extractAllSymbols(self) :
		for document in self.getDocumentList() :
			parsedAst = ast.parse(document.getContent())
			for node in ast.walk(parsedAst) :
				if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef) :
					self._symbolMap[node.name] = None
					if node.args.args :
						for arg in node.args.args :
							self._symbolMap[arg.arg] = None
				if isinstance(node, ast.ClassDef) :
					self._symbolMap[node.name] = None
				if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load) :
					self._symbolMap[node.id] = None
				if isinstance(node, ast.Attribute) and not isinstance(node.ctx, ast.Load) :
					self._symbolMap[node.attr] = None

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
			for tokenType, tokenValue,  _,  _, _ in generator:
				tokenList.append((tokenType, tokenValue))
			self._uidTokenListMap[document.getUid()] = tokenList

	def buildReservedSymbols(self, reservedMap) :
		for document in self.getDocumentList() :
			for tokenType, tokenValue in self._uidTokenListMap[document.getUid()]:
				if tokenType == tokenize.STRING and len(tokenValue) > 2 and tokenValue[0] == 'f' :
					symbols = re.findall(r'\b[\w\d_]+\b', tokenValue)
					for name in symbols :
						reservedMap[name] = None

	def insertExtraSpaces(self) :
		for document in self.getDocumentList() :
			previousIsIndent = False
			tokenList = self._uidTokenListMap[document.getUid()]
			for i in range(len(tokenList)) :
				tokenType, tokenValue = tokenList[i]
				if tokenType == tokenize.OP :
					extraSpaces = self.getRandomSpaces()
					tokenValue += extraSpaces
					if not previousIsIndent :
						tokenValue = extraSpaces + tokenValue
				previousIsIndent = (tokenType == tokenize.INDENT)
				tokenList[i] = (tokenType, tokenValue)

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
				tokenType, tokenValue = tokenList[i]
				if tokenType == tokenize.COMMENT :
					tokenValue = ''
					tokenList[i] = (tokenType, tokenValue)

	def removeDocString(self) :
		for document in self.getDocumentList() :
			tokenList = self._uidTokenListMap[document.getUid()]
			previousTokenType = None
			for i in range(len(tokenList)) :
				tokenType, tokenValue = tokenList[i]
				if tokenType == tokenize.STRING :
					if previousTokenType == tokenize.INDENT or previousTokenType == tokenize.NEWLINE :
						tokenValue = ''
						tokenList[i] = (tokenType, tokenValue)
				previousTokenType = tokenType

	def rename(self) :
		for document in self.getDocumentList() :
			tokenList = self._uidTokenListMap[document.getUid()]
			for i in range(len(tokenList)) :
				tokenType, tokenValue = tokenList[i]
				if tokenType == tokenize.NAME :
					if tokenValue in self._symbolMap :
						tokenValue = self._symbolMap[tokenValue]
				tokenList[i] = (tokenType, tokenValue)

	def finalize(self) :
		for document in self.getDocumentList() :
			tokenList = self._uidTokenListMap[document.getUid()]
			content = tokenize.untokenize(tokenList).decode('utf-8')
			document.setContent(content)

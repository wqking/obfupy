import re
import ast
import tokenize
import random
import io

class _IRenamer :
	def __init__(self) :
		self._documentManager = None
		self._randomSymbolLeadLetters = 'iIloO'
		self._randomSymbolAllLetters = self._randomSymbolLeadLetters + '0123456789'

	def transform(self, documentManager) :
		self._documentManager = documentManager
		symbolMap = {}
		self.extractAllSymbols(symbolMap)
		symbolMap = self.doFilterSymbols(symbolMap)
		self.generateNewSymbols(symbolMap)
		self.replaceAllDocuments(symbolMap)
		print(symbolMap)

	def getDocumentList(self) :
		return self._documentManager.getDocumentList()

	def extractAllSymbols(self, symbolMap) :
		for document in self.getDocumentList() :
			self.extractAllSymbolsFromDocument(document, symbolMap)

	def extractAllSymbolsFromDocument(self, document, symbolMap) :
		parsedAst = ast.parse(document.getContent())
		for node in ast.walk(parsedAst) :
			if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef) :
				symbolMap[node.name] = None
				if node.args.args :
					for arg in node.args.args :
						symbolMap[arg.arg] = None
			if isinstance(node, ast.ClassDef) :
				symbolMap[node.name] = None
			if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load) :
				symbolMap[node.id] = None
			if isinstance(node, ast.Attribute) and not isinstance(node.ctx, ast.Load) :
				symbolMap[node.attr] = None

	def doFilterSymbols(self, symbolMap) :
		result = {}
		reservedMap = {}
		self.buildReservedSymbols(reservedMap)
		for name in symbolMap :
			if name in reservedMap :
				continue
			if not self.isValidSymbolName(name) :
				continue
			result[name] = symbolMap[name]
		return result

	def isValidSymbolName(self, name) :
		if re.match(r'^__.*__$', name) :
			return False
		return True

	def generateNewSymbols(self, symbolMap) :
		usedMap = {}
		for name in symbolMap :
			while True :
				newName = self.generateSingleNewSymbol()
				if newName not in usedMap :
					usedMap[newName] = True
					symbolMap[name] = newName
					break

	def generateSingleNewSymbol(self) :
		length = random.randint(6, 20)
		result = random.choice(self._randomSymbolLeadLetters)
		while len(result) < length :
			result += random.choice(self._randomSymbolAllLetters)
		return result

	def buildReservedSymbols(self, reservedMap) :
		for document in self.getDocumentList() :
			self.buildReservedSymbolsForDocument(document, reservedMap)

	def buildReservedSymbolsForDocument(self, document, reservedMap) :
		content = document.getContent()
		generator = tokenize.tokenize(io.BytesIO(content.encode('utf-8')).readline)
		for tokenType, tokenValue,  _,  _, _ in generator:
			if tokenType == tokenize.STRING and len(tokenValue) > 2 and tokenValue[0] == 'f' :
				symbols = re.findall(r'\b[\w\d_]+\b', tokenValue)
				for name in symbols :
					reservedMap[name] = None

	def replaceAllDocuments(self, symbolMap) :
		for document in self.getDocumentList() :
			self.replaceDocument(document, symbolMap)

	def replaceDocument(self, document, symbolMap) :
		content = document.getContent()
		tokenList = []
		generator = tokenize.tokenize(io.BytesIO(content.encode('utf-8')).readline)
		for tokenType, tokenValue,  _,  _, _ in generator:
			if tokenType == tokenize.NAME :
				if tokenValue in symbolMap :
					tokenValue = symbolMap[tokenValue]
			tokenList.append((tokenType, tokenValue))
		content = tokenize.untokenize(tokenList).decode('utf-8')
		document.setContent(content)


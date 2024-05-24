from .internal import util

import re

class Replacer :
	def __init__(self, symbols, regexps = None) :
		self._nameMap = {}
		if isinstance(symbols, list) :
			for name in symbols :
				self._nameMap[f'\\b{name}\\b'] = None
		elif isinstance(symbols, dict) :
			for name in symbols :
				self._nameMap[f'\\b{name}\\b'] = symbols[name]
		if regexps is not None :
			for name in regexps :
				self._nameMap[name] = None

	def transform(self, documentManager) :
		for name in self._nameMap :
			if self._nameMap[name] is None :
				self._nameMap[name] = util.getUniqueRandomSymbol()
		for document in documentManager.getDocumentList() :
			self.doReplaceDocument(document)

	def doReplaceDocument(self, document) :
		content = document.getContent()
		for name in self._nameMap :
			content = re.sub(name, self._nameMap[name], content)
		document.setContent(content)

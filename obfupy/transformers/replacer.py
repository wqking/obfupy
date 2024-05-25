from .internal import util

import re
import tokenize
import io

class Replacer :
	def __init__(self, symbols, regexps = None, reportIfReplacedInString = True) :
		self._reportIfReplacedInString = reportIfReplacedInString
		self._nameMap = {}
		if isinstance(symbols, list) :
			for name in symbols :
				self._nameMap[name] = {
					'regexp' : f'\\b{name}\\b',
					'replacement' : None
				}
		elif isinstance(symbols, dict) :
			for name in symbols :
				self._nameMap[name] = {
					'regexp' : f'\\b{name}\\b',
					'replacement' : symbols[name]
				}
		if regexps is not None :
			for name in regexps :
				self._nameMap[name] = {
					'regexp' : name,
					'replacement' : None
				}

	def transform(self, documentManager) :
		for name in self._nameMap :
			if self._nameMap[name]['replacement'] is None :
				self._nameMap[name]['replacement'] = util.getUniqueRandomSymbol()
		for document in documentManager.getDocumentList() :
			self.doReplaceDocument(document)
			if self._reportIfReplacedInString :
				self.doReportIfReplacedInString(document)

	def doReplaceDocument(self, document) :
		content = document.getContent()
		for name in self._nameMap :
			content = re.sub(self._nameMap[name]['regexp'], self._nameMap[name]['replacement'], content)
		document.setContent(content)

	def doReportIfReplacedInString(self, document) :
		fileName = document.getFileName()
		content = document.getContent()
		generator = tokenize.tokenize(io.BytesIO(content.encode('utf-8')).readline)
		for tokenType, tokenValue, start,  _, _ in generator:
			if tokenType == tokenize.STRING :
				for name in self._nameMap :
					if re.search(r'\b%s\b' % (self._nameMap[name]['replacement']), tokenValue) is not None :
						print(f"Warning: replaced in string. Symbol: {name}, file: {fileName}, line: {start[0]}")

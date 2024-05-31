from .internal import util

import re
import tokenize
import io

class Replacer :
	def __init__(self, symbols, reportIfReplacedInString = True) :
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

	def transform(self, documentManager) :
		for name in self._nameMap :
			if self._nameMap[name]['replacement'] is None :
				self._nameMap[name]['replacement'] = util.getUnusedRandomSymbol()
		for document in documentManager.getDocumentList() :
			self._doReplaceDocument(document)
			if self._reportIfReplacedInString :
				self._doReportIfReplacedInString(document)

	def _doReplaceDocument(self, document) :
		def callback(match) :
			symbol = match.group(0)
			if symbol in self._nameMap :
				return self._nameMap[symbol]['replacement']
			return symbol
		content = document.getContent()
		pattern = re.compile('\w+')
		content = pattern.sub(callback, content)
		document.setContent(content)

	def _doReportIfReplacedInString(self, document) :
		fileName = document.getFileName()
		content = document.getContent()
		generator = tokenize.tokenize(io.BytesIO(content.encode('utf-8')).readline)
		for tokenType, tokenValue, start,  _, _ in generator:
			if tokenType == tokenize.STRING :
				for name in self._nameMap :
					if self._nameMap[name]['replacement'] in tokenValue : # fast but inaccurate check
						if re.search(r'\b%s\b' % (self._nameMap[name]['replacement']), tokenValue) is not None : # slow but accurate check
							print(f"Warning: replaced in string. Symbol: {name}, file: {fileName}, line: {start[0]}")

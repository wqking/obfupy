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

from .internal import util
from .internal import callbackdata
from .internal import optionsutil

import copy
import re
import tokenize
import io

Options = optionsutil._createOptionsClass({
	'symbols' : {
		'default' : [],
		'doc' : """
A list or dict of symbols to replace.  
If it's a list, all items are strings, they are replaced with random generated names.  
If it's a dict, all keys are strings, they are replaced with the values in the dict. If any value is `None`, random generated name is used.  
The replacement is always case sensitive and whole word.  
Note: this option can't be set from within `callback`.
"""
	},
	'reportIfReplacedInString' : {
		'default' : True,
		'doc' : """
If it's `True`, Replace prints warning if any Python string is replaced. Usually we only want to replace class, function, or variable names,
if any string is replaced, that may be wrong.  
Note: this option can't be set from within `callback`.
"""
	},
})

class Replacer :
	def __init__(self, options, callback = None) :
		self._options = copy.deepcopy(options)
		self._callback = callback
		self._reportIfReplacedInString = options.reportIfReplacedInString
		self._nameMap = {}
		symbols = options.symbols
		if isinstance(symbols, list) :
			for name in symbols :
				self._nameMap[name] = {
					'replacement' : None
				}
		elif isinstance(symbols, dict) :
			for name in symbols :
				self._nameMap[name] = {
					'replacement' : symbols[name]
				}

	def transform(self, documentManager) :
		for name in self._nameMap :
			if self._nameMap[name]['replacement'] is None :
				self._nameMap[name]['replacement'] = util.getUnusedRandomSymbol()
		for document in documentManager.getDocumentList() :
			if callbackdata._shouldSkipFile(self._callback, document.getFileName()) :
				continue
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
		pattern = re.compile(r'\w+')
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

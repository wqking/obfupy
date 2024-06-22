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

import random
import base64

from .internal import util as util
from .internal import callbackdata

class CodecProvider :
	def __init__(
			self,
			encoder = lambda x : x,
			decoder = '%s',
			extraCode = None
		) :
		self._encoder = encoder
		self._decoder = decoder
		self._extraCode = extraCode

	def reset(self) :
		pass

	def encode(self, data) :
		return self._encoder(data)

	def getDecoder(self, variableName) :
		if callable(self._decoder) :
			return self._decoder(variableName)
		return self._decoder % (variableName)

	def getExtraCode(self, indent) :
		return self._extraCode

class Codec :
	def __init__(self, provider, callback = None) :
		self._provider = provider
		self._callback = callback

	def transform(self, documentManager) :
		for document in documentManager.getDocumentList() :
			if callbackdata._shouldSkipFile(self._callback, document.getFileName()) :
				continue
			self._doTransformDocument(document)

	def _doTransformDocument(self, document) :
		if hasattr(self._provider, 'reset') :
			self._provider.reset()
		content = document.getContent()
		data = bytearray(content, 'utf-8')
		data = self._provider.encode(data)
		
		encoded = base64.b64encode(data).decode('utf-8')

		indent = '\t' * random.randint(1, 10)
		variableName = util.getRandomSymbol()
		code = ''
		code += "import base64\n"
		extraCode = None
		if hasattr(self._provider, 'getExtraCode') :
			extraCode = self._provider.getExtraCode(indent)
		if extraCode is not None :
			code += f"{extraCode}\n"
		code += f"{variableName} = '{encoded}'\n"
		tempVariableName = util.getRandomSymbol()
		decoder = self._provider.getDecoder(tempVariableName)
		code += f"{tempVariableName} = bytearray(base64.b64decode({variableName}))\n"
		code += f"eval(compile({decoder},'<string>','exec'))\n"
		document.setContent(code)


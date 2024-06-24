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
import copy

from .internal import util as util
from .internal import callbackdata
from .internal import optionsutil

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

def _getDefaultCodecProvider() :
	import obfupy.transformers.utils.codecproviders as codecproviders
	return codecproviders.zip

Options = optionsutil._createOptionsClass({
	'provider' : {
		'default' : _getDefaultCodecProvider(),
		'defaultLiteral' : "codecproviders.zip",
		'doc' : """
A codec provider defined in module `obfupy.transformers.utils.codecproviders`.
"""
	},
})

class Codec :
	def __init__(self, options, callback = None) :
		self._options = copy.deepcopy(options)
		self._callback = callback

	def transform(self, documentManager) :
		for document in documentManager.getDocumentList() :
			options = callbackdata._invokeCallback(
				self._callback,
				callbackdata._OptionCallbackData(document.getFileName(), self._options)
			) or self._options
			if not options.enabled :
				continue
			self._doTransformDocument(document, options)

	def _doTransformDocument(self, document, options) :
		provider = options.provider
		if hasattr(provider, 'reset') :
			provider.reset()
		content = document.getContent()
		data = bytearray(content, 'utf-8')
		data = provider.encode(data)
		
		encoded = base64.b64encode(data).decode('utf-8')

		indent = '\t' * random.randint(1, 10)
		variableName = util.getRandomSymbol()
		code = ''
		code += "import base64\n"
		extraCode = None
		if hasattr(provider, 'getExtraCode') :
			extraCode = provider.getExtraCode(indent)
		if extraCode is not None :
			code += f"{extraCode}\n"
		code += f"{variableName} = '{encoded}'\n"
		tempVariableName = util.getRandomSymbol()
		decoder = provider.getDecoder(tempVariableName)
		code += f"{tempVariableName} = bytearray(base64.b64decode({variableName}))\n"
		code += f"eval(compile({decoder},'<string>','exec'))\n"
		document.setContent(code)


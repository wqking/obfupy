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

from .internal.iformatter import _IFormatter
from .internal import util
from .internal import optionsutil

import copy

Options = optionsutil._createOptionsClass({
	'removeComment' : {
		'default' : True,
		'doc' : "Remove comments. Note: if transformer Rewriter is used, comments are always removed.",
	},
	'expandIndent' : {
		'default' : True,
		'doc' : "Expand indent with large amount of spaces or tabs.",
	},
	'addExtraSpaces' : {
		'default' : True,
		'doc' : "Add large amount of spaces or tabs around operators.",
	},
	'addExtraNewLines' : {
		'default' : True,
		'doc' : "Add large amount of blank lines between code lines.",
	},
})

class Formatter :
	def __init__(self, options = None, callback = None) :
		if options is None :
			options = Options()
		self._options = copy.deepcopy(options)
		self._callback = callback

	def transform(self, documentManager) :
		_IFormatter(options = self._options, callback = self._callback).transform(documentManager)

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

from .utils import stringencoders
from .internal import util
from .internal import optionsutil

import copy

Options = optionsutil._createOptionsClass({
	'extractFunction' : {
		'default' : True,
		'doc' : "Take out the function (global or class member) body to a new random named function with random arguments, then make the original function calls the new function. The function won't be changed if obfupy determines it will cause error, such as `super` is used.",
		'problemSituations' : '',
	},
	'extractConstant' : {
		'default' : True,
		'doc' : "Replace constants with random named variables, the variables represent obfuscated constants.",
	},
	'extractBuiltinFunction' : {
		'default' : True,
		'doc' : "Replace built-in function names such as 'print', 'isinstance', with random named variables, the variables represent the functions.",
	},
	'renameLocalVariable' : {
		'default' : True,
		'doc' : "Rename function local variables with random names.",
	},
	'aliasFunctionArgument' : {
		'default' : True,
		'doc' : "If extractFunction is False or a function can't be extracted, obfupy can use random named variables as the argument names and replace all usage with the random names. Note the argument names are not renamed.",
	},
	'addNopControlFlow' : {
		'default' : True,
		'doc' : "Add useless and harmless code block around `for` and `while`.",
	},
	'reverseBoolOperator' : {
		'default' : True,
		'doc' : "Convert `a and b` to `not (not a or not b)`, etc",
	},
	'reverseCompareOperator' : {
		'default' : optionsutil._createOptionsObject({
			'wrapReversedCompareOperator' : {
				'default' : True,
				'doc' : "Convert `a < b` to a function `try: return not (a >= b) except: return a < b`, then if `a` doesn't support operator `>=`, it will fall back to `<`.",
			},
		}),
		'doc' : "Convert `a < b` to `not (a >= b)`"
	},
	'expandIfCondition' : {
		'default' : True,
		'doc' : ''
	},
	'rewriteIf' : {
		'default' : True,
		'doc' : ''
	},
	'removeDocString' : {
		'default' : True,
		'doc' : ''
	},
	'stringEncoders' : {
		'default' : stringencoders.defaultEncoders,
		'doc' : '',
		'defaultLiteral' : 'stringencoders.defaultEncoders',
	},
	'unrenamedVariableNames' : {
		'default' : None,
		'doc' : ''
	},
})

class Rewriter :
	def __init__(self, options = None, callback = None) :
		if options is None :
			options = Options()
		self._options = copy.deepcopy(options)
		self._callback = callback

	def transform(self, documentManager) :
		from .internal.irewriter import _IRewriter
		_IRewriter(options = self._options, callback = self._callback).transform(documentManager)

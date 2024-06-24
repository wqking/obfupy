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
		'doc' : """
Take out the function (global or class member) body to a new random named function with random arguments,
then make the original function calls the new function.
The function won't be changed if obfupy determines that may cause error, such as `super` is used.
""",
		'problemSituations' : "It doesn't work if the function frame object is accessed, such as using the frame object in `inspect` package.",
	},
	'extractConstant' : {
		'default' : True,
		'doc' : "Replace constants with random named variables, the variables represent obfuscated constants.",
	},
	'extractBuiltinFunction' : {
		'default' : True,
		'doc' : """
Replace built-in function names such as 'print', 'isinstance', with random named variables, the variables represent the functions.
""",
	},
	'renameLocalVariable' : {
		'default' : True,
		'doc' : "Rename function local variables with random names.",
	},
	'aliasFunctionArgument' : {
		'default' : True,
		'doc' : """
If `extractFunction` is False or the function can't be extracted, obfupy can use random named variables as the argument names
and replace all usage with the random names. Note the argument names are not renamed.
""",
		'problemSituations' : "It may not work if the function uses `locals()` or frame object to access the arguments by name.",
	},
	'addNopControlFlow' : {
		'default' : True,
		'doc' : "Add no-effect code block around `for` and `while`.",
	},
	'invertBoolOperator' : {
		'default' : True,
		'doc' : "Convert `a and b` to `not (not a or not b)`, etc",
	},
	'invertCompareOperator' : {
		'default' : optionsutil._createOptionsObject({
			'wrapInvertedCompareOperator' : {
				'default' : True,
				'doc' : """
Convert `a < b` to a function `try: return not (a >= b) except: return a < b`, so if `a` doesn't support operator `>=`,
it will fall back to `<`. This is useful if an object implements comparison operator such as '<' but doesn't implement
the inverted operator `>=`.
""",
			},
		}),
		'doc' : "Convert `a < b` to `not (a >= b)`.",
		'problemSituations' : """
It doesn't work if the comparison operator is not invertible, i.e, `(a < b) != not (a >= b)`. One case is `set`. For example,
```python
a = { 'a', 'b' }
b = { '1', '2' }
print(a < b) # False
print(a >= b) # False
```
"""
	},
	'expandIfCondition' : {
		'default' : True,
		'doc' : """
Insert no-effect conditions to `if` conditions. For example, `if a and b` to `if alwaysTrueExpression and a and alwaysTrueExpression and b`, etc.
This helps to hide the real condition.
"""
	},
	'rewriteIf' : {
		'default' : True,
		'doc' : """
Rewrite `if` statement to more `if` branches and obfuscate the control flow.
If `expandIfCondition` is enabled, then the inserted no-effect conditions become no-effect control flows,
that increases the obfuscating effect significantly. The option `invertCompareOperator` may help too.
"""
	},
	'removeDocString' : {
		'default' : True,
		'doc' : "Remove doc strings. Note the comments are always removed, there is no option to control it.",
		'problemSituations' : "This doesn't work if the source code uses the doc strings, e.g, by accessing `__doc__`."
	},
	'stringEncoders' : {
		'default' : stringencoders.defaultEncoders,
		'defaultLiteral' : 'stringencoders.defaultEncoders',
		'doc' : """
The list of encoders that's used to obfuscate strings. The default is `stringencoders.defaultEncoders`.
If `stringEncoders` is `None` or empty list, the strings are not obfuscated.  
Note strings are obfuscated only if `extractConstant` is `True`.  
Note: this option can't be set from within `callback`.
""",
	},
	'unrenamedVariableNames' : {
		'default' : None,
		'doc' : """
A list of variable names that will be kept unrenamed. If it's `None`, no variable names are kept.  
Note: this option can't be set from within `callback`.
""",
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

from .utils import stringencoders
from .internal import util
from .internal import optionsutil

import copy

Options = optionsutil._createOptionsClass({
	'extractFunction' : True,
	'extractConstant' : True,
	'extractBuiltinFunction' : True,
	'renameLocalVariable' : True,
	'aliasFunctionArgument' : True,
	'addNopControlFlow' : True,
	'reverseBoolOperator' : True,
	'reverseCompareOperator' : optionsutil._createOptionsObject({
		'wrapReversedCompareOperator' : True,
	}),
	'expandIfCondition' : True,
	'rewriteIf' : True,
	'removeDocString' : True,
	'stringEncoders' : stringencoders.defaultEncoders,
	'unrenamedVariableNames' : None,
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

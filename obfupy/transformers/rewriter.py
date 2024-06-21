from .utils import stringencoders
from .internal import util as util

import copy

class Options :
	def __init__(self) :
		self._modified = False
		self._data = {
			'_skip' : False,
			'extractFunction' : True,
			'extractConstant' : True,
			'extractBuiltinFunction' : True,
			'renameLocalVariable' : True,
			'aliasFunctionArgument' : True,
			'addNopControlFlow' : True,
			'reverseBoolOperator' : True,
			'allowReverseCompareOperator' : not True,
			'wrapReversedCompareOperator' : True,
			'expandIfCondition' : True,
			'rewriteIf' : True,
			'removeDocString' : True,
			'stringEncoders' : stringencoders.defaultEncoders,
			'unrenamedVariableNames' : None,
		}

	def _isModified(self) :
		return self._modified

	def _resetModified(self) :
		self._modified = False
util.addOptionPropertiesToClass(Options, Options()._data)

class Rewriter :
	def __init__(self, options = None, callback = None) :
		if options is None :
			options = Options()
		self._options = copy.deepcopy(options)
		self._callback = callback

	def transform(self, documentManager) :
		from .internal.irewriter import _IRewriter
		_IRewriter(options = self._options, callback = self._callback).transform(documentManager)

from .utils import stringencoders
from .internal import util as iutil

import enum

class OptionNames(str, enum.Enum) :
	extractFunction = 'extractFunction'
	extractConstant = 'extractConstant'
	extractBuiltinFunction = 'extractBuiltinFunction'
	renameLocalVariable = 'renameLocalVariable'
	addNopControlFlow = 'addNopControlFlow'
	reverseBoolOperator = 'reverseBoolOperator'
	wrapReversedCompareOperator = 'wrapReversedCompareOperator'
	expandIfCondition = 'expandIfCondition'
	rewriteIf = 'rewriteIf'
	stringEncoders = 'stringEncoders'

defaultOptions = {
	OptionNames.extractFunction : True,
	OptionNames.extractConstant : True,
	OptionNames.extractBuiltinFunction : True,
	OptionNames.renameLocalVariable : True,
	OptionNames.addNopControlFlow : True,
	OptionNames.reverseBoolOperator : True,
	OptionNames.wrapReversedCompareOperator : True,
	OptionNames.expandIfCondition : True,
	OptionNames.rewriteIf : True,
	OptionNames.stringEncoders : stringencoders.defaultEncoders
}

class Rewriter :
	def __init__(self, options = None, callback = None) :
		self._options = iutil.makeOptions(options, defaultOptions)
		self._callback = callback

	def transform(self, documentManager) :
		from .internal.irewriter import _IRewriter
		_IRewriter(options = self._options, callback = self._callback).transform(documentManager)

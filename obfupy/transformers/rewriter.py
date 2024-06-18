from .utils import stringencoders
from .internal import util as iutil

import enum

class OptionNames(str, enum.Enum) :
	extractFunction = 'extractFunction'
	extractConstant = 'extractConstant'
	extractBuiltinFunction = 'extractBuiltinFunction'
	renameLocalVariable = 'renameLocalVariable'
	aliasFunctionArgument = 'aliasFunctionArgument'
	addNopControlFlow = 'addNopControlFlow'
	reverseBoolOperator = 'reverseBoolOperator'
	allowReverseCompareOperator = 'allowReverseCompareOperator'
	wrapReversedCompareOperator = 'wrapReversedCompareOperator'
	expandIfCondition = 'expandIfCondition'
	rewriteIf = 'rewriteIf'
	removeDocString = 'removeDocString'
	stringEncoders = 'stringEncoders'
	unrenamedVariableNames = 'unrenamedVariableNames'

defaultOptions = {
	OptionNames.extractFunction : True,
	OptionNames.extractConstant : True,
	OptionNames.extractBuiltinFunction : True,
	OptionNames.renameLocalVariable : True,
	OptionNames.aliasFunctionArgument : True,
	OptionNames.addNopControlFlow : True,
	OptionNames.reverseBoolOperator : True,
	OptionNames.allowReverseCompareOperator : False,
	OptionNames.wrapReversedCompareOperator : True,
	OptionNames.expandIfCondition : True,
	OptionNames.rewriteIf : True,
	OptionNames.removeDocString : True,
	OptionNames.stringEncoders : stringencoders.defaultEncoders,
	OptionNames.unrenamedVariableNames : None,
}

class Rewriter :
	def __init__(self, options = None, callback = None) :
		self._options = iutil.makeOptions(options, defaultOptions)
		self._callback = callback

	def transform(self, documentManager) :
		from .internal.irewriter import _IRewriter
		_IRewriter(options = self._options, callback = self._callback).transform(documentManager)

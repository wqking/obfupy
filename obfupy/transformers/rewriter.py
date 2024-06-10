from .utils import stringencoders

import enum

class OptionNames(str, enum.Enum) :
	extractFunction = 'extractFunction'
	extractConstant = 'extractConstant'
	extractBuiltinFunction = 'extractBuiltinFunction'
	renameLocalVariable = 'renameLocalVariable'
	addNopControlFlow = 'addNopControlFlow'
	reverseIfElse = 'reverseIfElse'
	rewriteConditionalExpression = 'rewriteConditionalExpression'
	stringEncoders = 'stringEncoders'

defaultOptions = {
	OptionNames.extractFunction : True,
	OptionNames.extractConstant : True,
	OptionNames.extractBuiltinFunction : True,
	OptionNames.renameLocalVariable : True,
	OptionNames.addNopControlFlow : True,
	OptionNames.reverseIfElse : True,
	OptionNames.rewriteConditionalExpression : True,
	OptionNames.stringEncoders : stringencoders.defaultEncoders
}

class Rewriter :
	def __init__(self, options = None) :
		self._options = defaultOptions.copy()
		if options is not None :
			for name in options :
				assert name in defaultOptions
				self._options[name] = options[name]

	def transform(self, documentManager) :
		from .internal.irewriter import _IRewriter
		_IRewriter(self._options).transform(documentManager)

import testutil
import obfupy.transformers.internal.optionsutil as optionsutil
import obfupy.transformers.rewriter as rewriter

import copy

def test_rewriterOptions_basic() :
	options = rewriter.Options()
	assert options.extractFunction
	options.extractFunction = False
	assert not options.extractFunction

def test_rewriterOptions_cannotAddNewOption() :
	options = rewriter.Options()
	try :
		options.nonExistOkNotCrazy = 1
		assert False
	except AttributeError :
		assert True

def test_deepCopyOptions() :
	options = rewriter.Options()
	options.extractFunction = False
	newOptions = copy.deepcopy(options)
	assert not newOptions.extractFunction

def test_nestedOptions() :
	Options = optionsutil._createOptionsClass({
		'first' : 1,
		'nested' : optionsutil._createOptionsClass({
			'second' : 2
		})()
	})
	options = Options()
	assert options.first == 1
	assert options.nested
	options.nested = False
	assert not options.nested
	assert options.nested.second == 2
	options.nested.second = 3
	assert options.nested.second == 3
	newOptions = copy.deepcopy(options)
	assert not newOptions.nested

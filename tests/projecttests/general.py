import sys
sys.path.append("../../")
import os
import codecs

import helper

from obfupy.documentmanager import DocumentManager
from obfupy.document import Document
import obfupy.util as util
from obfupy.transformers.rewriter import Rewriter
import obfupy.transformers.rewriter as rewriter
from obfupy.transformers.formatter import Formatter
from obfupy.transformers.replacer import Replacer
from obfupy.transformers.codec import Codec
from obfupy.transformers.codec import CodecProvider
import obfupy.transformers.utils.codecproviders as codecproviders

def obfuscateProject(options = None, callback = None) :
	args = helper.parseCommandLine()
	input = args['input']
	output = args['output']
	print(input, '->', output)

	fileList = util.findFiles(input)
	fileList = util.ensureLinuxPath(fileList)
	fileList = list(filter(lambda s : 'error' not in s and '.tox' not in s and 'conftest' not in s, fileList))
	documentManager = DocumentManager()
	documentManager.addDocument(util.loadDocumentsFromFiles(fileList))

	allowRewrite = True
	rewriterOptions = {
		rewriter.OptionNames.extractFunction : True and allowRewrite,
		rewriter.OptionNames.extractConstant : True and allowRewrite,
		rewriter.OptionNames.extractBuiltinFunction : True and allowRewrite,
		rewriter.OptionNames.renameLocalVariable : True and allowRewrite,
		rewriter.OptionNames.aliasFunctionArgument : True and allowRewrite,
		rewriter.OptionNames.addNopControlFlow : True and allowRewrite,
		rewriter.OptionNames.reverseBoolOperator : True and allowRewrite,
		rewriter.OptionNames.expandIfCondition : True and allowRewrite,
		rewriter.OptionNames.rewriteIf : True and allowRewrite,
		rewriter.OptionNames.removeDocString : True and allowRewrite,
		rewriter.OptionNames.allowReverseCompareOperator : False and allowRewrite,
		rewriter.OptionNames.wrapReversedCompareOperator : True and allowRewrite,
	}
	if options is not None :
		for name in options :
			rewriterOptions[name] = options[name]
	Rewriter(options = rewriterOptions, callback = callback).transform(documentManager)
	#Formatter(addExtraSpaces = True, expandIndent = True).transform(documentManager)
	#provider = CodecProvider()
	#Codec(codecproviders.byteEncryption).transform(documentManager)
	#Codec(codecproviders.zip).transform(documentManager)
	#Codec(codecproviders.bz2).transform(documentManager)
	#Codec(codecproviders.base64).transform(documentManager)

	util.writeOutputFiles(documentManager, input, output)
	return args

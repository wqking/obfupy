import sys
try :
	import obfupy
	print("Using installed obfupy")
except :
	sys.path.append("../../")
	print("Using local obfupy")

import os
import codecs

import obfupy.documentmanager as documentmanager
import obfupy.util as util
import obfupy.transformers.rewriter as rewriter
import obfupy.transformers.formatter as formatter
import obfupy.transformers.replacer as replacer
import obfupy.transformers.codec as codec
import obfupy.transformers.utils.codecproviders as codecproviders
import obfupy.transformers.utils.stringencoders as stringencoders

import obfupy.transformers.internal.rewriter.truemaker as truemaker
import obfupy.transformers.internal.rewriter.nopmaker as nopmaker

from obfupy.document import Document
import ast

inputPath = 'input'
outputPath = 'output'
fileList = util.findFiles(inputPath)
fileList = util.ensureLinuxPath(fileList)
fileList = list(filter(lambda s : 'error' not in s and '.tox' not in s and 'conftest' not in s, fileList))
documentManager = documentmanager.DocumentManager()
documentManager.addDocument(util.loadDocumentsFromFiles(fileList))

rewriterOptions = rewriter.Options(extractConstant = False)
#rewriterOptions.extractConstant = True
rewriterOptions.invertCompareOperator.enabled = True
rewriterOptions.invertCompareOperator.wrapInvertedCompareOperator = True
#rewriterOptions.stringEncoders = None

def rewriterCallback(data) :
	if 'importa' in data.getFileName() and not data.isFile() :
		context = data.getContext()
		if context.isFunction() and context.getName() == 'toBeSkipped' :
			data.getOptions().enabled = False
def formatterCallback(data) :
	if 'importa' in data.getFileName() :
		data.getOptions().addExtraSpaces = False
		data.getOptions().expandIndent = False
replacerOptions = replacer.Options()
replacerOptions.symbols = [ 'makeMessage' ]
rewriter.Rewriter(options = rewriterOptions, callback = rewriterCallback).transform(documentManager)
#replacer.Replacer(options = replacerOptions).transform(documentManager)
#formatter.Formatter(callback = formatterCallback).transform(documentManager)
#codec.Codec(codec.Options(provider = codecproviders.byteEncryption)).transform(documentManager)

util.writeOutputFiles(documentManager, inputPath, outputPath)

os.chdir('output')
os.system('python -m pytest -s')

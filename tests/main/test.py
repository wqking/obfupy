import sys
try :
	import obfupy
	print("Using installed obfupy")
except :
	sys.path.append("../../")
	print("Using local obfupy")

import os
import codecs

from obfupy.documentmanager import DocumentManager
from obfupy.document import Document
import obfupy.util as util
import obfupy.transformers.rewriter as rewriter
import obfupy.transformers.formatter as formatter
import obfupy.transformers.replacer as replacer
import obfupy.transformers.codec as codec
import obfupy.transformers.utils.codecproviders as codecproviders

import obfupy.transformers.internal.rewriter.truemaker as truemaker
import obfupy.transformers.internal.rewriter.nopmaker as nopmaker
import ast

folders = [ 'input', 'output' ]

print(folders[0])
fileList = util.findFiles(folders[0])
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
	rewriter.OptionNames.allowReverseCompareOperator : True and allowRewrite,
	rewriter.OptionNames.reverseBoolOperator : True and allowRewrite,
	rewriter.OptionNames.expandIfCondition : True and allowRewrite,
	rewriter.OptionNames.rewriteIf : True and allowRewrite,
	rewriter.OptionNames.removeDocString : not True and allowRewrite,
	rewriter.OptionNames.wrapReversedCompareOperator : True and allowRewrite,
	rewriter.OptionNames.unrenamedVariableNames : [],
}
def rewriterCallback(data) :
	if 'importa' in data.getFileName() and not data.isFile() :
		context = data.getContext()
		if context.isFunction() and context.getName() == 'toBeSkipped' :
			data.skip()
def formatterCallback(data) :
	if 'importa' in data.getFileName() :
		data.setOption(formatter.OptionNames.addExtraSpaces, False)
rewriter.Rewriter(options = rewriterOptions, callback = rewriterCallback).transform(documentManager)
replacer.Replacer(symbols = [ 'n', 'makeMessage' ]).transform(documentManager)
formatter.Formatter(callback = formatterCallback).transform(documentManager)
codec.Codec(codecproviders.byteEncryption).transform(documentManager)
codec.Codec(codecproviders.zip).transform(documentManager)
codec.Codec(codecproviders.bz2).transform(documentManager)
codec.Codec(codecproviders.base64).transform(documentManager)

util.writeOutputFiles(documentManager, folders[0], folders[1])

os.chdir('output')
os.system('python -m pytest -s')


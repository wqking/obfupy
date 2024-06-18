import sys
sys.path.append("../../")
import os
import codecs

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
def callback(data) :
	if 'importa' in data.getFileName() and not data.isFile() :
		context = data.getContext()
		if context.isFunction() and context.getName() == 'testInnerWraps' :
			data.skip()
Rewriter(options = rewriterOptions, callback = callback).transform(documentManager)
#Replacer(symbols = [ 'n', 'makeMessage' ]).transform(documentManager)
#Formatter(addExtraSpaces = True, expandIndent = True).transform(documentManager)
provider = CodecProvider(encoder = lambda x : codecs.encode(x, 'zip'), decoder = "codecs.decode(%s, 'zip')", extraCode = 'import codecs')
#provider = CodecProvider()
#Codec(codecproviders.byteEncryption).transform(documentManager)
#Codec(codecproviders.zip).transform(documentManager)
#Codec(codecproviders.bz2).transform(documentManager)
#Codec(codecproviders.base64).transform(documentManager)

util.writeOutputFiles(documentManager, folders[0], folders[1])

os.chdir('output')
os.system('python -m pytest -s')

class Xxx :
	def __init__(self) :
		self._value = 5

	add = (lambda self, a : self._value + a)

def xxxprint(a) :
	#print(a)
	pass

xxxprint(ast.dump(ast.parse('''
''.join([chr(i ^ value) for i in data])
'''), indent=4))
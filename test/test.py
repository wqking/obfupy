import sys
sys.path.append("../")
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
#folders = [ '/source/python/nodezator', '/test' ]
#folders = [ '/source/python/django', '/test/django' ]
#folders = [ '/source/python/algorithms', '/test/algorithms' ]
#folders = [ '/source/python/flask', '/test/flask' ]

print(folders[0])
fileList = util.findFiles(folders[0])
fileList = list(filter(lambda s : 'error' not in s and '.tox' not in s and 'conftest' not in s, fileList))
documentManager = DocumentManager()
documentManager.addDocument(util.loadDocumentsFromFiles(fileList))

allowRewrite = True
rewriterOptions = {
	rewriter.OptionNames.extractFunction : True and allowRewrite,
	rewriter.OptionNames.extractConstant : True and allowRewrite,
	rewriter.OptionNames.extractBuiltinFunction : True and allowRewrite,
	rewriter.OptionNames.renameLocalVariable : True and allowRewrite,
	rewriter.OptionNames.addNopControlFlow : True and allowRewrite,
	rewriter.OptionNames.reverseBoolOperator : True and allowRewrite,
	rewriter.OptionNames.expandIfCondition : True and allowRewrite,
	rewriter.OptionNames.rewriteIf : True and allowRewrite,
	rewriter.OptionNames.wrapReversedCompareOperator : True and allowRewrite,
}
Rewriter(rewriterOptions).transform(documentManager)
#Replacer(symbols = [ 'n', 'makeMessage' ]).transform(documentManager)
#Formatter(addExtraSpaces = True, expandIndent = True).transform(documentManager)
provider = CodecProvider(encoder = lambda x : codecs.encode(x, 'zip'), decoder = "codecs.decode(%s, 'zip')", extraCode = 'import codecs')
#provider = CodecProvider()
#Codec(codecproviders.byteEncryption).transform(documentManager)
#Codec(codecproviders.zip).transform(documentManager)
#Codec(codecproviders.bz2).transform(documentManager)
#Codec(codecproviders.base64).transform(documentManager)

util.writeOutputFiles(documentManager, folders[0], folders[1])

for _ in range(0) :
	print(ast.unparse(truemaker.TrueMaker(nopmaker.NopMaker()).makeTrue(None, 1)))
	continue
	node = nopmaker.NopWithClass().getDefineNodes()[0]
	node = nopmaker.NopWithClass().makeReturnAsNode(ast.Constant(value = 5))
	node = ast.fix_missing_locations(node)
	print(ast.unparse(node))
	pass

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
b''.join([chr(i ^ value).encode('utf-8') for i in data ]).decode('utf-8')
'''), indent=4))

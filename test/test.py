import sys
sys.path.append("../")
import os
import codecs

from obfupy.documentmanager import DocumentManager
from obfupy.document import Document
import obfupy.util as util
from obfupy.transformers.rewriter import Rewriter
from obfupy.transformers.literal import Literal
from obfupy.transformers.replacer import Replacer
from obfupy.transformers.codec import Codec
from obfupy.transformers.codec import CodecProvider
import obfupy.transformers.codecproviders as codecproviders

import obfupy.transformers.internal.rewriter.logicmaker as logicmaker
import obfupy.transformers.internal.rewriter.nopmaker as nopmaker
import ast

folders = [ 'input', 'output' ]
#folders = [ '/source/python/nodezator', '/temp/test' ]

documentManager = DocumentManager()
documentManager.addDocument(util.loadDocumentsFromFiles(util.findFiles(folders[0])))

Rewriter(constantAsVariable = True).transform(documentManager)
#Replacer(symbols = [ 'n', 'makeMessage' ]).transform(documentManager)
#Literal(addExtraSpaces = True, expandIndent = True).transform(documentManager)
provider = CodecProvider(encoder = lambda x : codecs.encode(x, 'zip'), decoder = "codecs.decode(%s, 'zip')", extraCode = 'import codecs')
#provider = CodecProvider()
#Codec(codecproviders.zip).transform(documentManager)
#Codec(codecproviders.bz2).transform(documentManager)
#Codec(codecproviders.byteEncryption).transform(documentManager)

util.writeOutputFiles(documentManager, folders[0], folders[1])

for _ in range(0) :
	print(ast.unparse(logicmaker.LogicMaker(nopmaker.NopMaker()).makeTrue(None, 1)))
	continue
	node = nopmaker.NopWithClass().getDefineNodes()[0]
	node = nopmaker.NopWithClass().makeReturnAsNode(ast.Constant(value = 5))
	node = ast.fix_missing_locations(node)
	print(ast.unparse(node))
	pass

os.chdir('output')
os.system('python main.py')

def xxxprint(a) :
	#print(a)
	pass

xxxprint(ast.dump(ast.parse('''
a, b = (5, 6)
c = 6
'''), indent=4))

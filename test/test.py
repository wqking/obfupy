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

documentManager = DocumentManager()
documentManager.addDocument(util.loadDocumentsFromFiles(util.findFiles('input')))

Rewriter().transform(documentManager)
#Replacer(symbols = [ 'n', 'makeMessage' ]).transform(documentManager)
#Literal(addExtraSpaces = True, expandIndent = True).transform(documentManager)
provider = CodecProvider(encoder = lambda x : codecs.encode(x, 'zip'), decoder = "codecs.decode(%s, 'zip')", extraCode = 'import codecs')
#provider = CodecProvider()
#Codec(codecproviders.zip).transform(documentManager)
#Codec(codecproviders.bz2).transform(documentManager)
#Codec(codecproviders.byteEncryption).transform(documentManager)

util.writeOutputFiles(documentManager, 'input', 'output')

os.chdir('output')
os.system('python main.py')

def xxxprint(a) :
	#print(a)
	pass

import ast
xxxprint(ast.dump(ast.parse('''
if a :
	pass
elif b :
	pass
else :
	print(5)
	pass
'''), indent=4))

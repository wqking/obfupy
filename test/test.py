import sys
sys.path.append("../")
import os

from obfupy.documentmanager import DocumentManager
from obfupy.document import Document
import obfupy.util as util
from obfupy.transformers.encodebase64 import EncodeBase64
from obfupy.transformers.rewriter import Rewriter
from obfupy.transformers.literal import Literal
from obfupy.transformers.operator import Operator
from obfupy.transformers.replacer import Replacer

documentManager = DocumentManager()
documentManager.addDocument(util.loadDocumentsFromFiles(util.findFiles('input')))

#Rewriter().transform(documentManager)
Replacer(symbols = [ 'n' ]).transform(documentManager)
#Literal(addExtraSpaces = True, expandIndent = True).transform(documentManager)
#EncodeBase64().transform(documentManager)
#Operator().transform(documentManager)

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

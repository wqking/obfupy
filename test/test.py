import sys
sys.path.append("../")
import os

from obfupy.documentmanager import DocumentManager
from obfupy.document import Document
import obfupy.util as util
from obfupy.transformers.encodebase64 import EncodeBase64
from obfupy.transformers.renamer import Renamer
from obfupy.transformers.literal import Literal
from obfupy.transformers.operator import Operator

documentManager = DocumentManager()
documentManager.addDocument(util.loadDocumentsFromFiles(util.findFiles('input')))

Renamer().transform(documentManager)
#Literal(addExtraSpaces = True, expandIndent = not True).transform(documentManager)
#EncodeBase64().transform(documentManager)
#Operator().transform(documentManager)

util.writeOutputFiles(documentManager, 'input', 'output')

os.chdir('output')
os.system('python main.py')

def xxxprint(a) :
	pass
import ast
xxxprint(ast.dump(ast.parse('''
print("a")
self = None
self.a = 1
class X :
	@staticmethod
	def one() :
		return 1
	def two(self) :
		return 2
x = X()
x.two()
'''), indent=4))
print(ast.dump(ast.parse('''
print("Hello world, " + self.makeMessage(abc, x = "hi"))
'''), indent=4))

import sys
sys.path.append("../")
import os

from obfupy.documentmanager import DocumentManager
from obfupy.document import Document
import obfupy.util as util
from obfupy.transformers.encodebase64 import EncodeBase64
from obfupy.transformers.renamer import Renamer

documentManager = DocumentManager()
documentManager.addDocument(util.loadDocumentsFromFiles(util.findFiles('input')))

transformer = EncodeBase64()
transformer = Renamer()
transformer.transform(documentManager)

util.writeOutputFiles(documentManager, 'input', 'output')

os.chdir('output')
os.system('python main.py')

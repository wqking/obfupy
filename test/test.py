import sys
sys.path.append("../")

from obfupy.documentmanager import DocumentManager
from obfupy.document import Document
import obfupy.util as util
from obfupy.transformers.encodebase64 import EncodeBase64

documentManager = DocumentManager()
documentManager.addDocument(util.loadDocumentsFromFiles(util.findFiles('input')))

transformer = EncodeBase64()
transformer.transform(documentManager)

util.writeOutputFiles(documentManager, 'input', 'output')

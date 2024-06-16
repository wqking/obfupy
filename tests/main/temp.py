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

source = '''
def abc() :
	a = 1
	b = 5
	if a > 0 and b >= 5 :
		assert True
	else :
		assert False
		pass
abc()
'''

documentManager = DocumentManager()
document = Document()
document.setContent(source)
documentManager.addDocument(document)

allowRewrite = True
rewriterOptions = {
	rewriter.OptionNames.extractFunction : not True and allowRewrite,
	rewriter.OptionNames.extractConstant : True and allowRewrite,
	rewriter.OptionNames.extractBuiltinFunction : not True and allowRewrite,
	rewriter.OptionNames.renameLocalVariable : not True and allowRewrite,
	rewriter.OptionNames.addNopControlFlow : not True and allowRewrite,
	rewriter.OptionNames.reverseBoolOperator : not True and allowRewrite,
	rewriter.OptionNames.wrapReversedCompareOperator : not True and allowRewrite,
}
Rewriter(rewriterOptions).transform(documentManager)
#Replacer(symbols = [ 'n', 'makeMessage' ]).transform(documentManager)
#Literal(addExtraSpaces = True, expandIndent = True).transform(documentManager)
provider = CodecProvider(encoder = lambda x : codecs.encode(x, 'zip'), decoder = "codecs.decode(%s, 'zip')", extraCode = 'import codecs')
#provider = CodecProvider()
#Codec(codecproviders.byteEncryption).transform(documentManager)
#Codec(codecproviders.zip).transform(documentManager)
#Codec(codecproviders.bz2).transform(documentManager)
#Codec(codecproviders.base64).transform(documentManager)

print(documentManager.getDocumentList()[0].getContent())


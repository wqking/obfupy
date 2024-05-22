import base64

from .internal import util as util

template = '''
import base64
{name} = """{code}"""
eval(compile(base64.b64decode({name}),'<string>','exec'))
'''

class EncodeBase64 :
	def transform(self, documentManager) :
		for document in documentManager.getDocumentList() :
			self.doTransformDocument(document)

	def doTransformDocument(self, document) :
		content = document.getContent()
		encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
		newContent = template.format(
			name = util.getRandomSymbol(),
			code = encoded
		)
		document.setContent(newContent)

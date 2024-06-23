import sys
sys.path.append("../")
import obfupy.transformers.rewriter as rewriter
import obfupy.transformers.internal.optionsutil as optionsutil
import toolutil

titleTag = '###'

def makeQualifiedName(name, parentName) :
	if parentName is None :
		return name
	return parentName + '.' + name

def doDumpOptionsValue(name, defaultValue, docObj, parentName) :
	text = docObj
	defaultLiteral = str(defaultValue)
	if isinstance(docObj, dict) :
		text = docObj['doc']
		if 'defaultLiteral' in docObj :
			defaultLiteral = docObj['defaultLiteral']
	if name == 'enabled' and text == '' :
		text = """
Enable or disable all the options.
"""
	text = text.strip()
	result = ''
	qualifiedName = makeQualifiedName(name, parentName)
	if isinstance(defaultValue, optionsutil._BaseOptions) :
		result += '%s %s = sub options\n' % (titleTag, qualifiedName)
		result += text + '\n'
		result += doDumpOptionsDoc(defaultValue, qualifiedName)
		return result
	result += '%s %s = %s\n' % (titleTag, qualifiedName, defaultLiteral)
	result += text + '\n'
	if len(text) > 0 :
		result += '\n'
	return result

def doDumpOptionsDoc(optionsClass, parentName = None) :
	dataMap = optionsClass._fullData
	nameList = []
	for name in dataMap :
		if name == 'enabled' :
			nameList.insert(0, name)
		else :
			nameList.append(name)

	result = ''
	for name in nameList :
		obj = dataMap[name]
		defaultValue = obj
		doc = ''
		if isinstance(obj, tuple) :
			defaultValue = obj[0]
			if len(obj) > 1 :
				doc = obj[1]
		elif isinstance(obj, dict) :
			defaultValue = obj['default']
			doc = obj
		result += doDumpOptionsValue(name, defaultValue, doc, parentName)
	return result

def dumpOptionsDoc(options) :
	return doDumpOptionsDoc(options)

tag = '<!--auto generated section-->'
rewriterMd = '../doc/transformer_rewriter.md'
text = dumpOptionsDoc(rewriter.Options)
toolutil.replaceSectionInFile(rewriterMd, text, tag)
#print(text)

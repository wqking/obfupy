import sys
sys.path.append("../")
import obfupy.transformers.rewriter as rewriter
import obfupy.transformers.internal.optionsutil as optionsutil
import toolutil

def makeQualifiedName(name, parentName) :
	if parentName is None :
		return name
	return parentName + '.' + name

def doDumpOptionsValue(name, value, doc, parentName) :
	text = doc
	defaultValue = str(value)
	if isinstance(doc, dict) :
		text = doc['doc']
		if 'defaultLiteral' in doc :
			defaultValue = doc['defaultLiteral']
	result = ''
	qualifiedName = makeQualifiedName(name, parentName)
	if isinstance(value, optionsutil._BaseOptions) :
		result += '#### %s = sub options\n' % (qualifiedName)
		result += text + '\n'
		result += doDumpOptionsDoc(value, qualifiedName)
		return result
	result += '#### %s = %s\n' % (qualifiedName, defaultValue)
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
		value = obj
		doc = ''
		if isinstance(obj, tuple) :
			value = obj[0]
			if len(obj) > 1 :
				doc = obj[1]
		elif isinstance(obj, dict) :
			value = obj['default']
			doc = obj
		result += doDumpOptionsValue(name, value, doc, parentName)
	return result

def dumpOptionsDoc(options) :
	return doDumpOptionsDoc(options)

tag = '<!--auto generated section-->'
rewriterMd = '../doc/transformer_rewriter.md'
text = dumpOptionsDoc(rewriter.Options)
toolutil.replaceSectionInFile(rewriterMd, text, tag)
#print(text)

import obfupy.transformers.internal.optionsutil as optionsutil

titleTag = '###'

def makeQualifiedName(name, parentName) :
	if parentName is None :
		return name
	return parentName + '.' + name

def doDumpOptionsValue(name, defaultValue, docObj, parentName) :
	text = docObj
	problemSituations = None
	defaultLiteral = str(defaultValue)
	if isinstance(docObj, dict) :
		text = docObj['doc']
		if 'defaultLiteral' in docObj :
			defaultLiteral = docObj['defaultLiteral']
		if 'problemSituations' in docObj :
			problemSituations = docObj['problemSituations']
	if name == 'enabled' and text == '' :
		text = """
Enable or disable all the options.
"""
	text = text.strip()
	if problemSituations is not None :
		if not isinstance(problemSituations, list) :
			problemSituations = [ problemSituations ]
		text += "  \n"
		text += "\n"
		for item in problemSituations :
			text += "**Problem situation:** %s\n" % (item.strip())
	result = ''
	qualifiedName = makeQualifiedName(name, parentName)
	if isinstance(defaultValue, optionsutil._BaseOptions) :
		result += '%s %s = sub options\n' % (titleTag, qualifiedName)
		result += text + '\n'
		result += doDumpOptionsDoc(defaultValue, qualifiedName)
		return result
	result += '%s %s = %s\n' % (titleTag, qualifiedName, defaultLiteral)
	#print('options.%s = %s' % (qualifiedName, defaultLiteral))
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


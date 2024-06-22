def replaceSectionInFile(fileName, text, beginTag, endTag = None) :
	if endTag is None :
		endTag = beginTag
	inputLineList = []
	with open(fileName, 'r') as f :
		inputLineList = f.read().split('\n')
	lineList = []
	inSection = False
	for line in inputLineList :
		if inSection :
			if line.strip() == endTag :
				inSection = False
				lineList.append(line)
		else :
			lineList.append(line)
			if line.strip() == beginTag :
				inSection = True
				lineList = lineList + text.split('\n')
	content = '\n'.join(lineList)
	with open(fileName, 'w') as f :
		f.write(content)

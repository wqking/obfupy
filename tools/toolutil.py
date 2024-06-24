def readTextFile(fileName) :
	with open(fileName, 'r') as file :
		return file.read()

def writeTextFile(fileName, content) :
	with open(fileName, 'w') as file :
		file.write(content)

def replaceSectionInFile(fileName, text, beginTag, endTag = None) :
	if endTag is None :
		endTag = beginTag
	inputLineList = readTextFile(fileName).split('\n')
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
	writeTextFile(fileName, content)

def tabToSpaceInCode(fileName) :
	inputLineList = readTextFile(fileName).split('\n')
	lineList = []
	inCode = False
	for line in inputLineList :
		isCodeTag = line.startswith('```')
		if inCode :
			if isCodeTag :
				inCode = False
			else :
				line = line.replace("\t", "    ")
		else :
			if isCodeTag :
				inCode = True
		lineList.append(line)
	content = '\n'.join(lineList)
	writeTextFile(fileName, content)

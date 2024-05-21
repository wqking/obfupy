from . import document

import codecs
import os
import pathlib

def writeTextFile(fileName, content) :
	file = codecs.open(fileName, "w", "utf-8")
	file.write(str(content))
	file.close()

def writeOutputFiles(documentManager, basePath, outputPath) :
	for document in documentManager.getDocumentList() :
		inputFileName = document.getFileName()
		relativePath = os.path.relpath(inputFileName, basePath)
		outputFileName = os.path.join(outputPath, relativePath)
		path = os.path.dirname(outputFileName)
		if not os.path.exists(path) :
			os.makedirs(path)
		writeTextFile(outputFileName, document.getContent())

def loadDocumentsFromFiles(fileNameList) :
	if not isinstance(fileNameList, list) :
		fileNameList = [ fileNameList ]
	result = []
	for fileName in fileNameList :
		result.append(document.Document().loadFromFile(fileName))
	return result

def findFiles(path, recursive = True) :
	pattern = '*.py'
	p = pathlib.Path(path)
	fileList = None
	if recursive :
		fileList = list(p.rglob(pattern))
	else :
		fileList = list(p.glob(pattern))
	result = []
	for file in fileList :
		result.append(str(file))
	return result

from . import document

import codecs
import os
import pathlib
import ast
import re

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

def findFiles(path, pattern = '*.py', recursive = True) :
	p = pathlib.Path(path)
	fileList = None
	if recursive :
		fileList = list(p.rglob(pattern))
	else :
		fileList = list(p.glob(pattern))
	return [ str(file.resolve()) for file in fileList ]

def ensureLinuxPath(path) :
	def convert(p) :
		return str(pathlib.PurePosixPath(pathlib.PureWindowsPath(p)))

	if isinstance(path, list) :
		return [ convert(p) for p in path ]
	else :
		return convert(path)

def listSymbols(documentManager, regexps = None) :
	classNameSet = {}
	functionNameSet = {}
	otherNameSet = {}
	for document in documentManager.getDocumentList() :
		content = document.getContent()
		parsedAst = ast.parse(content)
		for node in ast.walk(parsedAst) :
			if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef) :
				functionNameSet[node.name] = True
			if isinstance(node, ast.ClassDef) :
				classNameSet[node.name] = True
		if regexps is not None :
			for regexp in regexps :
				foundList = re.findall(regexp, content)
				for name in foundList :
					otherNameSet[name] = True
	return {
		'class' : list(classNameSet.keys()),
		'function' : list(functionNameSet.keys()),
		'other' : list(otherNameSet.keys())
	}

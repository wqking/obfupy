# obfupy library
#
# Copyright (C) 2024 Wang Qi (wqking)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from . import document
from .transformers.internal import util as iutil

import codecs
import os
import pathlib
import ast
import re

def readTextFile(fileName) :
	with codecs.open(fileName, 'r', 'utf-8') as file :
		return file.read()

def writeTextFile(fileName, content) :
	with codecs.open(fileName, "w", "utf-8") as file :
		file.write(str(content))

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

randomSymbolGenerator111 = iutil.randomSymbolGenerator111
randomSymbolGenerator000 = iutil.randomSymbolGenerator000
randomSymbolGeneratorUnicode = iutil.randomSymbolGeneratorUnicode

setRandomSymbolGenerator = iutil.setRandomSymbolGenerator

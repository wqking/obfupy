import sys
import os
scriptPath = os.path.dirname(__file__)
try :
	import obfupy
	print("Using installed obfupy")
except :
	sys.path.append(os.path.join(scriptPath, "../../"))
	print("Using local obfupy")

import obfupy.util as util
import obfupy.document as document
import obfupy.documentmanager as documentmanager
import obfupy.transformers.rewriter as rewriter

from timeit import default_timer as timer
import ast

options3 = rewriter.Options()
options3.addNopControlFlow = False

options4 = rewriter.Options()
options4.addNopControlFlow = False
options4.expandIfCondition = False

rewriterOptionsList = [
	{
		'options' : None,
		'message' : 'No obfuscated',
	},
	{
		'options' : rewriter.Options(),
		'message' : 'All features are enabled',
		'outputPath' : 'allenabled',
	},
	{
		'options' : options3,
		'message' : 'addNopControlFlow = False',
		'outputPath' : 'options3',
	},
	{
		'options' : options4,
		'message' : 'addNopControlFlow = False, expandIfCondition = False',
		'outputPath' : 'options4',
	},
]

def formatDuration(seconds) :
	return "%05f" % (seconds)

class Benchmark :
	def __init__(self) :
		self._inputPath = os.path.join(scriptPath, 'input')
		self._outputPath = os.path.join(scriptPath, 'output')

	def run(self) :
		inputFileList = util.findFiles(self._inputPath)
		for fileName in inputFileList :
			self._doBenchmark(fileName)

	def _doBenchmark(self, fileName) :
		doc = document.Document()
		doc.loadFromFile(fileName)
		sourceCode = doc.getContent()
		functionList = self._loadAllBenchmarkFunctions(sourceCode)
		for optionsItem in rewriterOptionsList :
			code = sourceCode
			if 'options' not in optionsItem :
				continue
			options = optionsItem['options']
			message = optionsItem['message']
			print(message)
			if options is not None :
				documentManager = documentmanager.DocumentManager()
				doc.setContent(sourceCode)
				documentManager.addDocument(doc)
				rewriter.Rewriter(options = options).transform(documentManager)
				code = doc.getContent()
				if 'outputPath' in optionsItem :
					util.writeOutputFiles(documentManager, self._inputPath, os.path.join(self._outputPath, optionsItem['outputPath']))
			globalContext = { 'timer' : timer }
			exec(code, globalContext)
			for functionName in functionList :
				result = self._doBenchmarkFunction(functionName, globalContext)
				print(functionName, formatDuration(result))
			print("")
	
	def _doBenchmarkFunction(self, functionName, globalContext) :
		code = f'''
start = timer()
for _ in range(1000 * 100) :
	{functionName}()
_currentBenchmarkResult = timer() - start
'''
		exec(code, globalContext)
		return globalContext['_currentBenchmarkResult']

	def _loadAllBenchmarkFunctions(self, sourceCode) :
		result = []
		for node in ast.walk(ast.parse(sourceCode)) :
			if isinstance(node, ast.FunctionDef) and node.name.startswith('benchmark_') :
				result.append(node.name)
		return result

Benchmark().run()

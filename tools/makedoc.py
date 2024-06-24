import sys
import os
scriptPath = os.path.dirname(__file__)
sys.path.append(os.path.join(scriptPath, "../"))

import dumpoptionsdoc
import toolutil

import obfupy.transformers.rewriter as rewriter
import obfupy.transformers.formatter as formatter
import obfupy.transformers.replacer as replacer
import obfupy.transformers.codec as codec

tag = '<!--auto generated section-->'

def processOptionsSections() :
	optionMdMap = [
		{
			'mdFileName' : os.path.join(scriptPath, '../doc/transformer_rewriter.md'),
			'optionClass' : rewriter.Options,
		},
		{
			'mdFileName' : os.path.join(scriptPath, '../doc/transformer_formatter.md'),
			'optionClass' : formatter.Options,
		},
		{
			'mdFileName' : os.path.join(scriptPath, '../doc/transformer_replacer.md'),
			'optionClass' : replacer.Options,
		},
		{
			'mdFileName' : os.path.join(scriptPath, '../doc/transformer_codec.md'),
			'optionClass' : codec.Options,
		},
	]
	for item in optionMdMap :
		text = dumpoptionsdoc.dumpOptionsDoc(item['optionClass'])
		toolutil.replaceSectionInFile(item['mdFileName'], text, tag)

def processScaffolding() :
	srcFileName = os.path.join(scriptPath, '../examples/scaffolding.py')
	docFileName = os.path.join(scriptPath, '../doc/scaffolding.md')
	text = """
```python
%s
```
""" % (toolutil.readTextFile(srcFileName))
	toolutil.replaceSectionInFile(docFileName, text, tag)

def doMain() :
	processOptionsSections()
	processScaffolding()

doMain()

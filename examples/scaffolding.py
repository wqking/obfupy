import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import obfupy.documentmanager as documentmanager
import obfupy.util as util
import obfupy.transformers.rewriter as rewriter
import obfupy.transformers.formatter as formatter
import obfupy.transformers.replacer as replacer
import obfupy.transformers.codec as codec
import obfupy.transformers.utils.codecproviders as codecproviders
import obfupy.transformers.utils.stringencoders as stringencoders

# Get the input/output path from command line.
# You may hardcode the input/output path for your projects.
if len(sys.argv) != 3 :
	print("Usage: python examples/scaffolding.py input_path output_path")
	sys.exit(1)
inputPath = sys.argv[1]
outputPath = sys.argv[2]

################################################################################
########## First step, prepare DocumentManager
################################################################################

# Search all .py files in input folder, recursively.
fileList = util.findFiles(inputPath)
# Ensure all path delimiters are / instead of \ if on Windows. This is not necessary
# but it's easier to check folder in callback.
fileList = util.ensureLinuxPath(fileList)
documentManager = documentmanager.DocumentManager()
# Load documents from the files and pass them to DocumentManager
documentManager.addDocument(util.loadDocumentsFromFiles(fileList))

################################################################################
########## Transformer Rewriter
################################################################################

# Following are the options for Rewriter. It sets the values ​​with default values.
# You don't need to set default values for your project. If all options ​​are default values,
# just pass `None` to the parameter `options` in Rewriter constructor.
rewriterOptions = rewriter.Options()
rewriterOptions.enabled = True
rewriterOptions.extractFunction = True
rewriterOptions.extractConstant = True
rewriterOptions.extractBuiltinFunction = True
rewriterOptions.renameLocalVariable = True
rewriterOptions.aliasFunctionArgument = True
rewriterOptions.addNopControlFlow = True
rewriterOptions.invertBoolOperator = True
rewriterOptions.invertCompareOperator.enabled = True
rewriterOptions.invertCompareOperator.wrapInvertedCompareOperator = True
rewriterOptions.expandIfCondition = True
rewriterOptions.rewriteIf = True
rewriterOptions.removeDocString = True
rewriterOptions.stringEncoders = stringencoders.defaultEncoders
rewriterOptions.preservedNames = None

# This is the callback function passed to the Rewriter. It demonstrates how to use callbacks.
# If you don't need the callback, just pass `None` to argument `callback` in Rewriter constructor.
def rewriterCallback(callbackData) :
	if 'the_file_name_to_skip' in callbackData.getFileName() :
		callbackData.getOptions().enabled = False
		return
	if not callbackData.isFile() :
		context = callbackData.getContext()
		if context.isFunction() :
			if context.getName() == 'functionNotToBeObfuscated' :
				callbackData.getOptions().enabled = False
			if context.getName() == 'functionNotToRewriteIf' :
				callbackData.getOptions().rewriteIf = False

# Performing transformations using Rewriter
rewriter.Rewriter(options = rewriterOptions, callback = rewriterCallback).transform(documentManager)

################################################################################
########## Transformer Formatter
################################################################################

formatterOptions = formatter.Options()
formatterOptions.enabled = True
formatterOptions.removeComment = True
formatterOptions.expandIndent = True
formatterOptions.addExtraSpaces = True
formatterOptions.addExtraNewLines = True

formatter.Formatter(options = formatterOptions, callback = None).transform(documentManager)

################################################################################
########## Transformer Replacer
################################################################################

replacerOptions = replacer.Options()
replacerOptions.symbols = [ 'theFuncNameToReplace', 'theClassNameToReplace' ]
replacerOptions.reportIfReplacedInString = True

replacer.Replacer(options = replacerOptions, callback = None).transform(documentManager)

################################################################################
########## Transformer Codec
################################################################################

codecOptions = codec.Options()
codecOptions.provider = codecproviders.zip

# The callback demonstrates how to use random codec provider for each source file
def codecCallback(callbackData) :
	providerList = [ codecproviders.zip, codecproviders.bz2, codecproviders.byteEncryption, codecproviders.base64 ]
	import random
	callbackData.getOptions().provider = random.choice(providerList)

codec.Codec(options = codecOptions, callback = codecCallback).transform(documentManager)

################################################################################
########## Last step, save the obfuscated files.
################################################################################

util.writeOutputFiles(documentManager, inputPath, outputPath)

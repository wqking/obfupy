# obfupy -- Python source code obfuscator aiming to produce correct and functional code

obfupy is a Python 3 library that can obfuscate entire Python 3 projects, transforming source code into obfuscated and difficult-to-understand code.
obfupy aims to produce correct and functional code. Several non-trivial real-world projects were tested using obfupy,
such as Flask, Nodezator, Algorithms collection, and Django (not all features are enabled for Django).

obfupy helps closed source projects to protect the code and intellectual property. You may not need it in your open source projects.  

You use this project at your own risk. If you use it to obfuscate malicious code, you bear all consequences of your malicious code. This project is not associated with any malicious code.

## Facts and features

- **Obfuscation methods**
  - Rewrite the "if" conditional to include many confusing branches.
  - Rename local variable names.
  - Extract the function and have the original function call the extracted function, then rename the parameters in the extracted function.
  - Create alias for function arguments.
  - Obfuscate numeric and string constants and replace them with random variable names.
  - Replace built-in function names (e.g. "print") with random variable names.
  - Add useless control flow to `for` and `while`.
  - Remove doc strings.
  - Remove comments.
  - Add extra spaces around operators.
  - Make indents larger to make it harder to read.
  - Add extra blank lines between code lines.
  - Encode the whole Python source file with base64, zip, bz2, byte obfuscator, and easy to add your own codec.
- **Customizable**
  - There are multiple layers of independent transformers. You can choose which transformers to use and which not to use.
  - The non-trivial transformers such as Rewriter, Formatter, support comprehensive options to enable/disable features. If any feature doesn't work well for your project, you can just disable it.
- **Well tested**
  - There are tests that cover all features.
  - Tested with several real world non-trivial projects such as Flask, Nodezator, Algorithms collection, and Django.

## License

Apache License, Version 2.0  

## Version 0.1.0

## Source code

[https://github.com/wqking/obfupy](https://github.com/wqking/obfupy)

## Dependencies

obfupy requires Python 3.9 or later, it doesn't have any other dependencies.

## Install

**Install from pip package**  
`pip install obfupy`

**Install from source code**  
Clone obfupy repository, change directory to the root of obfupy, then,  
`pip install -e .`

**Use from source code without installation**  
Clone obfupy repository, add following lines in the beginning of your script,  
```
import sys
sys.path.append(PATH_TO_OBFUPY)
```

## Quick start

If you want to see how the obfuscated code looks, please check [the obfuscated eventqueue.obfuscated.py](https://github.com/wqking/obfupy/blob/master/examples/eventqueue.obfuscated.py), and [the orginal eventqueue.py](https://github.com/wqking/obfupy/blob/master/examples/eventqueue.py). The source file is taken from my `eventpy` library.

A typical Python script using obfupy looks like,   

```python
import obfupy.documentmanager as documentmanager
import obfupy.util as util
import obfupy.transformers.rewriter as rewriter
import obfupy.transformers.formatter as formatter

inputPath = PATH_TO_THE_SOURCE_CODE
outputPath = PATH_TO_OUTPUT

# Prepare source code files as DocumentManager
fileList = util.findFiles(inputPath)
documentManager = documentmanager.DocumentManager()
documentManager.addDocument(util.loadDocumentsFromFiles(fileList))

# Transform the source code with various transformers

# Transformer Rewriter
rewriter.Rewriter().transform(documentManager)
# Transformer Formatter
formatter.Formatter().transform(documentManager)
# There are other transformers

# Write the obfuscated code to outputPath
util.writeOutputFiles(documentManager, inputPath, outputPath)
```

## Documentations

* [Get started -- the scaffolding script](doc/scaffolding.md)
* [Document and DocumentManager - the input source for transformers](doc/documentmanager.md)
* [Transformers overview](doc/transformer_overview.md)
* [Options and callback](doc/options_and_callback.md)
* [Transformer Rewriter -- rewrite the Python code in different structure](doc/transformer_rewriter.md)
* [Transformer Formatter -- change the code visual layout](doc/transformer_formatter.md)
* [Transformer Replacer -- replace symbols literally](doc/transformer_replacer.md)
* [Transformer Codec -- encode the whole Python source file](doc/transformer_codec.md)
* [Utilities](doc/util.md)
* [How obfupy is tested with real world projects](doc/real_world_projects.md)
* [Infrequently Asked Questions](doc/faq.md)

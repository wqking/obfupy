# Document and DocumentManager

obfupy uses class Document and DocumentManager to encapsulate Python source code files. The transformers only work on DocumentManager.  

## Class DocumentManager

### Import

```python
from obfupy.documentmanager import DocumentManager
```

### Member functions

#### addDocument(document)

Add `document` to DocumentManager. `document` can an instance of `Document` or a list of `Document`.

#### getDocumentList()

Returns a list of `Document`. This is used by transformers.

## Class Document

### Import

```python
from obfupy.document import Document
```

### Member functions

#### loadFromFile(fileName)

Load source file from `fileName`. `Document` always open the file as utf-8 encoding.

#### getFileName()

Returns the file name as `str`, or empty string '' if no file is loaded.

#### getContent()

Returns the loaded source code as `str`.  
This is usually used by transformers.

#### setContent(content)

Replaces the loaded source code with `content` which is a `str`. The new content is stored in memory, not written to any file.  
This is usually used by transformers.

## Use the utility function to ease the document management

There are some useful functions in [obfupy.util](util.md) that can help to load and save the document. Here is the example on how to do it.  

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

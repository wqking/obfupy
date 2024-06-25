# Utility functions

## Import

```python
import obfupy.util as util
```

## Functions

#### readTextFile(fileName)

Reads from the file `fileName` and returns the entire contents as a string.

#### writeTextFile(fileName, content)

Writes `content` as a string to the file `fileName`, encoded in 'utf-8'.

#### writeOutputFiles(documentManager, basePath, outputPath)

Writes all files in `documentManager` to folder `outputPath`. `documentManager` is an instance of `DocumentManager`.  
The subfolder structure is constructed from `basePath` and the document file name. For example, if the files in `documentManager` are loaded from folder '/project/mytest/', `basePath` should be set to '/project/mytest/'. The file '/project/mytest/src/whatever/main.py' will be written to 'outputPath/src/whatever/main.py'.

#### loadDocumentsFromFiles(fileNameList)

Loads `Document`s from each file name in `fileNameList`. `fileNameList` is a list of file names.  
The function returns a list of `Document` objects. The returned value can be passed to `DocumentManager.addDocument()`.

#### findFiles(path, pattern = '*.py', recursive = True)

Finds all files in `path` of `pattern`. `path` is a string. If `recursive` is True, all sub folders in `path` will be searched.  
The function returns a list of file names. File names have full absolute path.

#### ensureLinuxPath(path)

Ensures that the path delimiter in `path` is '/', even on Windows. `path` is a string or a list of strings.  
If `path` is a string, the function returns the string of the new path; if `path` is a list, the function returns a list of strings.
Note that on Windows, the driver delimiter is still '\', but the path separator will be '/', for example 'c:\/project/whatever/another'.
This function can be used to normalize paths and make it easier to check if a path contains subfolders,
for example, we can check for `'/whatever/' in path' on any platform.

#### listSymbols(documentManager, regexps = None)

Returns all class names, functions names, and any text matching any item in regexps, in `documentManager`.  
`regexps` is either `None` or a list of regular expressions.  
The function scans all document in `documentManager`, collects all class names, function names, and any text matching `regexps`.  
The function returns a dictionary,  
```python
{
    'class' : list of class names,
    'function' : list of function names,
    'other' : list of texts matching regexps
}
```
The use case of this function is to collect symbols to use transformer Replacer to replace them.

#### setRandomSymbolGenerator(generator)

Sets the generator function for random symbol. The function is used by all transformers. The word 'generator' is not related to Python generator. When possible, obfupy tries to limit the symbol length to 8 characters. Longer symbols may only increase file size and don't help with obfuscating.  
There are several built-in generators,  

`util.randomSymbolGenerator111` : Generate symbols with characters I, l, and 1. This is the default generator. Examples: I1lllll1, llllI1lI.  
`util.randomSymbolGenerator000` : Generate symbols with characters O, o, and 0. Examples: ooOO0OO0, O0O0oO00.  
`util.randomSymbolGeneratorUnicode` : Generate symbols with non-English Unicode characters. Examples: 𢺐齍嬱𗱯𡪲𤥳𛂮雩, 𧓢ᗰ䮝𢔻𘒤𥤏𡄑𥮮.  

**Provide your own symbol generator**  
The generator is a function of prototype `someGenerator(length)`. `length` is a positive integer of the expected length of the generated symbol. The function can choose not to respect `length` and use any length it likes. The function must return a string value. The string must be a valid Python identifier, that's to say, `string.isidentifier()` must be True.

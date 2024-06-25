# Transformer Formatter

Transformer Formatter changes the code visual layout, it doesn't change the code structure.  
Formatter makes it's difficult for human-beings to read the obfuscated code, but it's very easy to deobfuscate the code by a simple tool
or even a regular expression replace in the code editor.

## Features

- Remove comments.
- Add extra spaces around operators.
- Make indents larger to make it harder to read.
- Add extra blank lines between code lines.

## Import

```python
import obfupy.transformers.formatter as formatter
```

There are two classes, `formatter.Formatter` is the transformer, `formatter.Options` is the options class.

## Constructor

```python
Formatter(options = None, callback = None)
```

Formatter constructor accept `options` and `callback`. For basic usage of `options` and `callback`, [please read here](options_and_callback.md).  

## Formatter options

`options` argument is an object of `formatter.Options`. All its attributes are various of options.

<!--auto generated section-->
### enabled = True
Enable or disable all the options.

### removeComment = True
Remove comments. Note: if transformer Rewriter is used, comments are always removed.

### expandIndent = True
Expand indent with large amount of spaces or tabs.

### addExtraSpaces = True
Add large amount of spaces or tabs around operators.

### addExtraNewLines = True
Add large amount of blank lines between code lines.


<!--auto generated section-->


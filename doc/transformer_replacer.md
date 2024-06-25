# Transformer Replacer

Transformer Replacer replaces symbols provided by the user with random names literally.  

## Features

- Replace symbols in all source files.
- Warning if any symbol is replaced within Python strings.

## Import

```python
import obfupy.transformers.replacer as replacer
```

There are two classes, `replacer.Replacer` is the transformer, `replacer.Options` is the options class.

## Constructor

```python
Replacer(options, callback = None)
```

Replacer constructor accept `options` and `callback`. For basic usage of `options` and `callback`, [please read here](options_and_callback.md).  

## Replacer options

`options` argument is an object of `replacer.Options`. All its attributes are various of options.

<!--auto generated section-->
### enabled = True
Enable or disable all the options.

### symbols = []
A list or dict of symbols to replace.  
If it's a list, all items are strings, they are replaced with random generated names.  
If it's a dict, all keys are strings, they are replaced with the values in the dict. If any value is `None`, random generated name is used.  
The replacement is always case sensitive and whole word.  
Note: this option can't be set from within `callback`.

### reportIfReplacedInString = True
If it's `True`, Replace prints warning if any Python string is replaced. Usually we only want to replace class, function, or variable names,
if any string is replaced, that may be wrong.  
Note: this option can't be set from within `callback`.


<!--auto generated section-->

## Use Replacer efficiently

Replacer is the simplest transformer. If used properly, it can also be the most powerful and very reliable. Here is a suggested approach for effectively using Replacer in a semi-automated form, step by step.  

Step 1, prepare two text files (or tables in database). One named "rename" that contains symbols to be renamed, another named "preserve" that contains symbols that will be preserved.  

Step 2, write a tool to find all symbols that can probably be replaced in your projects. This can be done by either using `util.listSymbols` or write your own algorithm. The symbols can be whatever you need, such as class names, function names, or special argument/variable names such as _xxx.  
The tool will then filter out all the symbols in the two text files from step 1, and the remaining symbols will be the newly found ones.

Step 3, developers watch for new symbols and place them into appropriate text files to rename or preserve them.  

Step 4, in the obfuscating script, it reads symbols from "rename" text file and feed them to Replacer.

Done

Only Step 3 involves manual operation, and only the initial creation of the database requires a lot of work. Subsequent work is incremental and small.
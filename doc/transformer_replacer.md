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


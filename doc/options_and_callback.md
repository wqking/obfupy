# Options and callback in transformers

All transformers constructor accepts argument `callback`, and some customizable transformers also accepts argument `options`. The argument `options` sets the default options for the whole project to be obfuscated. Argument `callback` is a function that will be called by the transformer. The callback function can change the options for each source file, or even for each function or class in transformer Rewriter.

## Options

`Options` is an object. Each transformer has its own `Options` class. An option is a property of the `Options` object, the value can be True/False, string, integer, or another `Options` (a.k.a, sub options).  
Every `Options` has a property named `enabled`, setting it to `False` will disable all options in the `Options` object.  
All options can be set as properties of `Options`. All simple options, except sub options, can be passed to `Options` constructor as keyword arguments.  

Let's take transformer Rewriter as an example,

```python
import obfupy.transformers.rewriter as rewriter

# Create an instance of rewriter.Options
rewriterOptions = rewriter.Options()

# Set extractConstant to False to disable it
rewriterOptions.extractConstant = False

# We can also pass extractConstant to the constructor, for example,
# rewriterOptions = rewriter.Options(extractConstant = False)

# Enable the sub option invertCompareOperator
rewriterOptions.invertCompareOperator.enabled = True
# But disable invertCompareOperator.wrapInvertedCompareOperator
rewriterOptions.invertCompareOperator.wrapInvertedCompareOperator = False

# Pass the options to Rewriter and transform the documents
rewriter.Rewriter(options = rewriterOptions).transform(documentManager)
```

## Callback

All transformers constructor accepts argument `callback`. `callback` is a function that will be called at certain time point by the transformer. The callback function can change the options for each source file, or even for each function or class in transformer Rewriter.  

### callback prototype

```python
def callback(callbackData)
```

The callback receives one argument `callbackData`. `callbackData` is an object. All transformers supports the same basic `callbackData`, and some transformers such as Rewriter may extend `callbackData`.

### callbackData member function

All transformers support `callbackData` with below member functions

#### isFile()

Returns `True` if current processing context is file. It always returns `True` for most transformers. In transformer Rewriter it may return `False` if the processing context is class or function.

#### getFileName()

Returns the full file name of the current source code file being processed. This function is always valid no matter `isFile()` returns `True` or `False`.

#### getOptions()

Returns the options object. There is always an options object in the callback data, even if the transformer doesn't have options argument in its constructor. The options object has at least one property `enabled`, set it to `False` will skip further transforming.

## Example

Below code demonstrate how to skip all files in folder 'template'.

```python
import obfupy.transformers.formatter as formatter

def callback(callbackData) :
    if '/template/' in callbackData.getFileName() :
        callbackData.getOptions().enabled = False

formatter.Formatter(callback = callback).transform(documentManager)
```

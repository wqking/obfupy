- [Transformer Rewriter](#transformer-rewriter)
	- [Features](#features)
	- [Import](#import)
	- [Constructor](#constructor)
	- [Rewriter options](#rewriter-options)
		- [enabled = True](#enabled--true)
		- [extractFunction = True](#extractfunction--true)
		- [extractConstant = True](#extractconstant--true)
		- [extractBuiltinFunction = True](#extractbuiltinfunction--true)
		- [renameLocalVariable = True](#renamelocalvariable--true)
		- [aliasFunctionArgument = True](#aliasfunctionargument--true)
		- [addNopControlFlow = True](#addnopcontrolflow--true)
		- [invertBoolOperator = True](#invertbooloperator--true)
		- [invertCompareOperator = sub options](#invertcompareoperator--sub-options)
		- [invertCompareOperator.enabled = True](#invertcompareoperatorenabled--true)
		- [invertCompareOperator.wrapInvertedCompareOperator = True](#invertcompareoperatorwrapinvertedcompareoperator--true)
		- [expandIfCondition = True](#expandifcondition--true)
		- [rewriteIf = True](#rewriteif--true)
		- [removeDocString = True](#removedocstring--true)
		- [stringEncoders = stringencoders.defaultEncoders](#stringencoders--stringencodersdefaultencoders)
		- [preservedNames = None](#preservednames--none)
	- [Callback](#callback)
		- [callbackData member functions](#callbackdata-member-functions)
			- [getContext()](#getcontext)
		- [Context](#context)
			- [isFile()](#isfile)
			- [getFileName()](#getfilename)
			- [getOptions()](#getoptions)
			- [isModule()](#ismodule)
			- [isClass()](#isclass)
			- [isFunction()](#isfunction)
			- [getName()](#getname)
			- [getParent()](#getparent)
	- [String encoders](#string-encoders)
		- [Import](#import-1)
		- [Encoders](#encoders)
			- [reverse](#reverse)
			- [rot13](#rot13)
			- [hex](#hex)
			- [xor](#xor)
		- [defaultEncoders](#defaultencoders)

# Transformer Rewriter

Rewriter is the core and most useful transformer. Rewriter rewrites Python code into a different structure.  

## Features

- Rewrite the "if" conditional to include many confusing branches.
- Rename local variable names.
- Extract the function and have the original function call the extracted function, then rename the parameters in the extracted function.
- Create alias for function arguments.
- Obfuscate numeric and string constants and replace them with random variable names.
- Replace built-in function names (e.g. "print") with random variable names.
- Add useless control flow to `for` and `while`.
- Remove doc strings.

## Import

```python
import obfupy.transformers.rewriter as rewriter
```

There are two classes, `rewriter.Rewriter` is the transformer, `rewriter.Options` is the options class.

## Constructor

```python
Rewriter(options = None, callback = None)
```

Rewriter constructor accepts `options` and `callback`. For basic usage of `options` and `callback`, [please read here](options_and_callback.md).  

## Rewriter options

`options` argument is an object of `rewriter.Options`. All its attributes are various of options.

<!--auto generated section-->
### enabled = True
Enable or disable all the options.

### extractFunction = True
Take the body of a function (global or class member) and put it into a randomly named new function with random arguments,
and then have the original function call the new function.
If obfupy determines that this might cause an error, such as using `super`, the function will not be changed.  

**Problem situation:** It doesn't work if the function frame object is accessed, e.g, using the frame object in `inspect` package.


### extractConstant = True
Replace constants with randomly named variables that represent obfuscated constants.

### extractBuiltinFunction = True
Replace built-in function names (e.g., "print", "isinstance") with randomly named variables that represent the functions.

### renameLocalVariable = True
Rename function local variables with random names.  
Note only variables inside function are renamed, the variables in global scope are not renamed.

### aliasFunctionArgument = True
If `extractFunction` is `False` or the function cannot be extracted, obfupy can use randomly named variables as parameter names
and replace all usages with the random names. Note that parameter names are not renamed.  

**Problem situation:** It may not work if the function uses `locals()` or frame object to access the arguments by name.


### addNopControlFlow = True
Add no-effect code block around `for` and `while`.

### invertBoolOperator = True
Convert `a and b` to `not (not a or not b)`, etc

### invertCompareOperator = sub options
Convert `a < b` to `not (a >= b)`.  

**Problem situation:** It doesn't work if the comparison operator is not invertible, i.e, `(a < b) != not (a >= b)`. One case is `set`. For example,
```python
a = { 'a', 'b' }
b = { '1', '2' }
print(a < b) # False
print(a >= b) # False
```

### invertCompareOperator.enabled = True
Enable or disable all the options.

### invertCompareOperator.wrapInvertedCompareOperator = True
Convert `a < b` to a function `try: return not (a >= b) except: return a < b`, so if `a` doesn't support operator `>=`,
it will fall back to `<`. This is useful if an object implements comparison operator such as '<' but doesn't implement
the inverted operator `>=`.

### expandIfCondition = True
Insert no-effect conditions to `if` conditions. For example, `if a and b` to `if alwaysTrueExpression and a and alwaysTrueExpression and b`, etc.
This helps to hide the real condition.

### rewriteIf = True
Rewrite `if` statement to more `if` branches and obfuscate the control flow.
If `expandIfCondition` is enabled, then the inserted no-effect conditions become no-effect control flows,
that increases the obfuscating effect significantly. The option `invertCompareOperator` may help too.

### removeDocString = True
Remove doc strings. Note the comments are always removed, there is no option to control it.  

**Problem situation:** This doesn't work if the source code uses the doc strings, e.g, by accessing `__doc__`.


### stringEncoders = stringencoders.defaultEncoders
The list of encoders that's used to obfuscate strings. The default is `stringencoders.defaultEncoders`.
If `stringEncoders` is `None` or empty list, the strings are not obfuscated.  
Note: strings are obfuscated only if `extractConstant` is `True`.  
Note: this option can't be set from within `callback`.

### preservedNames = None
A list of symbol names that will be preserved and not renamed. If it's `None`, no symbol names are preserved.  
Note: this option can't be set from within `callback`.


<!--auto generated section-->



## Callback

The `callback` parameter in the Rewriter constructor is a function that will be called by the transformer at a specific point in time. The callback function can change options per source file, or per class, per function.

```python
def callback(callbackData)
```

### callbackData member functions

`callbackData` supports all member function in [basic callbackData](options_and_callback.md). Besides that, `callbackData` also extends with more functions.

#### getContext()

If processing is within a module, class or function, returns the current context object. If processing is within a file, returns None (callbackData.isFile() returns True).

### Context

The context object describes the current context of the transformation.  
The context has the following member functions.

#### isFile()

Returns `True` if a file is being processed, in which case `getContext()` returns `None`.  
If `isFile()` returns `False`, `getContext()` returns the context.

#### getFileName()

Returns the full file name of the source code file currently being processed. This function works regardless of whether `isFile()` returns `True` or `False`.

#### getOptions()

Returns an options object. The user can change the options on the object to change the behavior. Changing options only affects the current context and all inner (i.e. child) contexts, not other contexts. See the documentation for `getParent()` for example code.

#### isModule()

Returns `True` if the current context is processing a Python module. A Python module is simply a Python source file.  
Note that in obfupy, `module` (where `callbackData.isFile()` is `False` and `callbackData.getContext().isModule()` is `True`) is different from `file` (where `callbackData.isFile()` is `True` and `callbackData.getContext()` is `None`). When it is in `file`, the Python code has not been parsed yet, so the code may contain syntax errors. When it is in `module`, the Python code has been parsed, so the code needs to be legal Python code and cannot contain any syntax errors otherwise it throws exception and the processing will stop.

#### isClass()

Returns `True` if current context is processing a class.

#### isFunction()

Returns `True` if current context is processing a function or lambda.

#### getName()

Returns the name related to the context.  
If the context is module, it returns the source file name (with full path).  
If the context is class, it returns the class name.  
If the context is function, it returns the function name. However, if the context is lambda, the name is always '#lambda'.  

#### getParent()

Returns the parent context. The parent context is the outer context. Module is the outermost context, its parent is `None`.  
For example,

```python
class MyClass :
    def myFunc(self) :
        def inner() :
            pass
        pass

class AnotherClass :
    pass
```

Parent context of `inner` is `myFunc`. Parent of `myFunc` is `MyClass`. Parent of `MyClass` is the module. The module's parent is `None`.  
Parent context of `AnotherClass` is the module.  
If the `callback` function changes the options when `getContext()` is the context of `MyClass`, then the changes affect `myFunc` and `inner`, but not `AnotherClass` or the module.

## String encoders

Rewriter uses string encoders to obfuscate strings. There are several built-in encoders.

### Import

```python
import obfupy.transformers.utils.stringencoders as stringencoders
```

### Encoders

#### reverse

Convert "abcdef" to "fedcba".

#### rot13

Use 'rot13' encoding from Python `codecs` package.

#### hex

Use 'hex' encoding from Python `codecs` package.

#### xor

Replace each bytes `ch` in the string with `ch xor randomInteger`.

### defaultEncoders

```python
stringencoders.defaultEncoders = [
    reverse,
    rot13,
    hex,
    xor
]
```

This is the default value of Rewriter option `stringEncoders`.

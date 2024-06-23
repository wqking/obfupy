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
		- [unrenamedVariableNames = None](#unrenamedvariablenames--none)
	- [Callback](#callback)
		- [Member functions](#member-functions)
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

Rewriter is the core and most useful transformer. Rewriter rewrites Python code into different structure.  

## Features

- Rewrite `if` condition with many confusing branches.
- Rename local variable names.
- Extract function and make original function call the extracted one, then rename the arguments in the extracted function.
- Make alias for function arguments.
- Obfuscate number and string constants and replace them with random variable names.
- Replace built-in function names such as `print` with random variable names.
- Add no-effect control flows to `for` and `while`.
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

Rewriter constructor accept `options` and `callback`. For basic usage of `options` and `callback`, [please read here](options_and_callback.md).  

## Rewriter options

`options` argument is an object of `rewriter.Options`. All its attributes are various of options.

<!--auto generated section-->
### enabled = True
Enable or disable all the options.

### extractFunction = True
Take out the function (global or class member) body to a new random named function with random arguments,
then make the original function calls the new function.
The function won't be changed if obfupy determines that may cause error, such as `super` is used.

### extractConstant = True
Replace constants with random named variables, the variables represent obfuscated constants.

### extractBuiltinFunction = True
Replace built-in function names such as 'print', 'isinstance', with random named variables, the variables represent the functions.

### renameLocalVariable = True
Rename function local variables with random names.

### aliasFunctionArgument = True
If `extractFunction` is False or the function can't be extracted, obfupy can use random named variables as the argument names
and replace all usage with the random names. Note the argument names are not renamed.

### addNopControlFlow = True
Add no-effect code block around `for` and `while`.

### invertBoolOperator = True
Convert `a and b` to `not (not a or not b)`, etc

### invertCompareOperator = sub options
Convert `a < b` to `not (a >= b)`.
### invertCompareOperator.enabled = True
Enable or disable all the options.

### invertCompareOperator.wrapInvertedCompareOperator = True
Convert `a < b` to a function `try: return not (a >= b) except: return a < b`, so if `a` doesn't support operator `>=`,
it will fall back to `<`.

### expandIfCondition = True
Insert no-effect conditions to `if` conditions. For example, `if a and b` to `if alwaysTrueExpression and a and alwaysTrueExpression and b`, etc.
This helps to hide the real condition.

### rewriteIf = True
Rewrite `if` statement to more `if` branches and obfuscate the control flow.
If `expandIfCondition` is enabled, then the inserted no-effect conditions become no-effect control flows,
that increases the obfuscating effect significantly. The option `invertCompareOperator` may help too.

### removeDocString = True
Remove doc strings. Note the comments are always removed, there is no option to control it.

### stringEncoders = stringencoders.defaultEncoders
The list of encoders that's used to obfuscate strings. The default is `stringencoders.defaultEncoders`.
If `stringEncoders` is `None` or empty list, the strings are not obfuscated.  
Note strings are obfuscated only if `extractConstant` is `True`.  
This option can't be set in the `callback`.

### unrenamedVariableNames = None
A list of variable names that will be kept unrenamed. If it's `None`, no variable names are kept.  
This option can't be set in the `callback`.


<!--auto generated section-->



## Callback

The argument `callback` in Rewriter constructor is a function that will be called at certain time point by the transformer. The callback function can change the options for each source file, each function, or each class.  

```python
def callback(callbackData)
```

### Member functions

`callbackData` supports all member function in [basic callbackData](options_and_callback.md). Beside that, `callbackData` also extends with more functions.

#### getContext()

Returns current context object if the processing within module, class, or function. `None` if it's within the file (`callbackData.isFile()` returns `True`).

### Context

The context object describes the current context of the transforming.
Context has below member functions.

#### isFile()

Returns `True` if it's processing file, in such case `getContext()` returns `None`.  
If `isFile()` returns `False`, then `getContext()` returns the context.

#### getFileName()

Returns the full file name of the current source code file being processed. This function is always valid no matter `isFile()` returns `True` or `False`.

#### getOptions()

Returns the options object. The user can change the options on the object to change the behavior. Changing the options only affects current context and all inner (i.e, child) context, it doesn't affect the other contexts. See the document of `getParent()` for the example code.

#### isModule()

Returns `True` if current content is processing a Python module. A Python module is just a Python source file.  
Note in obfupy `module` (where `callbackData.isFile()` is `False` and `callbackData.getContext().isModule()` is `True`) is different with `file` (where `callbackData.isFile()` is `True` and `callbackData.getContext()` is `None`). When it's in `file`, the Python code is not parsed yet, so the code can contain syntax error. When it's in `module`, the Python code is already parsed so the code requires to be legal Python code and can't contain any syntax error.

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

Convert "abc" to "cba".

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

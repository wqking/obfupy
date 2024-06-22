# Transformer Rewriter

Rewriter is the most useful transformer that rewrite Python code into different structure.  

## Features:

- Rewrite `if` condition with many confusing branches.
- Rename local variable names.
- Extract function and make original function call the extracted one, then rename the arguments in the extracted function.
- Make alias for function arguments.
- Obfuscate number and string constants and replace them with random variable names.
- Replace built-in function names such as `print` with random variable names.
- Add useless control flow to `for`, `while`, and `if`.
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

`options` argument is an object or `rewriter.Options`. All its attributes are various of options.

<!--auto generated section-->
#### enabled = True

#### extractFunction = True
Take out the function (global or class member) body to a new random named function with random arguments, then make the original function calls the new function. The function won't be changed if obfupy determines it will cause error, such as `super` is used.

#### extractConstant = True
Replace constants with random named variables, the variables represent obfuscated constants.

#### extractBuiltinFunction = True
Replace built-in function names such as 'print', 'isinstance', with random named variables, the variables represent the functions.

#### renameLocalVariable = True
Rename function local variables with random names.

#### aliasFunctionArgument = True
If extractFunction is False or a function can't be extracted, obfupy can use random named variables as the argument names and replace all usage with the random names. Note the argument names are not renamed.

#### addNopControlFlow = True
Add useless and harmless code block around `for` and `while`.

#### reverseBoolOperator = True
Convert `a and b` to `not (not a or not b)`, etc

#### reverseCompareOperator = sub options
Convert `a < b` to `not (a >= b)`
#### reverseCompareOperator.enabled = True

#### reverseCompareOperator.wrapReversedCompareOperator = True
Convert `a < b` to a function `try: return not (a >= b) except: return a < b`, then if `a` doesn't support operator `>=`, it will fall back to `<`.

#### expandIfCondition = True

#### rewriteIf = True

#### removeDocString = True

#### stringEncoders = stringencoders.defaultEncoders

#### unrenamedVariableNames = None


<!--auto generated section-->




# How obfupy is tested with real world projects

obfupy is not an academic project. obfupy is designed to generate correct and usable code for real-world projects. As such, several non-trivial real-world projects are tested using obfupy.

Only the transformer Rewriter is tested with these projects. The other transformers are simpler and do not need to be tested with them.

If a project uses pytest for unit test and there is a file `conftest.py`, then `conftest.py` is not obfuscated because it exposes functions for the whole tests and can't be obfuscated.

## Tested projects

### Flask

https://github.com/pallets/flask.git

All features in obfupy are enabled, all .py code are obfuscated.  
All unit tests in Flask succeed.

### Nodezator

https://github.com/IndiePython/nodezator.git

All features in obfupy are enabled, all .py code are obfuscated.  
The software can be launched and operated successfully.

### Pythonic Data Structures and Algorithms

https://github.com/keon/algorithms.git

All features in obfupy are enabled, all .py code are obfuscated.  
All unit tests in Flask succeed.

### Django

https://github.com/django/django.git

Following features (options) are disabled,  
`extractFunction`: Django uses inspect package to get local variable, extractFunction won't work for all functions.  
`extractBuiltinFunction`: Django uses the built-in function names as variable and function names.  
`aliasFunctionArgument`: Due to usage of inspect package.  
`removeDocString`: Django code accesses doc string thus it can't be removed.  
`invertCompareOperator`: Some comparison is not invertible such as `<` with set operands.  
`rewriteIf`: enabled by default, but disabled for class body, because some classes inherits from enum.Enum and have if condition in class body, if we rewrite the `if` condition, the newly generated assignment will cause enum.Enum throw exceptions.  

Almost all .py files in both Django source folder and tests folder are obfuscated, only small parts are left untouched, such as test data, templates, etc.  
Almost all unit tests succeed. Only several test folders fail, either due to they don't work well on my Windows with Chinese code page (gbk encode error) which is not related to the obfuscator, or some due to the usage of inspect package.  
It's possible to enable above disabled options for most code and only disable them for problematic code, however it will be very time-consuming. The goal to test with Django is to verify obfuscate works, not to make Django maximally obfuscated.

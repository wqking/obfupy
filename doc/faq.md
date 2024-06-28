# Infrequently Asked Questions

## General

### The transformer doesn't print any progress, how can I know the processing progress?

We can use the callback to print the file name currently being processed. For example,

```python
def callback(callbackData) :
    if callbackData.isFile() : 
        print(callbackData.getFileName())

rewriter.Rewriter(callback = callback).transform(documentManager)
```

By counting the number of documents in the `DocumentManager` we can also display the progress as a percentage.

## Transformer Rewriter

### Why can't Rewriter rename class, function, and argument names?

Due to the dynamic nature of Python, it is impossible to generate 100% correct code if we rename the class and function names.
For example, in following code,  

```python
class MyClass :
    def myFunc(self) :
        pass

def anotherFunc(obj) :
    obj.myFunc()
```

In the global function `anotherFunc` , calling `obj.myFunc()` can call functions in `MyClass` or call unobfuscated functions in third-party libraries, in which case renaming `myFunc` may cause a runtime error.

For function argument, it's possible to rename the positional arguments, and avoid renaming any arguments used as keyword, that sounds work. But one case is impossible to work properly, that is, use dictionary as keyword arguments. Example code,  

```python
def func(a, b) :
    pass

args = { "a": 1, "b" : 2 }
func(**args)
```

If we rename arguments `a` and `b`, calling `func` will cause error.

### But I want to rename class and function, can I?

Yes, just use transformer Replacer.

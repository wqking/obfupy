# Transformers overview

A transformer is a class to obfuscate the Python code in a certain way. Transformers are orthogonal, a transformer doesn't depend on other transformer. Multiple transformers can be used to obfuscate the same Python code base. In theory the order of transformers doesn't matter, but if transformer `Rewriter` is used after `Codec`, then not many things can be really rewritten.

## Only one public member function

```python
transform(documentManager)
```

Each transformer only supports one public member function `transform(documentManager)`. The transformer will transform all documents in `documentManager` and store the obfuscated code back to `documentManager`. The function doesn't return anything.  

## The suggested transformers order

Though transformers are orthogonal, to obtain the best result, the transformers should be performed in certain order. The order should be,  
Rewriter, Replacer, Formatter, Codec

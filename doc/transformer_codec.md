# Transformer Codec

Transformer Codec encodes the whole Python source file with base64, zip, bz2, or byte obfuscator.  

## Features

- Several built-in encoders.
- Easy to provide user defined encoders.

## Import

```python
import obfupy.transformers.codec as codec
```

There are two classes, `codec.Codec` is the transformer, `codec.Options` is the options class.

## Constructor

```python
Codec(options, callback = None)
```

Codec constructor accept `options` and `callback`. For basic usage of `options` and `callback`, [please read here](options_and_callback.md).  

## Codec options

`options` argument is an object of `codec.Options`. All its attributes are various of options.

<!--auto generated section-->
### enabled = True
Enable or disable all the options.

### provider = codecproviders.zip
A codec provider defined in module `obfupy.transformers.utils.codecproviders`.


<!--auto generated section-->

## Codec providers

Codec uses codec providers to encode/decode the source file. There are several built-in providers.

### Import

```python
import obfupy.transformers.utils.codecproviders as codecproviders
```

### Providers

#### base64

Encode the source file as base64.

#### zip

Compress the source file with zip then encode it as base64.

#### bz2

Compress the source file with bz2 then encode it as base64.

#### byteEncryption

Encrypt the source file with random byte algorithm then encode it as base64.

## Problem situations

If the source code uses functions that relies on the existence of source file, Codec won't work, and the encoded source file will cause error.  
For example, Python `inspect.getsource()` function will report errors if it's obfuscated with Codec.
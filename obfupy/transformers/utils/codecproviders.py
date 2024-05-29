from .. import codec
from ..internal import byteencryptioncodec

import codecs

base64 = codec.CodecProvider()
zip = codec.CodecProvider(encoder = lambda x : codecs.encode(x, 'zip'), decoder = "codecs.decode(%s, 'zip')", extraCode = 'import codecs')
bz2 = codec.CodecProvider(encoder = lambda x : codecs.encode(x, 'bz2'), decoder = "codecs.decode(%s, 'bz2')", extraCode = 'import codecs')
byteEncryption = byteencryptioncodec.ByteEncryptionCodec()

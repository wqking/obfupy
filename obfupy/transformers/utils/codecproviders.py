# obfupy library
#
# Copyright (C) 2024 Wang Qi (wqking)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .. import codec
from ..internal import byteencryptioncodec

import codecs

base64 = codec.CodecProvider()
zip = codec.CodecProvider(encoder = lambda x : codecs.encode(x, 'zip'), decoder = "codecs.decode(%s, 'zip')", extraCode = 'import codecs')
bz2 = codec.CodecProvider(encoder = lambda x : codecs.encode(x, 'bz2'), decoder = "codecs.decode(%s, 'bz2')", extraCode = 'import codecs')
byteEncryption = byteencryptioncodec.ByteEncryptionCodec()

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

from . import util

import random

class ByteEncryptionCodec :
	def __init__(self) :
		pass

	def reset(self) :
		self._operatorCount = len(operatorConfigList)
		self._operatorList = [] + operatorConfigList
		while len(self._operatorList) > self._operatorCount :
			self._operatorList.pop()
		while len(self._operatorList) < self._operatorCount :
			self._operatorList.append(random.choice(operatorConfigList))
		random.shuffle(self._operatorList)

		self._keyList = []
		while len(self._keyList) < self._operatorCount :
			keyRange = (1, 255)
			k = len(self._keyList)
			if 'keyRange' in self._operatorList[k] :
				keyRange = self._operatorList[k]['keyRange']
			self._keyList.append(random.randint(keyRange[0], keyRange[1]))

		self._decoderName = util.getUnusedRandomSymbol()

	def encode(self, data) :
		for i in range(len(data)) :
			for k in range(self._operatorCount - 1, -1, -1) :
				data[i] = self._operatorList[k]['encode'](data[i], self._keyList[k])
		return data

	def getDecoder(self, variableName) :
		return f'{self._decoderName}({variableName})'

	def getExtraCode(self, indent) :
		dataName = 'data'
		decoderCode = ''
		decoderCode += f"def {self._decoderName}({dataName}) :\n"
		decoderCode += f"{indent}for i in range(len({dataName})) :\n"
		for k in range(self._operatorCount) :
			decoderCode += f"{indent}{indent}{dataName}[i] = " + self._operatorList[k]['decode'].format(
				data = f"{dataName}[i]",
				key = self._keyList[k],
				keyMinus8 = 8 - self._keyList[k],
			) + "\n"
		decoderCode += f"{indent}return {dataName}\n"
		return decoderCode

def xor(data, key) :
	return data ^ key

def add(data, key) :
	return (data + key) % 256

def sub(data, key) :
	return (data - key) % 256

def ror(data, key) :
	return ((data >> key) | (data << (8 - key))) & 0xff

def rol(data, key) :
	return ((data << key) | (data >> (8 - key))) & 0xff

def bitNot(data, key) :
	return (~data) & 0xff

operatorConfigList = [
	{
		'encode' : xor,
		'decode' : '{data} ^ {key}',
	},

	{
		'encode' : add,
		'decode' : '({data} - {key}) % 256',
	},

	{
		'encode' : sub,
		'decode' : '({data} + {key}) % 256',
	},

	{
		'encode' : ror,
		'decode' : '(({data} << {key}) | ({data} >> {keyMinus8})) & 0xff',
		'keyRange' : (1, 7)
	},

	{
		'encode' : rol,
		'decode' : '(({data} >> {key}) | ({data} << {keyMinus8})) & 0xff',
		'keyRange' : (1, 7)
	},

	{
		'encode' : bitNot,
		'decode' : '(~{data}) & 0xff',
	},
]

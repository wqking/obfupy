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

import os
import codecs

class Document :
	_uidSeed = 1

	def __init__(self) :
		self._fileName = ''
		self._content = ''
		self._uid = 'uid_%d' % (Document._uidSeed)
		Document._uidSeed += 1

	def loadFromFile(self, fileName) :
		file = codecs.open(fileName, "r", "utf-8")
		self._content = file.read()
		file.close()
		self._fileName = fileName
		return self

	def getContent(self) :
		return self._content

	def setContent(self, content) :
		self._content = str(content)

	def getFileName(self) :
		return self._fileName

	def getUid(self) :
		return self._uid

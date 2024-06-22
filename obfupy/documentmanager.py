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

class DocumentManager :
	def __init__(self) :
		self._documentList = []
		self._uidDocumentMap = {}

	def getDocumentList(self) :
		return self._documentList

	def addDocument(self, document) :
		if isinstance(document, list) :
			self._documentList += document
			for doc in document :
				self._uidDocumentMap[doc.getUid()] = doc
		else :
			self._documentList.append(document)
			self._uidDocumentMap[document.getUid()] = document

	def getDocumentByUid(self, uid) :
		return self._uidDocumentMap[uid]

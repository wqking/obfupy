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

from .. import astutil

class ExtraNodeManager :
	def __init__(self) :
		self._nodeList = []
		self._nodeNameSet = {}

	def addNode(self, node, checkExisting = False) :
		if isinstance(node, list) :
			for n in node :
				self.addNode(n, checkExisting)
			return
		name = None
		if isinstance(checkExisting, str) :
			name = checkExisting
		elif checkExisting is True :
			name = astutil.astToSource(node)
		if name is not None :
			if name in self._nodeNameSet :
				return
			self._nodeNameSet[name] = True
		self._nodeList.append(node)

	def getNodeList(self) :
		return self._nodeList

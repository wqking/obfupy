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

from ..import astutil
from ..import util

import random
import ast

class GotoWithIf :
	def __init__(self, visitor) :
		self._visitor = visitor
		self._labelList = []
		self._handlerList = []
		self._body = None
		self._varName = util.getUnusedRandomSymbol()

	def getNewLable(self) :
		label = self._generateNewLable()
		self._labelList.append(label)
		return label

	def gotoLabel(self, label) :
		return astutil.makeAssignment(
			ast.Name(id = self._varName, ctx = ast.Store()),
			self._visitNode(ast.Constant(value = label))
		)

	def addHandler(self, label, handlerNodeList) :
		for handle in self._handlerList :
			assert label != handle["label"]

		self._handlerList.append({
			"label" : label,
			"nodeList" : handlerNodeList
		})

	def setBody(self, bodyNodeList) :
		self._body = bodyNodeList

	def makeNode(self) :
		assert self._body is not None
		assert len(self._labelList) == len(self._handlerList)

		resultNodeList = []
		startLabel = self._generateNewLable()
		resultNodeList.append(astutil.makeAssignment(
			ast.Name(id = self._varName, ctx = ast.Store()),
			self._visitNode(ast.Constant(value = startLabel))
		))

		resultNodeList = util.joinList(resultNodeList, self._body)

		node = None
		for handler in self._handlerList :
			node = ast.If(
				test = ast.Compare(
					left = ast.Name(id = self._varName, ctx = ast.Load()),
					ops = [ ast.Eq() ],
					comparators = [ self._visitNode(ast.Constant(value = handler['label'])) ]
				),
				body = util.ensureList(handler['nodeList']),
				orelse = []
			)
			resultNodeList.append(node)

		return resultNodeList

	def _generateNewLable(self) :
		right = 50
		while True :
			label = random.randint(1, right)
			if label not in self._labelList :
				return label
			right += 50

	def _visitNode(self, node) :
		return self._visitor._doVisit(node)

class LabelOrderRandomizer :
	def __init__(self) :
		self._handlerList = []

	def addHandler(self, label, handlerNodeList) :
		self._handlerList.append({
			"label" : label,
			"nodeList" : handlerNodeList
		})

	def takeOut(self, goto) :
		random.shuffle(self._handlerList)
		for handler in self._handlerList :
			goto.addHandler(handler['label'], handler['nodeList'])
		self._handlerList = []

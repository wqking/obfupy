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

import enum

guardId_compare = 1
guardId_boolOp = 2
guardId_constant = 3
guardId_makeCodeBlock = 4

featureYield = "yield"

class NodeProperties(str, enum.Enum) :
	docstring = 'docstring'

def setNodeContext(node, context) :
	assert not hasattr(node, 'visitorContext')
	node.visitorContext = context

def getNodeContext(node) :
	assert hasattr(node, 'visitorContext')
	assert node.visitorContext is not None
	return node.visitorContext

def setNodeProperty(node, property, value = False) :
	if not hasattr(node, 'vistorProperties') :
		node.vistorProperties = {}
	node.vistorProperties[property] = value

def getNodeProperty(node, property, default = None) :
	if not hasattr(node, 'vistorProperties') :
		return default
	return node.vistorProperties[property]

def markNodeDocString(node) :
	if astutil.isChildDocString(node) :
		setNodeProperty(node.body[0].value, NodeProperties.docstring)
		setNodeProperty(node, NodeProperties.docstring)

def isConstantNodeMarkedDocString(node) :
	return getNodeProperty(node, NodeProperties.docstring) is not None

def isNodeMarkedDocString(node) :
	return getNodeProperty(node, NodeProperties.docstring) is not None

def findFirstInsertableIndex(node) :
	if isNodeMarkedDocString(node) :
		return 1
	return 0

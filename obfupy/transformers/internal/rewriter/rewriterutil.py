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

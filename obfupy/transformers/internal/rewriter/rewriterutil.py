guardId_compare = 1
guardId_boolOp = 2
guardId_constant = 3
guardId_makeCodeBlock = 4

featureYield = "yield"

def getNodeContext(node) :
	assert hasattr(node, 'visitorContext')
	assert node.visitorContext is not None
	return node.visitorContext

def setNodeContext(node, context) :
	assert not hasattr(node, 'visitorContext')
	node.visitorContext = context


featureYield = "yield"

def getNodeContext(node) :
	assert hasattr(node, 'visitorContext')
	assert node.visitorContext is not None
	return node.visitorContext

def setNodeContext(node, context) :
	assert not hasattr(node, 'visitorContext')
	node.visitorContext = context


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

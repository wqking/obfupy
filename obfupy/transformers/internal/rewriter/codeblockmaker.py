import random
import ast

from .. import util

class CodeBlockMaker :
	def __init__(self, logicMaker) :
		self._logicMaker = logicMaker

	def makeCodeBlock(self, node, allowOuterBlock, depth = 1) :
		return self.doMakeCodeBlock(node, allowOuterBlock, depth)

	def doMakeCodeBlock(self, node, allowOuterBlock, depth) :
		if depth <= 0 :
			return node
		isLoop = isinstance(node, ( ast.For, ast.While, ast.AsyncFor ))
		useOuter = False
		if allowOuterBlock and util.hasChance(2) :
			useOuter = True
		else :
			useOuter = False
		callbackList = [
			self.doMakeIfBlock,
		]
		# Below while/for maker can't be used as inner block in a loop, that will cause continue/break not working
		if useOuter or not isLoop :
			callbackList += [
				self.doMakeWhileBlock,
				self.doMakeForBlockWithRange,
				self.doMakeForBlockWithIn
			]
		callback = random.choice(callbackList)
		if useOuter :
			node = callback([ node ])
		else :
			node.body = [ callback(node.body) ]
			node = node
		return self.doMakeCodeBlock(node, allowOuterBlock, depth - 1)

	def doMakeIfBlock(self, bodyNodeList) :
		return ast.If(
			test = self._logicMaker.makeTrue(None),
			body = bodyNodeList,
			orelse = []
		)

	def doMakeWhileBlock(self, bodyNodeList) :
		return ast.While(
			test = self._logicMaker.makeTrue(None),
			body = bodyNodeList + [ ast.Break() ],
			orelse = []
		)

	def doMakeForBlockWithRange(self, bodyNodeList) :
		args = [ random.randint(2, 50) ]
		if util.hasChance(3) :
			args.append(args[0] - 1)
			args.append(-1)
		else :
			args.append(args[0] + 1)
		iter = ast.Call(
			func = ast.Name(id = 'range', ctx = ast.Load()),
			args = [ ast.Constant(value = n) for n in args ],
			keywords = []
		)
		return self.doMakeForBlockFromIter(bodyNodeList, iter)

	def doMakeForBlockWithIn(self, bodyNodeList) :
		nodeType = ast.List
		if util.hasChance(2) :
			nodeType = ast.Tuple
		iter = nodeType(
			elts = [ ast.Constant(value = random.randint(0, 50)) ],
			ctx = ast.Load()
		)
		return self.doMakeForBlockFromIter(bodyNodeList, iter)

	def doMakeForBlockFromIter(self, bodyNodeList, iter) :
		return ast.For(
			target = ast.Name(id = util.getUnusedRandomSymbol(), ctx = ast.Store()),
			iter = iter,
			body = bodyNodeList,
			orelse = []
		)

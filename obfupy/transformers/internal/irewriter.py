import ast
import random
import copy

from . import util
from . import astutil
from . import reentryguard
from . import builtinfunctions
from .rewriter import constantmanager
from .rewriter import logicmaker
from .rewriter import nopmaker
from .rewriter import context
from .rewriter import codeblockmaker
from .rewriter import extranodemanager

astMaxPhaseCount = 2

guardId_compare = 1
guardId_boolOp = 2
guardId_constant = 3
guardId_makeCodeBlock = 4
guardId_extactFunction = 5

class _AstVistor(ast.NodeTransformer) :
	def __init__(self, options) :
		super().__init__()
		self._options = options
		self._renameArgument = self._options['renameArgument']
		self._contextStack = context.ContextStack()
		self._constantManager = constantmanager.ConstantManager(self._options['stringEncoders'])
		self._nopMaker = nopmaker.NopMaker()
		self.reset(0)

	def reset(self, phase) :
		self._phase = phase
		self._reentryGuard = reentryguard.ReentryGuard()

	def isPreprocessPhase(self) :
		return self._phase == 0

	def isRewritePhase(self) :
		return self._phase == 1

	def prependNodes(self, body, nodeList) :
		if nodeList is None :
			return
		if isinstance(nodeList, list) :
			for node in reversed(nodeList) :
				self.prependNodes(body, node)
		else :
			body.insert(0, nodeList)

	def makeResultNode(self, node) :
		siblingList = self._contextStack.getCurrentContext().getSiblingNodeList()
		if len(siblingList)  == 0 :
			return node
		return siblingList + [ node ]

	def visit_Module(self, node) :
		with context.ContextGuard(self._contextStack, context.ModuleContext()) as currentContext :
			self.doRemoveDocString(node)
			node = self.generic_visit(node)
			if self.isRewritePhase() :
				extraNodeManager = extranodemanager.ExtraNodeManager()
				self._constantManager.loadExtraNode(extraNodeManager)
				self._nopMaker.loadExtraNode(extraNodeManager)
				self.prependNodes(node.body, extraNodeManager.getNodeList())
			return node

	def visit_ClassDef(self, node):
		with context.ContextGuard(self._contextStack, context.ClassContext(node.name)) :
			self.doRemoveDocString(node)
			node = self.generic_visit(node)
			return self.makeResultNode(node)

	def visit_AsyncFunctionDef(self, node):
		return self.doRewriteFunction(node)

	def visit_FunctionDef(self, node) :
		return self.doRewriteFunction(node)

	def doRewriteFunction(self, node) :
		self.doRemoveDocString(node)
		newNode = self.doExtractFunction(node)
		if newNode is not None :
			return newNode
		with context.ContextGuard(self._contextStack, context.FunctionContext(node.name)) as currentContext :
			renamedArgsListNode = None
			if self.isRewritePhase() and self._renameArgument :
				renamedArgsListNode = self.doCreateRenamedArgsList(node)

			node.body = self.doVisitNodeList(node.body)
			# Only visit decorator_list in nested function
			if currentContext.getParentContext().isFunction() :
				node.decorator_list = self.doVisitNodeList(node.decorator_list)

			if renamedArgsListNode is not None :
				node.body.insert(0, renamedArgsListNode)

			return node
		
	def doCreateRenamedArgsList(self, node) :
		renamedArgList = []
		currentContext = self._contextStack.getCurrentContext()
		argList = [ node.args.args, node.args.posonlyargs, node.args.kwonlyargs, [ node.args.vararg, node.args.kwarg ] ]
		for item in argList :
			for argItem in item :
				if argItem is None :
					continue
				currentContext.addArgument(argItem.arg)
				renamedArgList.append({
					'newName' : currentContext.getNewName(argItem.arg),
					'argName' : argItem.arg
				})
		if len(renamedArgList) > 0 :
			random.shuffle(renamedArgList)
			targetList = []
			valueList = []
			for item in renamedArgList :
				targetList.append(ast.Name(id = item['newName'], ctx = ast.Store()))
				valueList.append(ast.Name(id = item['argName'], ctx = ast.Load()))
			return astutil.makeAssignment(targetList, valueList)
		return None

	def doExtractFunction(self, node) :
		if not self.isRewritePhase() :
			return None
		if self._reentryGuard.isEntered(guardId_extactFunction) :
			return None
		with (reentryguard.AutoReentryGuard(self._reentryGuard, guardId_extactFunction),
			context.ContextGuard(self._contextStack, context.FunctionContext(node.name)) as currentContext) :
			parentContext = currentContext.getParentContext()
			if not (parentContext.isModule() or parentContext.isClass()) :
				return None
			if currentContext.getPersistentContext().isNameSeen('super') :
				return None
			newFuncNode = copy.deepcopy(node)
			newFuncNode.decorator_list = []
			newFuncNode.args.defaults = []
			# Don't set it, it's used by bare *
			#newFuncNode.args.kw_defaults = []
			newFuncNode.name = currentContext.getNewName(newFuncNode.name)
			# Don't shuffle parameter order, it will cause recursive calling failure
			argList = [ newFuncNode.args.posonlyargs, newFuncNode.args.args, newFuncNode.args.kwonlyargs, [ newFuncNode.args.vararg, newFuncNode.args.kwarg ] ]
			for item in argList :
				for argItem in item :
					if argItem is None :
						continue
					argItem.arg = currentContext.getNewName(argItem.arg)
			# The variables in renamedArgsListNode is not used by function body because the body uses the new arg names
			renamedArgsListNode = self.doCreateRenamedArgsList(newFuncNode)
			newFuncNode.body = self.doVisitNodeList(newFuncNode.body)
			if renamedArgsListNode is not None :
				newFuncNode.body.insert(0, renamedArgsListNode)
			callArgs = []
			callKeywords = []
			argList = [ node.args.posonlyargs, node.args.args ]
			for i in range(len(argList)) :
				itemList = argList[i]
				for argItem in itemList :
					if argItem is None :
						continue
					callArgs.append(ast.Name(id = argItem.arg, ctx = ast.Load()))
			if node.args.vararg :
				callArgs.append(ast.Starred(
					value = ast.Name(id = node.args.vararg.arg, ctx = ast.Load()),
					ctx = ast.Load()
				))
			argList = node.args.kwonlyargs
			for argItem in argList :
				if argItem is None :
					continue
				callKeywords.append(
					ast.keyword(
						arg = currentContext.findNewName(argItem.arg),
						value = ast.Name(id = argItem.arg, ctx = ast.Load())
					)
				)
			if node.args.kwarg :
				callKeywords.append(ast.keyword(value = ast.Name(id = node.args.kwarg.arg, ctx = ast.Load())))
			newBody = ast.Return(
				value = ast.Call(
					func = ast.Name(newFuncNode.name, ctx = ast.Load()),
					args = callArgs,
					keywords = callKeywords
				)
			)
			node.body = [ newBody ]
			if parentContext.isModule() :
				return [ newFuncNode, node ]
			else :
				parentContext.addSiblingNode(newFuncNode)
				return node
		return None
	
	def visit_Name(self, node) :
		if node.id in [ 'super' ] :
			self._contextStack.getCurrentContext().getPersistentContext().seeName(node.id)
		self._contextStack.getCurrentContext().seeName(node.id)
		if self.isRewritePhase() :
			node.id = self._contextStack.findNewName(node.id)
		return node
	
	def visit_For(self, node):
		node = self.doMakeCodeBlock(node, visitChildren =True, allowOuterBlock = True)
		return node

	def visit_While(self, node):
		node = self.doMakeCodeBlock(node, visitChildren =True, allowOuterBlock = True)
		return node

	def visit_Call(self, node) :
		if self.isRewritePhase() :
			if isinstance(node.func, ast.Name) and node.func.id in builtinfunctions.builtinFunctionMap :
				node.func = self._constantManager.getNameReplacedNode(node.func.id)
		return self.generic_visit(node)

	def visit_Compare(self, node) :
		if self._reentryGuard.isEntered([ guardId_compare, guardId_boolOp ]) :
			return self.generic_visit(node)
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_compare) :
			node = self.doRewriteLogicalOperator(node)
			return self.generic_visit(node)

	def visit_BoolOp(self, node) :
		if self._reentryGuard.isEntered(guardId_boolOp) :
			return self.generic_visit(node)
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_boolOp) :
			node = self.doRewriteLogicalOperator(node)
			return self.generic_visit(node)

	def visit_If(self, node) :
		with reentryguard.AutoReentryGuard(self._reentryGuard, [ guardId_compare, guardId_boolOp ]) :
			return self.doRewriteIf(node)

	def visit_Constant(self, node) :
		if self._reentryGuard.isEntered(guardId_constant) :
			return self.generic_visit(node)
		return self.doRewriteConstant(node)

	def visit_JoinedStr(self, node) :
		# Don't obfuscate constants in f-string (JoinedStr), otherwise ast.unparse will give error
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_constant) :
			return self.generic_visit(node)

	def visit_Assign(self, node) :
		return self.doRewriteLocalVariable(node)

	def visit_AugAssign(self, node) :
		return self.doRewriteLocalVariable(node)

	# walrus operator
	def visit_NamedExpr(self, node) :
		return self.doRewriteLocalVariable(node)

	def visit_Global(self, node) :
		for name in node.names :
			self._contextStack.getCurrentContext().useGlobalName(name)
		return self.generic_visit(node)

	def visit_Nonlocal(self, node) :
		currentContext = self._contextStack.getCurrentContext()
		for i in range(len(node.names)) :
			name = node.names[i]
			currentContext.useNonlocalName(name)
			if self.isRewritePhase() :
				node.names[i] = self._contextStack.findNewName(name)
		return self.generic_visit(node)

	def doMakeCodeBlock(self, node, visitChildren, allowOuterBlock) :
		if self.isRewritePhase() :
			if not self._reentryGuard.isEntered(guardId_makeCodeBlock) :
				with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_makeCodeBlock) :
					node = self.createCodeBlockMaker().makeCodeBlock(node, allowOuterBlock)
					if visitChildren :
						node = self.generic_visit(node)
					return node
		if visitChildren :
			node = self.generic_visit(node)
		return node

	def doRewriteLocalVariable(self, node) :
		currentContext = self._contextStack.getCurrentContext()
		if self.isRewritePhase() and currentContext.isFunction() :
			targetList = []
			if hasattr(node, 'targets') :
				targetList = node.targets
			elif hasattr(node, 'target') :
				targetList = node.target
			targetNodeList = astutil.getNodeListFromAssignTargets(targetList)
			for target in targetNodeList :
				if not isinstance(target, ast.Name) :
					continue
				name = target.id
				if not self.canNameBeLocalVariable(name) :
					continue
				target.id = currentContext.getNewName(name)
		return self.generic_visit(node)
	
	def canNameBeLocalVariable(self, name) :
		currentContext = self._contextStack.getCurrentContext()
		if currentContext.isArgument(name) :
			return False
		if util.isUsedRandomSymbol(name) :
			return False
		# Leave it to visit_Name to rename
		if currentContext.isGlobalOrNonlocal(name) :
			return False
		if currentContext.isRenamed(name) :
			return False
		# Symbol is used before assignment, just don't rename it
		if currentContext.isNameSeen(name) :
			return False
		return True

	def doVisitNodeList(self, nodeList) :
		result = []
		for node in nodeList :
			newNode = self.visit(node)
			if newNode is not None :
				result.append(newNode)
		return result

	def doRewriteIf(self, node) :
		if not self.isRewritePhase() :
			return self.generic_visit(node)
		if not astutil.isLogicalNode(node.test) :
			return self.generic_visit(node)
		newTest = astutil.makeNegation(node.test)
		if newTest is not None :
			newTest = self.createLogicMaker().makeTrue(newTest)
			node.test = newTest
			node.body, node.orelse = node.orelse, node.body
			if len(node.body) == 0 :
				node.body.append(ast.Pass())
		return self.generic_visit(node)

	def doRewriteConstant(self, node) :
		if self.isPreprocessPhase() :
			self._constantManager.foundConstant(node.value)
		elif self.isRewritePhase() :
			newNode = self._constantManager.getConstantReplacedNode(node.value)
			if newNode is not None :
				return newNode
		return node

	def doRewriteLogicalOperator(self, node) :
		if not self.isRewritePhase() :
			return node
		if not astutil.isLogicalNode(node) :
			return node
		newNode = astutil.makeNegation(node)
		newNode = astutil.addNot(newNode)
		return newNode
	
	def doRemoveDocString(self, node) :
		# Do it in preprocess phase otherwise it will be taken out as constant
		if not self.isPreprocessPhase() :
			return
		# See get_raw_docstring in Python built-in ast.py
		if len(node.body) == 0 :
			return
		child = node.body[0]
		if not isinstance(child, ast.Expr) :
			return
		child = child.value
		if not isinstance(child, ast.Constant) or not isinstance(child.value, str) :
			return
		node.body = node.body[1 : ]
		if len(node.body) == 0 :
			node.body.append(ast.Pass())

	def createLogicMaker(self) :
		return logicmaker.LogicMaker(self._nopMaker, constants = self._constantManager.getConstantValueList())

	def createCodeBlockMaker(self) :
		return codeblockmaker.CodeBlockMaker(self.createLogicMaker())

class _IRewriter :
	def __init__(self, options) :
		super().__init__()
		self._options = options
		self._documentManager = None

	def getDocumentList(self) :
		return self._documentManager.getDocumentList()

	def transform(self, documentManager) :
		self._documentManager = documentManager
		astMap = {}
		visitorMap = {}

		for document in self.getDocumentList() :
			rootNode = ast.parse(document.getContent(), document.getFileName())
			astMap[document.getUid()] = rootNode
			visitor = _AstVistor(options = self._options)
			visitorMap[document.getUid()] = visitor

		for document in self.getDocumentList() :
			rootNode = astMap[document.getUid()]
			visitor = visitorMap[document.getUid()]
			for i in range(astMaxPhaseCount) :
				visitor.reset(i)
				visitor.visit(rootNode)

		for document in self.getDocumentList() :
			rootNode = astMap[document.getUid()]
			document.setContent(astutil.astToSource(rootNode))

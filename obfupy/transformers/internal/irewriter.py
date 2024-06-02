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
guardId_inCase = 6

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

	def _isPreprocessPhase(self) :
		return self._phase == 0

	def _isRewritePhase(self) :
		return self._phase == 1

	def _prependNodes(self, body, nodeList) :
		if nodeList is None :
			return
		if isinstance(nodeList, list) :
			for node in reversed(nodeList) :
				self._prependNodes(body, node)
		else :
			body.insert(0, nodeList)

	def _makeResultNode(self, node) :
		siblingList = self._contextStack.getCurrentContext().getSiblingNodeList()
		if len(siblingList)  == 0 :
			return node
		return siblingList + [ node ]

	def visit_Module(self, node) :
		with context.ContextGuard(self._contextStack, context.ModuleContext()) as currentContext :
			self._doRemoveDocString(node)
			node = self.generic_visit(node)
			if self._isRewritePhase() :
				extraNodeManager = extranodemanager.ExtraNodeManager()
				self._constantManager.loadExtraNode(extraNodeManager)
				self._nopMaker.loadExtraNode(extraNodeManager)
				self._prependNodes(node.body, extraNodeManager.getNodeList())
			return node

	def visit_ClassDef(self, node):
		with context.ContextGuard(self._contextStack, context.ClassContext(node.name)) :
			self._doRemoveDocString(node)
			node = self.generic_visit(node)
			return self._makeResultNode(node)

	def visit_AsyncFunctionDef(self, node):
		with context.ContextGuard(self._contextStack, context.FunctionContext(node.name)) :
			node = self._doRewriteFunction(node)
			return self._makeResultNode(node)

	def visit_FunctionDef(self, node) :
		with context.ContextGuard(self._contextStack, context.FunctionContext(node.name)) :
			node = self._doRewriteFunction(node)
			return self._makeResultNode(node)

	def _doRewriteFunction(self, node) :
		for argNode in node.args.defaults :
			if argNode is not None :
				self.visit(argNode)
		for argNode in node.args.kw_defaults :
			if argNode is not None :
				self.visit(argNode)

		self._doRemoveDocString(node)
		newNode = self._doExtractFunction(node)
		if newNode is not None :
			return newNode
		newNode = self._doRenameArguments(node)
		if newNode is not None :
			return newNode
		return node

	def _doRenameArguments(self, node) :
		currentContext = self._contextStack.getCurrentContext()
		renamedArgsListNode = None
		if self._isRewritePhase() :
			renamedArgsListNode = self._doCreateRenamedArgsList(node)

		# Only visit decorator_list in nested function
		if currentContext.getParentContext().isFunction() :
			node.decorator_list = self._doVisitNodeList(node.decorator_list)
			if self._isRewritePhase() :
				# Rename innner function and put the new name into outer function context
				if currentContext.getParentContext().isGlobalOrNonlocal(node.name) :
					node.name = self._contextStack.getCurrentContext().findRenamedNameInChain(node.name) or node.name
			'''
			# Don't rename nested function
				else :
					node.name = currentContext.getParentContext().renameSymbol(node.name)
			'''
		# This visit must be after previous block, after node.name is renamed.
		node.body = self._doVisitNodeList(node.body)

		if renamedArgsListNode is not None :
			node.body.insert(0, renamedArgsListNode)

		return node
		
	def _doCreateRenamedArgsList(self, node) :
		renamedArgList = []
		currentContext = self._contextStack.getCurrentContext()
		argList = [ node.args.args, node.args.posonlyargs, node.args.kwonlyargs, [ node.args.vararg, node.args.kwarg ] ]
		for item in argList :
			for argItem in item :
				if argItem is None :
					continue
				currentContext.addArgument(argItem.arg)
				renamedArgList.append({
					'newName' : currentContext.renameSymbol(argItem.arg),
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

	def _doExtractFunction(self, node) :
		if not self._isRewritePhase() :
			return None
		# Don't extract special names such as __cast, which name is mangled.
		if util.isNameMangling(node.name) :
			return None
		currentContext = self._contextStack.getCurrentContext()
		# If the function contains any managed names, don't extract because the names are not accessible outside of the class
		for name in currentContext.getPersistentContext().getSeenNameSet() :
			if util.isNameMangling(name) :
				return None
		for name in currentContext.getPersistentContext().getSeenAttributeSet() :
			if util.isNameMangling(name) :
				return None
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_extactFunction) :
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
			# Don't put the new name to context, not only it's unnecessary, but also it will cause trouble
			# such as the member method call another global function of the same name
			newName = self._contextStack.getCurrentContext().findRenamedNameInChain(newFuncNode.name)
			newFuncNode.name = newName or util.getUnusedRandomSymbol()
			# Don't shuffle parameter order, it will cause recursive calling failure
			argList = [
				newFuncNode.args.posonlyargs,
				newFuncNode.args.args,
				newFuncNode.args.kwonlyargs,
				[ newFuncNode.args.vararg, newFuncNode.args.kwarg ]
			]
			for item in argList :
				for argItem in item :
					if argItem is None :
						continue
					argItem.arg = currentContext.renameSymbol(argItem.arg)
			# The variables in renamedArgsListNode is not used by function body because the body uses the new arg names
			renamedArgsListNode = self._doCreateRenamedArgsList(newFuncNode)
			newFuncNode.body = self._doVisitNodeList(newFuncNode.body)
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
						arg = currentContext.findRenamedName(argItem.arg) or argItem.arg,
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
			node = self._convertFunctionToLambda(node) or node
			self._contextStack.getTopScopedContext().addSiblingNode(newFuncNode)
			return node
			if parentContext.isModule() :
				return [ newFuncNode, node ]
			else :
				parentContext.addSiblingNode(newFuncNode)
				return node
		return None
	
	def _convertFunctionToLambda(self, node) :
		if type(node) != ast.FunctionDef :
			return None
		if len(node.decorator_list) > 0 :
			return None
		if len(node.body) != 1 :
			return None
		if util.isSpecialFunctionName(node.name) :
			return None
		bodyNode = node.body[0]
		lambdaBody = None
		if isinstance(bodyNode, ast.Pass) :
			lambdaBody = bodyNode
		elif isinstance(bodyNode, ast.Return) :
			lambdaBody = bodyNode.value
		else :
			return None
		arguments = copy.deepcopy(node.args)
		argList = [
			arguments.posonlyargs,
			arguments.args,
			arguments.kwonlyargs,
			[ arguments.vararg, arguments.kwarg ]
		]
		for item in argList :
			for argItem in item :
				if argItem is None :
					continue
				argItem.annotation = None
				argItem.type_comment = None
		lambdaNode = ast.Lambda(
			args = arguments,
			body = lambdaBody
		)
		return astutil.makeAssignment(ast.Name(id = node.name, ctx = ast.Store()), lambdaNode)

	def visit_Name(self, node) :
		self._contextStack.getCurrentContext().getPersistentContext().seeName(node.id)
		self._contextStack.getCurrentContext().seeName(node.id)
		if self._isRewritePhase() :
			node.id = self._contextStack.getCurrentContext().findRenamedNameInChain(node.id) or node.id
		return node
	
	def visit_Attribute(self, node) :
		self._contextStack.getCurrentContext().getPersistentContext().seeAttribute(node.attr)
		return self.generic_visit(node)

	def visit_For(self, node):
		node = self._doRewriteLocalVariable(node)
		node = self._doMakeCodeBlock(node, visitChildren =True, allowOuterBlock = True)
		return node

	def visit_While(self, node):
		node = self._doMakeCodeBlock(node, visitChildren =True, allowOuterBlock = True)
		return node

	def visit_Call(self, node) :
		if self._isRewritePhase() :
			if isinstance(node.func, ast.Name) and node.func.id in builtinfunctions.builtinFunctionMap :
				node.func = self._constantManager.getNameReplacedNode(node.func.id)
		return self.generic_visit(node)

	def visit_Compare(self, node) :
		if self._reentryGuard.isEntered([ guardId_compare, guardId_boolOp ]) :
			return self.generic_visit(node)
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_compare) :
			node = self._doRewriteLogicalOperator(node)
			return self.generic_visit(node)

	def visit_BoolOp(self, node) :
		if self._reentryGuard.isEntered(guardId_boolOp) :
			return self.generic_visit(node)
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_boolOp) :
			node = self._doRewriteLogicalOperator(node)
			return self.generic_visit(node)

	def visit_If(self, node) :
		with reentryguard.AutoReentryGuard(self._reentryGuard, [ guardId_compare, guardId_boolOp ]) :
			return self._doRewriteIf(node)

	def visit_Constant(self, node) :
		if self._reentryGuard.isEntered(guardId_constant) :
			return self.generic_visit(node)
		return self._doRewriteConstant(node)

	def visit_Case(self, node):
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_inCase) :
			return self.generic_visit(node)

	def visit_JoinedStr(self, node) :
		# Don't obfuscate constants in f-string (JoinedStr), otherwise ast.unparse will give error
		with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_constant) :
			return self.generic_visit(node)

	def visit_Assign(self, node) :
		return self.generic_visit(self._doRewriteLocalVariable(node))

	def visit_AugAssign(self, node) :
		return self.generic_visit(self._doRewriteLocalVariable(node))

	# walrus operator
	def visit_NamedExpr(self, node) :
		return self.generic_visit(self._doRewriteLocalVariable(node))

	def visit_Import(self, node) :
		node = self._doRenameImport(node)
		return self.generic_visit(node)
	
	def visit_ImportFrom(self, node) :
		node = self._doRenameImport(node)
		return self.generic_visit(node)
	
	def _doRenameImport(self, node) :
		for alias in node.names :
			if alias.asname is not None :
				alias.asname = self._contextStack.getCurrentContext().findRenamedNameInChain(alias.asname) or alias.asname
		return node

	def visit_Global(self, node) :
		for name in node.names :
			self._contextStack.getCurrentContext().useGlobalName(name)
		return self.generic_visit(node)

	def visit_Nonlocal(self, node) :
		currentContext = self._contextStack.getCurrentContext()
		for i in range(len(node.names)) :
			name = node.names[i]
			currentContext.useNonlocalName(name)
			if self._isRewritePhase() :
				node.names[i] = self._contextStack.getCurrentContext().findRenamedNameInChain(name) or name
		return self.generic_visit(node)

	def visit_Lambda(self, node) :
		if self._isRewritePhase() :
			with context.ContextGuard(self._contextStack, context.FunctionContext('lambda')) :
				currentContext = self._contextStack.getCurrentContext()
				argList = [ node.args.args, node.args.posonlyargs, node.args.kwonlyargs, [ node.args.vararg, node.args.kwarg ] ]
				for item in argList :
					for argItem in item :
						if argItem is None :
							continue
						argItem.arg = currentContext.renameSymbol(argItem.arg)
				node.args = self.visit(node.args)
				node.body = self.visit(node.body)
				return node
		return self.generic_visit(node)

	def _doMakeCodeBlock(self, node, visitChildren, allowOuterBlock) :
		if self._isRewritePhase() :
			if not self._reentryGuard.isEntered(guardId_makeCodeBlock) :
				with reentryguard.AutoReentryGuard(self._reentryGuard, guardId_makeCodeBlock) :
					node = self._createCodeBlockMaker().makeCodeBlock(node, allowOuterBlock)
					if visitChildren :
						node = self.generic_visit(node)
					return node
		if visitChildren :
			node = self.generic_visit(node)
		return node

	def _doRewriteLocalVariable(self, node) :
		currentContext = self._contextStack.getCurrentContext()
		if self._isRewritePhase() and currentContext.isFunction() :
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
				if not self._canNameBeLocalVariable(name) :
					continue
				target.id = currentContext.renameSymbol(name)
		return node
	
	def _canNameBeLocalVariable(self, name) :
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

	def _doVisitNodeList(self, nodeList) :
		result = []
		for node in nodeList :
			newNode = self.visit(node)
			if newNode is not None :
				result.append(newNode)
		return result

	def _doRewriteIf(self, node) :
		if not self._isRewritePhase() :
			return self.generic_visit(node)
		if not astutil.isLogicalNode(node.test) :
			return self.generic_visit(node)
		newTest = astutil.makeNegation(node.test)
		if newTest is not None :
			newTest = self._createLogicMaker().makeTrue(newTest)
			node.test = newTest
			node.body, node.orelse = node.orelse, node.body
			if len(node.body) == 0 :
				node.body.append(ast.Pass())
		return self.generic_visit(node)

	def _doRewriteConstant(self, node) :
		if self._reentryGuard.isEntered(guardId_boolOp) :
			return node
		if self._isPreprocessPhase() :
			self._constantManager.foundConstant(node.value)
		elif self._isRewritePhase() :
			newNode = self._constantManager.getConstantReplacedNode(node.value)
			if newNode is not None :
				return newNode
		return node

	def _doRewriteLogicalOperator(self, node) :
		if not self._isRewritePhase() :
			return node
		if not astutil.isLogicalNode(node) :
			return node
		newNode = astutil.makeNegation(node)
		newNode = astutil.addNot(newNode)
		return newNode
	
	def _doRemoveDocString(self, node) :
		# Do it in preprocess phase otherwise it will be taken out as constant
		if not self._isPreprocessPhase() :
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

	def _createLogicMaker(self) :
		return logicmaker.LogicMaker(self._nopMaker, constants = self._constantManager.getConstantValueList())

	def _createCodeBlockMaker(self) :
		return codeblockmaker.CodeBlockMaker(self._createLogicMaker())

class _IRewriter :
	def __init__(self, options) :
		super().__init__()
		self._options = options
		self._documentManager = None

	def _getDocumentList(self) :
		return self._documentManager.getDocumentList()

	def XXXtransform(self, documentManager) :
		self._documentManager = documentManager
		astMap = {}
		visitorMap = {}

		for document in self._getDocumentList() :
			rootNode = ast.parse(document.getContent(), document.getFileName())
			astMap[document.getUid()] = rootNode
			visitor = _AstVistor(options = self._options)
			visitorMap[document.getUid()] = visitor

		for document in self._getDocumentList() :
			rootNode = astMap[document.getUid()]
			visitor = visitorMap[document.getUid()]
			for i in range(astMaxPhaseCount) :
				visitor.reset(i)
				visitor.visit(rootNode)

		for document in self._getDocumentList() :
			rootNode = astMap[document.getUid()]
			document.setContent(astutil.astToSource(rootNode))

	def transform(self, documentManager) :
		self._documentManager = documentManager
		for document in self._getDocumentList() :
			rootNode = ast.parse(document.getContent(), document.getFileName())
			visitor = _AstVistor(options = self._options)
			for i in range(astMaxPhaseCount) :
				visitor.reset(i)
				visitor.visit(rootNode)
			document.setContent(astutil.astToSource(rootNode))

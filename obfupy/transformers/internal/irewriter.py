import ast
import random

from . import util
from . import astutil
from . import reentryguard
from .rewriter import constantmanager
from .rewriter import logicmaker
from .rewriter import nopmaker
from .rewriter import context

astMaxPhaseCount = 2

guardId_compare = 1
guardId_boolOp = 2
guardId_constant = 3

class _AstVistor(ast.NodeTransformer) :
	def __init__(self, options) :
		super().__init__()
		self._options = options
		self._renameArgument = self._options['renameArgument']
		self._contextStack = context.ContextStack(context.GlobalContext())
		self._constantManager = constantmanager.ConstantManager(self._options)
		self._nopMaker = nopmaker.NopMaker()
		self._logicMaker = logicmaker.LogicMaker(self._nopMaker)
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

	def visit_Module(self, node) :
		self.doRemoveDocString(node)
		node = self.generic_visit(node)
		if self.isRewritePhase() :
			self.prependNodes(node.body, self._nopMaker.getDefineNodes())
			self.prependNodes(node.body, self._constantManager.getDefineNodes())
		return node

	def visit_ClassDef(self, node):
		self._contextStack.pushContext(context.ClassContext())
		self.doRemoveDocString(node)
		node = self.generic_visit(node)
		self._contextStack.popContext()
		return node

	def visit_AsyncFunctionDef(self, node):
		self.doRemoveDocString(node)
		return self.generic_visit(node)

	def visit_FunctionDef(self, node) :
		self.doRemoveDocString(node)
		currentContext = self._contextStack.pushContext(context.FunctionContext())
		renamedArgList = []
		if self.isRewritePhase() and self._renameArgument :
			for arg in node.args.args :
				renamedArgList.append({
					'newName' : currentContext.getNewName(arg.arg),
					'argName' : arg.arg
				})
		node.body = self.doVisitNodeList(node.body)
		# Don't visit decorator_list, don't rename anything in decorator_list
		#node.decorator_list = self.doVisitNodeList(node.decorator_list)

		if len(renamedArgList) > 0 :
			random.shuffle(renamedArgList)
			targetList = []
			valueList = []
			for item in renamedArgList :
				targetList.append(ast.Name(id = item['newName'], ctx = ast.Store()))
				valueList.append(ast.Name(id = item['argName'], ctx = ast.Load()))
			node.body.insert(0, astutil.makeAssignment(targetList, valueList))

		self._contextStack.popContext()
		return node
	
	def visit_Name(self, node) :
		if self.isRewritePhase() :
			node.id = self._contextStack.getCurrentContext().findNewName(node.id, node.id)
		return node
	
	def visit_Call(self, node) :
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
			newTest = self._logicMaker.makeTrue(newTest)
			node.test = newTest
			node.body, node.orelse = node.orelse, node.body
			if len(node.body) == 0 :
				node.body.append(ast.Pass())
		return self.generic_visit(node)

	def doRewriteConstant(self, node) :
		if self.isPreprocessPhase() :
			self._constantManager.foundConstant(node.value)
		elif self.isRewritePhase() :
			newNode = self._constantManager.getReplacedNode(node.value)
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
				if i == astMaxPhaseCount - 1 :
					document.setContent(ast.unparse(ast.fix_missing_locations(rootNode)))

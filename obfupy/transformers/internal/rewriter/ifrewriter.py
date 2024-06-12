from . import context
from . import rewriterutil
from . import gotowithif
from .. import astutil
from .. import util
from .. import reentryguard
from ... import rewriter

import ast
import copy
import random

class IfRewriter :
	def __init__(self, visitor) :
		self._visitor = visitor
		self._goto = gotowithif.GotoWithIf()

	def rewriteIf(self, node) :
		self._goto.reset()
		with reentryguard.AutoReentryGuard(self._visitor._reentryGuard, [ rewriterutil.guardId_compare, rewriterutil.guardId_boolOp ]) :
			node.test = self._visitor._doVisitNodeList(node.test)
			node.body = self._visitor._doVisitNodeList(node.body)
			node.orelse = self._visitor._doVisitNodeList(node.orelse)
		node = self._doRewriteIfCondition(node)
		return node

	def _doRewriteIfCondition(self, node) :
		if isinstance(node.test, ast.BoolOp) :
			if util.hasChance(2) :
				node.test = self._visitor.getNegationMaker().makeNegation(node.test)
				node.test = astutil.addNot(node.test)
		if isinstance(node.test, ast.BoolOp) :
			node = self._doRewriteAndOr(node) 
		return node

	def _doRewriteAndOr(self, node) :
		if isinstance(node.test.op, ast.And) :
			node = self._doRewriteAnd(node)
		else :
			node = self._doRewriteOr(node)
		return node

	def _doRewriteAnd(self, node) :
		node = self._doRewriteAndType1(node)
		return node

	def _doRewriteOr(self, node) :
		node = self._doRewriteOrType1(node)
		return node

	'''
	if(a and b and c) {X} else {Y}

	if(a) goto label1
	else goto labelElse
	label1: {
		if(b) goto label2
		else goto labelElse
	}
	label2: {
		if(c) goto label3
		else goto labelElse
	}
	label3: X
	labelElse: Y

	'''
	def _doRewriteAndType1(self, node) :
		self._goto.reset()
		labelElse = self._goto.getNewLable()
		labelList = [ self._goto.getNewLable() for _ in node.test.values ]
		for i in range(len(node.test.values)) :
			newNode = ast.If(
				test = node.test.values[i],
				body = util.ensureList(self._goto.gotoLabel(labelList[i])),
				orelse = util.ensureList(self._goto.gotoLabel(labelElse))
			)
			if i == 0 :
				self._goto.setBody(newNode)
			else :
				self._goto.addHandler(labelList[i - 1], newNode)
		self._goto.addHandler(labelList[-1], node.body)
		if len(node.orelse) == 0 :
			node.orelse = [ ast.Pass() ]
		self._goto.addHandler(labelElse, node.orelse)
		node = self._goto.makeNode()
		return node

	'''
	if(a or b or c) {X} else {Y}

	if(a) { goto labelDoIt }
	else { goto Label1 }
	label1: {
		if(b) { goto labelDoIt }
		else { goto Label2 }
	}
	label2: {
		if(c) { goto labelDoIt }
		else { goto Label3 }
	}
	labelDoIt: X
	label3: Y

	'''
	def _doRewriteOrType1(self, node) :
		self._goto.reset()
		labelDoIt = self._goto.getNewLable()
		labelList = [ self._goto.getNewLable() for _ in node.test.values ]
		for i in range(len(node.test.values)) :
			newNode = ast.If(
				test = node.test.values[i],
				body = util.ensureList(self._goto.gotoLabel(labelDoIt)),
				orelse = util.ensureList(self._goto.gotoLabel(labelList[i]))
			)
			if i == 0 :
				self._goto.setBody(newNode)
			else :
				self._goto.addHandler(labelList[i - 1], newNode)
		self._goto.addHandler(labelDoIt, node.body)
		if len(node.orelse) == 0 :
			node.orelse = [ ast.Pass() ]
		self._goto.addHandler(labelList[-1], node.orelse)
		node = self._goto.makeNode()
		return node

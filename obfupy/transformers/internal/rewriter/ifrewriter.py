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

	def rewriteIf(self, node) :
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
		return self._doRewriteIfConditionHelper(node)

	def _doRewriteIfConditionHelper(self, node) :
		node = copy.deepcopy(node)
		if isinstance(node.test, ast.BoolOp) :
			node = self._doRewriteAndOr(node) 
		elif isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not) :
			node = self._doRewriteNot(node)
		else :
			node = self._doRewriteCommon(node)
		return node
	
	def _doRewriteNot(self, node) :
		node = ast.If(
			test = node.test.operand,
			body = astutil.addPassIfNecessary(node.orelse),
			orelse = node.body
		)
		node = self._doRewriteIfConditionHelper(node)
		return node

	def _doRewriteCommon(self, node) :
		node = ast.If(
			test = self._visitor.getNegationMaker().makeNegation(node.test),
			body = astutil.addPassIfNecessary(node.orelse),
			orelse = node.body
		)
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
		goto = self._createGoto()
		labelElse = goto.getNewLable()
		labelList = [ goto.getNewLable() for _ in node.test.values ]
		for i in range(len(node.test.values)) :
			newNode = ast.If(
				test = node.test.values[i],
				body = util.ensureList(goto.gotoLabel(labelList[i])),
				orelse = util.ensureList(goto.gotoLabel(labelElse))
			)
			newNode = self._doRewriteIfConditionHelper(newNode)
			if i == 0 :
				goto.setBody(newNode)
			else :
				goto.addHandler(labelList[i - 1], newNode)
		randomizer = gotowithif.LabelOrderRandomizer()
		randomizer.addHandler(labelList[-1], node.body)
		node.orelse = astutil.addPassIfNecessary(node.orelse)
		randomizer.addHandler(labelElse, node.orelse)
		randomizer.takeOut(goto)

		node = goto.makeNode()
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
		goto = self._createGoto()
		labelDoIt = goto.getNewLable()
		labelList = [ goto.getNewLable() for _ in node.test.values ]
		for i in range(len(node.test.values)) :
			newNode = ast.If(
				test = node.test.values[i],
				body = util.ensureList(goto.gotoLabel(labelDoIt)),
				orelse = util.ensureList(goto.gotoLabel(labelList[i]))
			)
			newNode = self._doRewriteIfConditionHelper(newNode)
			if i == 0 :
				goto.setBody(newNode)
			else :
				goto.addHandler(labelList[i - 1], newNode)
		randomizer = gotowithif.LabelOrderRandomizer()
		randomizer.addHandler(labelDoIt, node.body)
		node.orelse = astutil.addPassIfNecessary(node.orelse)
		randomizer.addHandler(labelList[-1], node.orelse)
		randomizer.takeOut(goto)

		node = goto.makeNode()
		return node

	def _createGoto(self) :
		return gotowithif.GotoWithIf(self._visitor)

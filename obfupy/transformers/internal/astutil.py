# obfupy library
#
# Copyright (C) 2024 Wang Qi (wqking)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast

from . import util

_negationLogicalOps = [
	[ ast.Lt, ast.GtE ],
	[ ast.Gt, ast.LtE ],
	[ ast.Eq, ast.NotEq ],
	[ ast.In, ast.NotIn ],
	[ ast.Is, ast.IsNot ],
]

def getNegationLogicalOp(opType) :
	newOpType = None
	for item in _negationLogicalOps :
		if item[0] == opType :
			newOpType = item[1]
			break
		if item[1] == opType :
			newOpType = item[0]
			break
	return newOpType

# a < b -> a >= b
def _doMakeCompareNegation(node) :
	if len(node.comparators) != 1 :
		return None
	opType = type(node.ops[0])
	newOpType = getNegationLogicalOp(opType)
	if newOpType is None :
		return None
	return ast.Compare(
		left = node.left,
		ops = [ newOpType() ],
		comparators = node.comparators
	)

# a and b -> ~a or ~b
def _doMakeBoolOpNegation(node) :
	newValues = []
	for value in node.values :
		newNode = makeNegation(value)
		if newNode is None :
			return None
		newValues.append(newNode)
	newOpType = ast.Or
	if type(node.op) == ast.Or :
		newOpType = ast.And
	return ast.BoolOp(
		op = newOpType(),
		values = newValues
	)

def isLogicalNode(node) :
	if isinstance(node, ast.Compare) :
		return True
	if isinstance(node, ast.BoolOp) :
		for value in node.values :
			if not isLogicalNode(value) :
				return False
		return True
	if isinstance(node, ast.Constant) :
		return node.value is True or node.value is False
	if isinstance(node, ast.UnaryOp) :
		return isinstance(node.op, ast.Not)
	return False

def ensureLogicalNode(node) :
	if not isLogicalNode(node) :
		node = ast.Call(
			func = ast.Name(id = 'bool', ctx = ast.Load()),
			args = [ node ],
			keywords = []
		)
	return node

# make logoc not
def makeNegation(node) :
	if isinstance(node, ast.Compare) :
		newNode = _doMakeCompareNegation(node)
		if newNode is not None :
			return newNode
	if isinstance(node, ast.BoolOp) :
		newNode = _doMakeBoolOpNegation(node)
		if newNode is not None :
			return newNode
	if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not) :
		return node.operand
	if isinstance(node, ast.Constant) :
		if node.value is True :
			return makeConstant(False)
		elif node.value is False :
			return makeConstant(True)
	return addNot(node)

# a -> not a
def addNot(node) :
	return ast.UnaryOp(op = ast.Not(), operand = node)

def makeAssignment(targets, values) :
	if not isinstance(targets, list) :
		targets = [ targets ]
	if isinstance(values, list) :
		if len(values) == 1 :
			values = values[0]
		else :
			values = ast.Tuple(elts = values, ctx = ast.Load())
	node = None
	if len(targets) == 1 :
		node = ast.Assign(
				targets = targets,
				value = values
		)
	else :
		node = ast.Assign(
				targets = [ ast.Tuple(elts = targets, ctx = ast.Store()) ],
				value = values
		)
	return ast.fix_missing_locations(node)

def makeConstant(value) :
	return ast.Constant(value = value)

def _doGetNodeListFromAssignTargets(targetList, result) :
	if targetList is None :
		return
	if isinstance(targetList, list) :
		for target in targetList :
			_doGetNodeListFromAssignTargets(target, result)
	elif isinstance(targetList, ast.Tuple) :
		for target in targetList.elts :
			_doGetNodeListFromAssignTargets(target, result)
	else :
		result.append(targetList)

def getNodeListFromAssignTargets(targets) :
	result = []
	_doGetNodeListFromAssignTargets(targets, result)
	return result

def astToSource(node) :
	return ast.unparse(ast.fix_missing_locations(node))

def fixMissingLocations(node) :
	if isinstance(node, (list, tuple)) :
		for i in range(len(node)) :
			node[i] = fixMissingLocations(node[i])
	else :
		node = ast.fix_missing_locations(node)
	return node

def enumerateArguments(arguments, callback) :
	argList = [
		arguments.args,
		arguments.posonlyargs,
		arguments.kwonlyargs,
		[ arguments.vararg, arguments.kwarg ]
	]
	for item in argList :
		for argItem in item :
			if argItem is None :
				continue
			callback(argItem)

def isChildDocString(node) :
	# See get_raw_docstring in Python built-in ast.py
	if len(node.body) == 0 :
		return False
	child = node.body[0]
	if not isinstance(child, ast.Expr) :
		return False
	child = child.value
	if not isinstance(child, ast.Constant) or not isinstance(child.value, str) :
		return False
	return True

def removeDocString(node) :
	if not isChildDocString(node) :
		return node
	node.body = node.body[1 : ]
	if len(node.body) == 0 :
		node.body.append(ast.Pass())
	return node

def addPassIfNecessary(nodeList) :
	if nodeList is None or len(nodeList) == 0 :
		return [ ast.Pass() ]
	return nodeList

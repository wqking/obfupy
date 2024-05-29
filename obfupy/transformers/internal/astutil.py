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
	if not isinstance(values, list) :
		values = [ values ]
	if len(targets) == 1 :
		return ast.Assign(
				targets = targets,
				value = values
		)
	else :
		return ast.Assign(
				targets = [ ast.Tuple(elts = targets, ctx = ast.Store()) ],
				value = ast.Tuple(elts = values, ctx = ast.Load())
		)

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

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
	if isinstance(node, (ast.Name, ast.Constant)) :
		return addNot(node)
	return addNot(node)

# a -> not a
def addNot(node) :
	return ast.UnaryOp(op = ast.Not(), operand = node)

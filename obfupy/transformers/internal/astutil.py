import ast

from . import util

_negationLogicalOps = [
	[ ast.Lt, ast.GtE ],
	[ ast.Gt, ast.LtE ],
	[ ast.Eq, ast.NotEq ],
	[ ast.In, ast.NotIn ],
	[ ast.Is, ast.IsNot ],
]

# a < b -> a >= b
def _doMakeCompareNegation(node) :
	if len(node.comparators) != 1 :
		return util.failedResult
	opType = type(node.ops[0])
	newOpType = None
	for item in _negationLogicalOps :
		if item[0] == opType :
			newOpType = item[1]
			break
		if item[1] == opType :
			newOpType = item[0]
			break
	if newOpType is None :
		return util.failedResult
	return util.Result(ast.Compare(
		left = node.left,
		ops = [ newOpType() ],
		comparators = node.comparators
	))

# a and b -> ~a or ~b
def _doMakeBoolOpNegation(node) :
	newValues = []
	for value in node.values :
		result = makeNegation(value)
		if not result.isSuccess() :
			return util.failedResult
		newValues.append(result.getValue())
	newOpType = ast.Or
	if type(node.op) == ast.Or :
		newOpType = ast.And
	return util.Result(ast.BoolOp(
		op = newOpType(),
		values = newValues
	))

# make logoc not
def makeNegation(node) :
	if isinstance(node, ast.Compare) :
		result = _doMakeCompareNegation(node)
		if result.isSuccess() :
			return result
	if isinstance(node, ast.BoolOp) :
		return _doMakeBoolOpNegation(node)
	if isinstance(node, (ast.Name, ast.Constant)) :
		return addNot(node)
	return addNot(node)

# a -> not a
def addNot(node) :
	return util.Result(ast.UnaryOp(op = ast.Not(), operand = node))

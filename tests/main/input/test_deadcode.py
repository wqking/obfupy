def deadCodeInFunc1(n) :
	itemList = [ 1, 2, 3 ]
	if n in itemList :
		return True
	return False
	raise Exception("What?")
	itemList = None

def deadCodeInFunc2(n) :
	itemList = [ 1, 2, 3 ]
	if n in itemList :
		return True
	raise Exception("What?")
	return False
	itemList = None

def deadCodeInForWhile() :
	for i in range(5) :
		if i < 0 :
			continue
		break
		i = 6
	while i < 0 :
		continue
		i = 6

def deadIfCondition() :
	if 1 + 2 > 0 :
		print("Good")
	else :
		print("You can't see this")

	if 1 + 2 * 100 < 0 + 50 * 4 :
		print("You can't see this, 222")
	else :
		print("Good 222")

	if str(35) != "35" :
		print("You can't see this, 333")
	elif ord('a') != 97 :
		print("You can't see this, 444")
	else :
		print("Good 444")

def deadCodeOf__debug__() :
	if __debug__ :
		print("You can't see this, 111")
	else :
		print("Good 111")

	if __debug__ or 1 < 2:
		print("Good 222")
	else :
		print("You can't see this, 222")

	if __debug__ and 1 < 2:
		print("You can't see this, 333")
	else :
		print("Good 333")

def test_deadBoolOp() :
	i = 5
	a = (1 > 0) and i > 3
	assert a
	a = (1 < 0) and i > 3
	assert not a
	a = (1 > 0) or i > 6
	assert a
	a = (1 < 0) or i == 5
	assert a

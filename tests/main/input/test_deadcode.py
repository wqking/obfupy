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

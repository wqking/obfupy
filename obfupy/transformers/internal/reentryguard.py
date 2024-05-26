class ReentryGuard :
	def __init__(self) :
		self._guardMap = {}

	def enter(self, guardId) :
		if isinstance(guardId, list) :
			for i in guardId :
				self.enter(i)
		else :
			if guardId in self._guardMap :
				self._guardMap[guardId] += 1
			else :
				self._guardMap[guardId] = 1

	def leave(self, guardId) :
		if isinstance(guardId, list) :
			for i in guardId :
				self.leave(i)
		else :
			assert guardId in self._guardMap
			assert self._guardMap[guardId] > 0
			self._guardMap[guardId] -= 1

	def isEntered(self, guardId) :
		if isinstance(guardId, list) :
			for i in guardId :
				if i in self._guardMap and self._guardMap[i] > 0 :
					return True
		else :
			if guardId in self._guardMap and self._guardMap[guardId] > 0 :
				return True
		return False
	
class AutoReentryGuard :
	def __init__(self, reentryGuard, guardId) :
		self._reentryGuard = reentryGuard
		self._guardId = guardId

	def __enter__(self) :
		self._reentryGuard.enter(self._guardId)
		return self

	def __exit__(self, type, value, traceBack) :
		self._reentryGuard.leave(self._guardId)


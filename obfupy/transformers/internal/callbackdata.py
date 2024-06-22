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

from . import optionsutil

import copy

def _shouldSkipFile(callback, fileName) :
	options = _invokeCallback(callback, _OptionCallbackData(fileName, optionsutil.EmptyOptions()))
	return (
		options is not None
		and not options.enabled
	)

def _invokeCallback(callback, data) :
	if callback is None :
		return None
	callback(data)
	if data._isModified() :
		return data._makeOptions()
	return None

class _OptionCallbackData :
	def __init__(self, fileName, options) :
		self._fileName = fileName
		if options is None :
			options = optionsutil.EmptyOptions()
		options._resetModified()
		self._original = options
		self._options = None
		self._needCopy = True

	def getOptions(self) :
		if self._options is None :
			self._options = copy.deepcopy(self._original)
		return self._options

	def getFileName(self) :
		return self._fileName
	
	def isFile(self) :
		return True

	def _isModified(self) :
		return self._options is not None and self._options._isModified()

	def _makeOptions(self) :
		return self._options


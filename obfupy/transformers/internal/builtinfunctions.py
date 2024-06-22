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

builtinFunctionList = [
	"abs",
	"aiter",
	"all",
	"anext",
	"any",
	"ascii",
	"bin",
	"bool",
	"breakpoint",
	"bytearray",
	"bytes",
	"callable",
	"chr",
	"classmethod",
	"compile",
	"complex",
	"delattr",
	"dict",
	"dir",
	"divmod",
	"enumerate",
	"eval",
	"exec",
	"filter",
	"float",
	"format",
	"frozenset",
	"getattr",
	"globals",
	"hasattr",
	"hash",
	"help",
	"hex",
	"id",
	"input",
	"int",
	"isinstance",
	"issubclass",
	"iter",
	"len",
	"list",
	"locals",
	"map",
	"max",
	"memoryview",
	"min",
	"next",
	"object",
	"oct",
	"open",
	"ord",
	"pow",
	"print",
	"property",
	"range",
	"repr",
	"reversed",
	"round",
	"set",
	"setattr",
	"slice",
	"sorted",
	"staticmethod",
	"str",
	"sum",
	"tuple",
	"type",
	"vars",
	"zip",
]

builtinFunctionMap = dict.fromkeys(builtinFunctionList, True)

# Don't rename "super", it will raise exception "__class__ cell not found"

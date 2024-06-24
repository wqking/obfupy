# https://github.com/keon/algorithms.git, branch master, commit cad4754bc71742c2d6fcbd3b92ae74834d359844

import general
import helper

import os

args = helper.parseCommandLine()
general.obfuscateProject()

os.chdir(args['output'])
print(os.getcwd())
os.system('python -m pytest -s tests')

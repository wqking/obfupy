# https://github.com/pallets/flask.git, branch main, commit 0d2100ed17d24b2a30594729b99feebe76839bc5

import general
import helper

import os

args = helper.parseCommandLine()
general.obfuscateProject()

os.chdir(args['output'])
print(os.getcwd())
os.system('tox')

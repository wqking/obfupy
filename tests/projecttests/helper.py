import argparse

def parseCommandLine() :
	parser = argparse.ArgumentParser(description = 'Obfuscate project')
	parser.add_argument('--input', dest = 'input', type = str, required = True)
	parser.add_argument('--output', dest = 'output', type = str, required = True)
	args = parser.parse_args()
	return {
		'input' : args.input,
		'output' : args.output,
	}

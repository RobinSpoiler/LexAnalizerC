import re

newline = 'newline'

identifier = 'ident'

loopsList = ['while', 'for']

arithmeticOp = ['+', '-', '*', '/', '//', '**', '%']
assignmentOp = ["=", "+=", "-=", "*=", "/=", "//=", "%=", "**="]
comparisonOp = ["==", "!=", "<", ">", "<=", ">="]
operatorsList = arithmeticOp + assignmentOp + comparisonOp 

"""
returns:
	{ lineNumber: int, indices: [[int, int] ...] }
"""
def formatInfo(lineNumber, indices):
	return {'lineNumber': lineNumber, 'indices': indices }



def getTokensFromALine(tokens, matchLine):
	matchedTokens = []
	for token in tokens:
		line = int(token[2])
		if line == matchLine + 1:
			matchedTokens.append(token)
	return matchedTokens


# Separates the code into blocks, and puts the toekns into their respective blocks
def separateCode(linesOfCode, tokens):
	main = {"code": "", "tokens": []}
	functions = {"code": "", "tokens": []}
	loops = {"code": "", "tokens": []}
	conditionals = {"code": "", "tokens": []}
	
	functionKeyword = "def"
	loopKeywords = ["while", "for"]
	conditionalKeywords = ["if", "elif", "else"]

	currentSection = "main"
	indents = 0
	for lineIndex in range(len(linesOfCode)):
		currentLine = linesOfCode[lineIndex]

		# If the current line is the start of a function then append it to the function maps
		if currentLine.startswith(functionKeyword) and not currentLine[len(functionKeyword)].isalpha():
			currentSection = "function"
			indents = 0
		
		# Check if the current line is the start of a loop 
		for key in loopKeywords:
			if currentLine.startswith(key) and not currentLine[len(key)].isalpha():
				currentSection = "loop"
				indents = 0


		# Check if the current line is the start of a conditional 
		for key in conditionalKeywords:
			if currentLine.startswith(key) and not currentLine[len(key)].isalpha():
				currentSection = "conditional"
				indents = 0


		tokensOnThatLine = getTokensFromALine(tokens, lineIndex)
		lastToken =  tokensOnThatLine[-1] if len(tokensOnThatLine) > 0 else [None]

		if (currentSection == "function"):
			functions["code"] += currentLine + '\n'
			functions["tokens"] += tokensOnThatLine
		elif (currentSection == "loop"):
			loops["code"] += currentLine + '\n'
			loops["tokens"] += tokensOnThatLine
		elif (currentSection == "conditional"):
			conditionals["code"] += currentLine + '\n'
			conditionals["tokens"] += tokensOnThatLine
		elif (currentSection == "main"):
			main["code"] += linesOfCode[lineIndex] + '\n'
			main["tokens"] += tokensOnThatLine

		if lastToken[0] == "indent":
			indents += 1
		if lastToken[0] == "dedent":
			indents -= 1
			lastTokenIndex = len(tokensOnThatLine) - 2
			while tokensOnThatLine[lastTokenIndex][0] == "dedent" and indents > 0:
				indents -= 1
				lastTokenIndex -= 1
			if indents == 0:
				currentSection = "main"

	return {"main": main, "functions": functions, "loops": loops, "conditionals": conditionals}


def getCharacteristics(tokens, linesOfCode):
	# Requires tokens
	ints = 0
	intsIndexes = []
	strings = 0
	stringIndexes = []
	floats = 0
	floatsIndexes = []
	identifiers = 0
	identifiersIndexes = []
	loops = 0
	loopsIndexes = []
	operators = 0
	operatorsIndexes = []
	# Requires linesOfCode
	arguments = 0
	argumentsIndexes = []

	# =============== Get all semantic values from tokens
	prevLine = '0'
	currentLine = 0
	indexesKeys = ["int", 'float', 'string', 'ident', 'loops', 'operators', 'arguments']
	currentIndexes = {}
	for key in indexesKeys:
		currentIndexes[key] = []
	for token, index, line in tokens:
		# Since the line has changed, we must add the pre-existing values
		if prevLine != line:
			for key, value in currentIndexes.items():
				if len(value) > 0:
					formattedInfo = formatInfo(currentLine, value)
					if key == "int":
						intsIndexes.append(formattedInfo)
					elif key == "float":
						floatsIndexes.append(formattedInfo)
					elif key == "string":
						stringIndexes.append(formattedInfo)
					elif key == "ident":
						identifiersIndexes.append(formattedInfo)
					elif key == "loops":
						loopsIndexes.append(formattedInfo)
					elif key == "operators":
						operatorsIndexes.append(formattedInfo)
					# Restart that index
					currentIndexes[key] = []
			currentLine += 1
			prevLine = line

		# tokenIndex = 
		if token == "int":
			ints += 1
			currentIndexes['int'].append([int(x) for x in index.split('-')])
		elif token == "strdata":
			strings += 1
			start, end = [int(x) for x in index.split('-')]
			currentIndexes['string'].append([start - 1, end + 1])
		elif token == "float":
			floats += 1
			currentIndexes['float'].append([int(x) for x in index.split('-')])
		elif token == "ident":
			identifiers += 1
			currentIndexes['ident'].append([int(x) for x in index.split('-')])
		elif token in loopsList:
			loops += 1
			currentIndexes['loops'].append([int(x) for x in index.split('-')])
		elif token in operatorsList:
			operators += 1
			currentIndexes['operators'].append([int(x) for x in index.split('-')])
	# Add last line of indexes
	for key, value in currentIndexes.items():
		if len(value) > 0:
			formattedInfo = formatInfo(currentLine, value)
			if key == "int":
				intsIndexes.append(formattedInfo)
			elif key == "float":
				floatsIndexes.append(formattedInfo)
			elif key == "string":
				stringIndexes.append(formattedInfo)
			elif key == "ident":
				identifiersIndexes.append(formattedInfo)
			elif key == "loops":
				loopsIndexes.append(formattedInfo)
			elif key == "operators":
				operatorsIndexes.append(formattedInfo)

	# =========== Get the arguments from linesOfCode
	argumentsRegex = r"[a-zA-Z_][a-zA-Z0-9_]*\(([a-zA-Z0-9,_\s\"\'\.]*)\)"

	for line in linesOfCode:
		match = re.search(argumentsRegex, line)
		if match:
			captured_args = match.group(1)
			split_args = [a.strip() for a in captured_args.split(",")]
			arguments += len(split_args)
	return {
		"enteros": {"cantidad": ints, "location": intsIndexes},
		"strings": {"cantidad": strings, "location": stringIndexes},
		"floats": {"cantidad": floats, "location": floatsIndexes},
		"identifiers": {"cantidad": identifiers, "location": identifiersIndexes},
		"loops": {"cantidad": loops, "location": loopsIndexes},
		"operators": {"cantidad": operators, "location": operatorsIndexes},
		"arguments": {"cantidad": arguments, "location": argumentsIndexes},
	}


def getSemanticValues(linesOfCode, tokens):
	blocks = separateCode(linesOfCode, tokens)
	for key, value in blocks.items():
		code = value["code"]
		block_tokens = value["tokens"]
		characteristics = getCharacteristics(block_tokens, code)
		blocks[key]["characteristics"] = characteristics
	return blocks	

def getSemanticPercentage(semantic1, semantic2):
	percentage = 0
	for key, value1 in semantic1.items():
		# Getting the characteristics of both files
		value2 = semantic2[key]
		charact1 = value1['characteristics']
		charact2 = value2['characteristics']
		counterNoZeros = 0
		counterWithZeros = 0
		# Comparing each of the characteristics to check if they have the same amount of ints, floats, etc.
		for charactKey, charactValue1 in charact1.items():
			charactValue2 = charact2[charactKey]
			if charactValue1['cantidad'] == charactValue2['cantidad'] and charactValue1['cantidad'] > 0:
				counterNoZeros += 1
			if charactValue1['cantidad'] == charactValue2['cantidad']:
				counterWithZeros += 1
		if counterWithZeros == 7:
			percentage += (7/28)
		else:
			percentage += counterNoZeros
	return percentage * 100
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


def getVariables(tokens):
	lineNumber = 1
	indexes = []
	variables = []
	for token, index, _line in tokens:
		if token == newline:
			if len(indexes) > 0:
				variables.append(formatInfo(lineNumber, indexes))
			indexes = []
			lineNumber += 1
		if token == identifier:
			# Index has format "17-18"
			start, end = [int(x) for x in index.split('-')]
			indexes.append([start, end])
	return variables
			
def getLoops(tokens):
	lineNumber = 1
	indexes = []
	loops = []
	for token, index, _line in tokens:
		if token == newline:
			if len(indexes) > 0:
				loops.append(formatInfo(lineNumber, indexes))
			indexes = []
			lineNumber += 1
		if token in loopsList:
			# Index has format "17-18"
			start, end = [int(x) for x in index.split('-')]
			indexes.append([start, end])
	return loops

def getOperators(tokens):
	lineNumber = 1
	indexes = []
	operators = []
	for token, index, _line in tokens:
		if token == newline:
			if len(indexes) > 0:
				operators.append(formatInfo(lineNumber, indexes))
			indexes = []
			lineNumber += 1
		if token in operatorsList:
			# Index has format "17-18"
			start = int(index.split('-')[0])
			end = start + len(token)
			indexes.append([start, end])
	return operators


def getFunctions(linesOfCode):
	# matches: "  def identifier_439"
	functionRegex = r"^\s*def\s[a-zA-Z_][a-zA-Z0-9_]*"
	lineNumber = 1
	funciones = []
	for line in linesOfCode:
		if not line.startswith("#") and len(line) > 0:
			match = re.search(functionRegex, line)
			if match:
				funciones.append(formatInfo(lineNumber, [[match.start() + 1, match.end() + 1]]))
			lineNumber += 1
	return funciones

def getArguments(linesOfCode):
	# matches: "  comprar_carro(30000, "Nissan", "Sentra", 2019)"
	argRegex = r"[a-zA-Z_][a-zA-Z0-9_]*\(([a-zA-Z0-9,_\s\"\'\.]*)\)"
	lineNumber = 1
	args = []
	indexes = []
	for line in linesOfCode:
		if not line.startswith("#") and len(line) > 0:
			match = re.search(argRegex, line)
			if match:
				# Get only the arguments
				captured_args = match.group(1)
				# Find where the arguments start
				index_count = match.start(1)
				# Remove what is before the args
				line = line[index_count:]
				# Split arguments and remove extra spaces
				split_args = [a.strip() for a in captured_args.split(",")]
				# For each argument, get the starting and ending position
				for arg in split_args:
					start_index = line.find(arg) + index_count
					end_index = start_index + len(arg)
					indexes.append([start_index + 1, end_index + 1])
					index_count = end_index
					# Removing part of the line to avoid repetitions
					line = line[(len(arg) + line.find(arg)):]
				args.append(formatInfo(lineNumber, indexes))
			lineNumber += 1
			indexes = []
	return args

def getTokensFromALine(tokens, matchLine):
	matchedTokens = []
	for token in tokens:
		line = token[2]
		if line == matchLine + 1:
			matchedTokens.append(token)
	return matchedTokens

def getFirstToken(tokens, matchLine):
	lastToken = None
	for token in tokens:
		line = int(token[2])
		if line == matchLine:
			lastToken = token
	return lastToken

def separateCode(linesOfCode, tokens):
	main = {"code": "", "tokens": []}
	functions = {"code": "", "tokens": []}
	loops = {"code": "", "tokens": []}
	conditionals = {"code": "", "tokens": []}
	
	functionKeyword = "def"
	loopKeywords = ["while", "for"]
	conditionalKeywords = ["if", "elif", "else"]

	
	for lineIndex in range(len(linesOfCode)):

		# If the current line is the start of a function then append it to the function maps
		if linesOfCode[lineIndex].startswith(functionKeyword) and linesOfCode[lineIndex][len(functionKeyword)]:

			functions["code"] += linesOfCode[lineIndex] + '\n'
			functions["tokens"] += getTokensFromALine(tokens, lineIndex)
			lineIndex += 1

			while lineIndex < len(linesOfCode):
				firstToken = getFirstToken(tokens, lineIndex)
				print("fToken", firstToken)
				if firstToken[0] == "dedent":
					lineIndex -= 1
					break
				functions["code"] += linesOfCode[lineIndex] + '\n'
				functions["tokens"] += getTokensFromALine(tokens, lineIndex)
				lineIndex += 1
		else:
			# Check if the current line is the start of a loop 
			isLoop = False
			for key in loopKeywords:
				if linesOfCode[lineIndex].startswith(key) and not linesOfCode[lineIndex][len(key)].isalpha():
					isLoop = True

			# Check if the current line is the start of a conditional 
			isConditional = False
			for key in conditionalKeywords:
				if linesOfCode[lineIndex].startswith(key) and not linesOfCode[lineIndex][len(key)].isalpha():
					isConditional = True

			# If it's a loop then append it to the loop map
			if isLoop:
				loops["code"] += linesOfCode[lineIndex] + '\n'
				loops["tokens"] += getTokensFromALine(tokens, lineIndex)
				lineIndex += 1
				while lineIndex < len(linesOfCode):
					firstToken = getFirstToken(tokens, lineIndex)
					if firstToken[0] == "dedent":
						lineIndex -= 1
						break
					loops["code"] += linesOfCode[lineIndex] + '\n'
					loops["tokens"] += getTokensFromALine(tokens, lineIndex)
					lineIndex += 1
			
			# If it's a conditional, append it to the conditionals
			elif isConditional:
				print("isConditional")
				conditionals["code"] += linesOfCode[lineIndex] + '\n'
				conditionals["tokens"] += getTokensFromALine(tokens, lineIndex)
				lineIndex += 1
				while lineIndex < len(linesOfCode):
					firstToken = getFirstToken(tokens, lineIndex)
					if firstToken[0] == "dedent":
						lineIndex -= 1
						break
					conditionals["code"] += linesOfCode[lineIndex] + '\n'
					conditionals["tokens"] += getTokensFromALine(tokens, lineIndex)
					lineIndex += 1
			
			else:
				main["code"] += linesOfCode[lineIndex] + '\n'
				main["tokens"] += getTokensFromALine(tokens, lineIndex)
				
				
	return {"main": main, "functions": functions, "loops": loops, "conditionals": conditionals}


def getSemanticValues(linesOfCode, tokens):
	# linesOfCode = ["def hello():", "	print("Hello")"]
	# tokens = [("reserved", 1-3, 1), ]

	"""
	num1 = 10
	num2 = 14
	num3 = 12
	if (num1 >= num2) and (num1 >= num3):
		largest = num1
	elif (num2 >= num1) and (num2 >= num3):
		largest = num2
	else:
		largest = num3
	print("The largest number is", largest)
	def printHola():
		print("hola")
   """
		
	return {
		'variables': getVariables(tokens),
		'ciclos': getLoops(tokens),
		'operadores': getOperators(tokens),
		'funciones': getFunctions(linesOfCode),
		'argumentos': getArguments(linesOfCode)
	}

"""
{
	variables: [
		{ lineNumber: int (desde 1), indices: [[int, int] ... }
	]
	ciclos: [
		{ lineNumber: int (desde 1), indices: [[int, int] ... }
	]
	operadores: [
		{ lineNumber: int (desde 1), indices: [[int, int] ... }
	]
	funciones: [
		{ lineNumber: int (desde 1), indices: [[int, int] ... }
	]
	argumentos: [
		{ lineNumber: int (desde 1), indices: [[int, int] ... }
	]
}
"""
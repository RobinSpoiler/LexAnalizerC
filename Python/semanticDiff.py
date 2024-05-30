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
	for token, index in tokens:
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
	for token, index in tokens:
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
	for token, index in tokens:
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

def getSemanticValues(linesOfCode, tokens):
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
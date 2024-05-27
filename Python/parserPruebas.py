import sys, re
from pythonparser import source, lexer, diagnostic
import difflib

# -------Comparing files as plain text--------
def getIndexes(startIndex, endIndex, textFile):
    lineNumber = 1
    filteredLines = textFile.split('\n')
    for line in filteredLines:
        if startIndex < len(line):
            break
        # Sum one to include the line breaks
        startIndex -= len(line) + 1
        endIndex -= len(line) + 1
        lineNumber += 1

    indexes = [startIndex, endIndex]

    return {'lineNumber': lineNumber,
            'indexes': indexes
            }

def getCleanList(data):
    merged = {}
    for entry in data:
        lineNumber = entry['lineNumber']
        indexes = entry['indexes']
        if lineNumber in merged:
            merged[lineNumber]['indexes'].append(indexes)
        else:
            merged[lineNumber] = {'lineNumber': lineNumber, 'indexes': [indexes]}
    return list(merged.values())


def getPlainText(fileName):
    plainText = None
    with open(fileName) as file:
        plainText =  file.read()
    return plainText

def getTextSimilarityPercentage(textFile1, textFile2):
    similarityFile1 = []
    similarityFile2 = []

    s = difflib.SequenceMatcher(None, textFile1, textFile2)
    for block in s.get_matching_blocks():
        startIndexFile1 = block.a
        startIndexFile2 = block.b
        similaritySize = block.size
        # Change to the corresponding limit of size
        if similaritySize > 1:
            similarityFile1.append(getIndexes(startIndexFile1, startIndexFile1 + similaritySize - 1, textFile1))
            similarityFile2.append(getIndexes(startIndexFile2, startIndexFile2 + similaritySize - 1, textFile2))
    
    cleanSimilarityFile1 = getCleanList(similarityFile1)
    cleanSimilarityFile2 = getCleanList(similarityFile2)
    return cleanSimilarityFile1, cleanSimilarityFile2


def compareFilesAsText(fileName1, fileName2):
    textFile1 = getPlainText(fileName1)
    textFile2 = getPlainText(fileName2)
    similarityFile1, similarityFile2 = getTextSimilarityPercentage(textFile1, textFile2)
    return similarityFile1, similarityFile2

# -------Comparing files with tokens--------

# 
def getBuffer(filecontent, filename):
    buf = None
    # Check if the file exists and has a size greater than zero
    # if file and file.seekable() and file.tell() > 0:
        # Move the pointer to the beginning of the file
        # file.seek(0)
        # with io.BytesIO(file.read()) as f:
            # Print file content for debugging
            # file_content = f.read()
    buf = source.Buffer(filecontent, filename)
    # else:
    #     print("Error: File is empty or does not exist.")
    return buf


def getTokenSimilarityPercentage(tokensFile1, tokensFile2):
    return difflib.SequenceMatcher(None, tokensFile1, tokensFile2).ratio() * 100

def getTokensValue(buffer, engine):
    tokensFile = []
    for token in lexer.Lexer(buffer, (3,4), engine):
        if token.value == None:
            tokensFile.append(token.kind)
        else:
            tokensFile.append(token.value)
    return tokensFile

def getTokensKind(buffer, engine):
    tokensKindFile = []
    tokensValueFile = []
    tokensList = []
    
    for token in lexer.Lexer(buffer, (3,4), engine):
        tokensKindFile.append(token.kind)
        tokensList.append((token.kind, str(token.loc)[11:]))
        if token.value == None:
            tokensValueFile.append(token.kind)
        else:
            tokensValueFile.append(token.value)
    print("variabels",cleanTokensList(tokensList))
    print("AAAA tokensList: ", tokensList)

    return tokensKindFile, tokensValueFile, tokensList

def cleanTokensList(tokensList):
    variables = []
    for registroToken in tokensList:
        linea = registroToken[1][:2]
        print(registroToken[1].replace(linea, ''))
        variables.append((registroToken[0],registroToken[1].replace(linea, '')))
    return variables

    
def compareFilesWithTokens(fileName1, fileName2,fileName1content, fileName2content):
    
    bufferFile1 = getBuffer(fileName1content, fileName1)
    bufferFile2 = getBuffer(fileName2content, fileName2)

    # Engine
    engine = diagnostic.Engine()

    # Getting tokens of file 1
    tokensFile1Kind, tokensFile1Value, tokensList1 = getTokensKind(bufferFile1, engine)
    # Getting tokens of file 2
    tokensFile2Kind, tokensFile2Value, tokensList2  = getTokensKind(bufferFile2, engine)
    
    # Getting similarity between two files
    similarityKind = getTokenSimilarityPercentage(tokensFile1Kind, tokensFile2Kind)
    similarityValue = getTokenSimilarityPercentage(tokensFile1Value, tokensFile2Value)
    print("Comparing tokens by kind: they are " + str(similarityKind) +"% similar")
    print("Comparing tokens by value: they are " + str(similarityValue) +"% similar")
    # print("tokensList1: ", tokensList1)
    # print('\n')
    # print("tokensList2: ", tokensList2)
    return similarityKind, similarityValue, tokensList1, tokensList2

files = ["prueba1.py", "prueba2.py"] # "prueba3.py", "prueba4.py", "prueba5.py"]

for file1 in files:
    for file2 in files:
        if file1 != file2:
            print("\nComparing file " + file1 +" with " + file2)
            filename1 = file1
            filename2 = file2
            uno = getPlainText(file1)
            dos = getPlainText(file2)
            
            print(uno)
            print(dos)
            
            compareFilesWithTokens(file1, file2, uno, dos)
            # compareFilesAsText(file1, file2)
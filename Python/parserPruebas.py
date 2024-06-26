import sys, re
from pythonparser import source, lexer, diagnostic
import difflib

# -------Comparing files as plain text--------
def getIndexes(startIndex, endIndex, textFile):
    lineNumber = 1
    filteredLines = textFile.split('\n')
    similarities = []
    
    for line in filteredLines:
        # if the start index is bigger than the end, then we're done getting the indexes
        if startIndex >= endIndex:
            break

        lineLength = len(line)

        # If the start index is less than the length of the line it means that we can start getting indexes
        if startIndex < lineLength:
            # If the end index is less than the line length it means that we're done getting indexes
            if endIndex < lineLength:
                # the indexes will be the start index + 1 because it's 1-indexed and end index +2 because of that and because it's exclusive
                indexes = [startIndex + 1, endIndex + 2]
                similarities.append({'lineNumber': lineNumber, 'indices': indexes})
                break
            
            # If the end index is equal to the line length it means that it included the break line character, so we only sum 1 to it
            if endIndex == lineLength:
                indexes = [startIndex + 1, endIndex + 1]
                similarities.append({'lineNumber': lineNumber, 'indices': indexes})
                break

            # If the end index is bigger than to the length of the line
            if endIndex > lineLength:
                indexes = [startIndex + 1, lineLength + 1]
                similarities.append({'lineNumber': lineNumber, 'indices': indexes})
                startIndex = 0
                endIndex -= (lineLength + 1)
        # If the index is equal to the lineLenght, it means that is the first character of the next line
        elif startIndex == lineLength:
            startIndex = 0
            endIndex -= lineLength + 1
        else:
            # Substract the length of the line + 1 of the line break
            startIndex -= (lineLength + 1)
            endIndex -= (lineLength + 1)
        
        lineNumber += 1

    return similarities

def getCleanList(data):
    merged = {}
    for entry in data:
        lineNumber = entry['lineNumber']
        indexes = entry['indices']
        if lineNumber in merged:
            merged[lineNumber]['indices'].append(indexes)
        else:
            merged[lineNumber] = {'lineNumber': lineNumber, 'indices': [indexes]}
    return list(merged.values())


def getPlainText(fileName):
    plainText = None
    with open(fileName) as file:
        plainText =  file.read()
    return plainText

def getTextSimilarityIndexes(textFile1, textFile2):
    similarityFile1 = []
    similarityFile2 = []

    s = difflib.SequenceMatcher(None, textFile1, textFile2)
    for block in s.get_matching_blocks():
        startIndexFile1 = block.a
        startIndexFile2 = block.b
        similaritySize = block.size
        # Change to the corresponding limit of size
        if similaritySize > 3:
            similarityFile1 += getIndexes(startIndexFile1, startIndexFile1 + similaritySize - 1, textFile1)
            similarityFile2 += getIndexes(startIndexFile2, startIndexFile2 + similaritySize - 1, textFile2)

    cleanSimilarityFile1 = getCleanList(similarityFile1)
    cleanSimilarityFile2 = getCleanList(similarityFile2)
    return {"texto": cleanSimilarityFile1}, {"texto": cleanSimilarityFile2}


def compareFilesAsText(fileName1, fileName2):
    textFile1 = getPlainText(fileName1)
    textFile2 = getPlainText(fileName2)
    similarityFile1, similarityFile2 = getTextSimilarityIndexes(textFile1, textFile2)
    return similarityFile1, similarityFile2

# -------Comparing files with tokens--------

# 
def getBuffer(filecontent, filename):
    buf = None
    buf = source.Buffer(filecontent, filename)
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
    return similarityKind, similarityValue, tokensList1, tokensList2

files = ["prueba2.py", "prueba5.py"] # "prueba3.py", "prueba4.py", "prueba5.py"]

for file1 in files:
    for file2 in files:
        if file1 != file2:
            print("\nComparing file " + file1 +" with " + file2)
            filename1 = file1
            filename2 = file2
            
            # compareFilesWithTokens(file1, file2, uno, dos)
            # compareFilesAsText(file1, file2)
compareFilesAsText(files[0], files[1])
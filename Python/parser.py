import sys, re
from pythonparser import source, lexer, diagnostic
import difflib
import io

# -------Comparing files as plain text--------

def getPlainText(file):
    plainText = None
    with io.BytesIO(file.read()) as f:  # Lee el contenido del archivo en un buffer en memoria
        plainText = f.read()
    return plainText

def getIndexes(startIndex, endIndex, textFile):
    lineNumber = 1
    filteredLines = textFile.split('\n')
    
    for line in filteredLines:
        lineLength = len(line)
        if startIndex < lineLength:
            # Some lines have \t so we avoid including that with this statement
            if endIndex > lineLength:
                endIndex = lineLength - 1
            break
        # If the index is equal to the lineLenght, it means that is the first character of the next line
        if startIndex == lineLength:
            startIndex -= lineLength
            endIndex -= lineLength
            lineNumber += 1
            break
        # Substract the length of the line + 1 of the line break
        startIndex -= (lineLength + 1)
        endIndex -= (lineLength + 1)
        lineNumber += 1
    
    indexes = [startIndex + 1, endIndex + 2]
    return {'lineNumber': lineNumber,
            'indices': indexes
            }

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
            similarityFile1.append(getIndexes(startIndexFile1, startIndexFile1 + similaritySize - 1, textFile1))
            similarityFile2.append(getIndexes(startIndexFile2, startIndexFile2 + similaritySize - 1, textFile2))
    
    cleanSimilarityFile1 = getCleanList(similarityFile1)
    cleanSimilarityFile2 = getCleanList(similarityFile2)
    return {"texto": cleanSimilarityFile1}, {"texto": cleanSimilarityFile2}


def compareFilesAsText(textFile1, textFile2):
    similarityFile1, similarityFile2 = getTextSimilarityIndexes(textFile1, textFile2)
    return similarityFile1, similarityFile2

def getTextSimilarityPercentage(textFile1, textFile2):
    return difflib.SequenceMatcher(None, textFile1, textFile2).ratio() * 100

# -------Comparing files with tokens--------
def getBuffer(filecontent, filename):
    buf = None
    buf = source.Buffer(filecontent, filename)
    return buf

def getTokenSimilarityPercentage(tokensFile1, tokensFile2):
    return difflib.SequenceMatcher(None, tokensFile1, tokensFile2).ratio() * 100

def getTokensKindAndValue(buffer, engine):
    tokensKindFile = []
    tokensValueFile = []
    tokensList = []
    
    
    lex = lexer.Lexer(buffer, (3,4), engine)
    for token in lex:
        tokensList.append((token.kind, str(token.loc)[11:]))
        tokensKindFile.append(token.kind)
        if token.value is None:
            tokensValueFile.append(token.kind)
        else:
            tokensValueFile.append(token.value)
    return tokensKindFile, tokensValueFile, tokensList

def cleanTokensList(tokensList):
    cleanTokensList = []
    for registroToken in tokensList:
        dospuntos = registroToken[1].find(':')
        linea = registroToken[1][:dospuntos]
        cleanTokensList.append((registroToken[0],registroToken[1].replace(linea+":", '')))
    return cleanTokensList

def compareFilesWithTokens(fileName1, fileName2,filecontent1, filecontent2):
    bufferFile1 = getBuffer(filecontent1, fileName1)
    bufferFile2 = getBuffer(filecontent2, fileName2)

    # Engine
    engine = diagnostic.Engine()
    # Getting tokens of file 1
    tokensFile1Kind, tokensFile1Value,tokensList1 = getTokensKindAndValue(bufferFile1, engine)
    # Getting tokens of file 2
    tokensFile2Kind, tokensFile2Value, tokensList2  = getTokensKindAndValue(bufferFile2, engine)
    
    # Getting similarity between two files by kind
    similarityKind = getTokenSimilarityPercentage(tokensFile1Kind, tokensFile2Kind)
    # print("Comparing tokens by kind: they are " + str(similarityKind) +"% similar")

    # Getting similarity between two files by value
    similarityValue = getTokenSimilarityPercentage(tokensFile1Value, tokensFile2Value)
    tokensList1 = list(tokensList1)
    tokensList2 = list(tokensList2)

    return similarityKind, similarityValue, tokensList1, tokensList2
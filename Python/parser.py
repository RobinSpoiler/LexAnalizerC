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
    tokensListandLoc = []
    
    lex = lexer.Lexer(buffer, (3,4), engine)
    for token in lex:
        tokenloc = str(token.loc)
        # Location in format line : startIndex - line : endIndex
        indexLocation = tokenloc[tokenloc.find(':') + 1:]
        if(str(token.kind) != "dedent" and str(token.kind) != "indent"):
            linea = indexLocation[:indexLocation.find(':')]
            indexLocation = indexLocation.replace(linea+":", '')
        # Token and index location format : ('ident', '20-34') except dedent/indent/newline
        tokensListandLoc.append((token.kind, indexLocation))
        
        tokensKindFile.append(token.kind)
        if token.value is None:
            tokensValueFile.append(token.kind)
        else:
            tokensValueFile.append(token.value)
    # print("tokensListandLoc", tokensListandLoc)
    return tokensKindFile, tokensValueFile, tokensListandLoc

def compareFilesWithTokens(fileName1, fileName2,filecontent1, filecontent2):
    bufferFile1 = getBuffer(filecontent1, fileName1)
    bufferFile2 = getBuffer(filecontent2, fileName2)

    # Engine
    engine = diagnostic.Engine()
    # Getting tokens of file 1
    tokensFile1Kind, tokensFile1Value,tokensListandLoc1 = getTokensKindAndValue(bufferFile1, engine)
    # Getting tokens of file 2
    tokensFile2Kind, tokensFile2Value, tokensListandLoc2  = getTokensKindAndValue(bufferFile2, engine)
    
    # Getting similarity between two files by kind
    similarityKind = getTokenSimilarityPercentage(tokensFile1Kind, tokensFile2Kind)
    # print("Comparing tokens by kind: they are " + str(similarityKind) +"% similar")

    # Getting similarity between two files by value
    similarityValue = getTokenSimilarityPercentage(tokensFile1Value, tokensFile2Value)
    tokensListandLoc1 = list(tokensListandLoc1)
    tokensListandLoc2 = list(tokensListandLoc2)

    return similarityKind, similarityValue, tokensListandLoc1, tokensListandLoc2
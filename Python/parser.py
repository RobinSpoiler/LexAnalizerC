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
    similarityPercentage = getTextSimilarityPercentage(textFile1, textFile2)
    return {"texto": cleanSimilarityFile1}, {"texto": cleanSimilarityFile2}, similarityPercentage


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
        tokensListandLoc.append((token.kind, indexLocation, linea))
        
        tokensKindFile.append(token.kind)
        if token.value is None:
            tokensValueFile.append(token.kind)
        else:
            tokensValueFile.append(token.value)
    # print("tokensListandLoc", tokensListandLoc)
    return tokensKindFile, tokensValueFile, tokensListandLoc

def getTokenSimilarity(tokenValue1, tokenValue2):   
    matches = difflib.SequenceMatcher(None, tokenValue1, tokenValue2)
    bloques = []
    for block in matches.get_matching_blocks():
        bloques.append([block[0], block[1], block[2]])
    bloques.pop()
    return bloques

def getTokenUbication(tokens, similitud, lineaFAnte):
    first = tokens[0]

    if (first[0] == "indent" or first[0] == "dedent"):
        dospuntos = first[1].find(':')
        lineaI = int(first[1][:dospuntos])
        ubiI = int(first[1][dospuntos+1:])  
    else:
        score = first[1].find('-')
        lineaI = int(first[2])

        if (score != -1):
            ubiI = int(first[1][:score])
        else:
            ubiI = int(first[1])


    linea = 0

    for token in tokens:
        if token[0] == "newline":
            score = token[1].find('-')
            linea = int(token[2])

            if (score != -1):
                ubi = int(token[1][:score])
            else:
                ubi = int(token[1])

            if (lineaI == linea):
                if (lineaI == lineaFAnte):
                    similitud[len(similitud)-1]["indices"].append([ubiI, ubi])               
                else:
                    similitud.append({'lineNumber': int(linea), 'indices': [[ubiI, ubi]]})
            else:
                similitud.append({'lineNumber': int(linea), 'indices': [[1, ubi]]})

    last = tokens[len(tokens)-1]

    if (last[0] == "indent" or last[0] == "dedent"):
        dospuntos = last[1].find(':')
        lineaF = int(last[1][:dospuntos])
        ubiF = int(last[1][dospuntos+1:])

    elif (last[0] == "newline"):
        lineaF = linea
        ubiF = ubi
    else:
        score = last[1].find('-')
        lineaF = int(last[2])

        if  (score != -1):
            ubiF = int(last[1][score+1:])
        else:
            ubiF = int(last[1])

    if (lineaF == lineaI):
        #No encontro un newline
        if (lineaF == lineaFAnte):
            similitud[len(similitud)-1]["indices"].append([ubiI, ubiF])
        elif (linea != lineaF):
            similitud.append({'lineNumber': int(lineaF), 'indices': [[ubiI, ubiF]]})
    else:
        #Si encontro un newline
        if (linea != lineaF):
            similitud.append({'lineNumber': int(lineaF), 'indices': [[1, ubiF]]})

    return similitud, lineaF


def getTokenForHighlight(tokensStream1, tokensStream2, bloques):
    '''
    token: {
            similitud: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
        }
    '''

    similitud1 = []
    similitud2 = []

    lineaF1 = 0
    lineaF2 = 0

    for bloque in bloques:
        #Analisis para achivo 1 -----------------------------------------
        tokens1 = tokensStream1[bloque[0]:bloque[0] + bloque[2]]
        similitud1, lineaF1= getTokenUbication(tokens1, similitud1, lineaF1)

        #Analisis para archivo 2 -----------------------------------------
        tokens2 = tokensStream2[bloque[1]:bloque[1] + bloque[2]]
        similitud2, lineaF2 = getTokenUbication(tokens2, similitud2, lineaF2)

    return similitud1, similitud2

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

    # Getting the index of the tokens similarity highlight
    bloques = getTokenSimilarity(tokensFile1Kind, tokensFile2Kind)
    # tokenSimilarityFile1, tokenSimilarityFile2 = getTokenForHighlight(tokensListandLoc1, tokensListandLoc2, bloques)

    return similarityKind, similarityValue, tokensListandLoc1, tokensListandLoc2, bloques

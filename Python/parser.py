import sys, re
from pythonparser import source, lexer, diagnostic
import difflib

# -------Comparing files as plain text--------
def getPlainText(fileName):
    plainText = None
    with open(fileName) as file:
        plainText =  file.read()
    return plainText

def getTextSimilarityPercentage(textFile1, textFile2):
    return difflib.SequenceMatcher(None, textFile1, textFile2).ratio() * 100


def compareFilesAsText(fileName1, fileName2):
    textFile1 = getPlainText(fileName1)
    textFile2 = getPlainText(fileName2)

    similarity = getTextSimilarityPercentage(textFile1, textFile2)
    print("Comparing texts: they are " + str(similarity) +"% similar")

# -------Comparing files with tokens--------

# 
def getBuffer(fileName):
    buf = None
    with open(fileName) as file:
        buf = source.Buffer(file.read(), file.name)
    return buf

def getTokenSimilarityPercentage(tokensFile1, tokensFile2):
    return difflib.SequenceMatcher(None, tokensFile1, tokensFile2).ratio() * 100

def getTokens(buffer, engine):
    tokensFile = []
    for token in lexer.Lexer(buffer, (3,4), engine):
        tokensFile.append(token.value)
    return tokensFile

def compareFilesWithTokens(fileName1, fileName2):
    bufferFile1 = getBuffer(fileName1)
    bufferFile2 = getBuffer(fileName2)

    # Engine
    engine = diagnostic.Engine()

    # Getting tokens of file 1
    tokensFile1 = getTokens(bufferFile1, engine)
    # Getting tokens of file 2
    tokensFile2 = getTokens(bufferFile2, engine)
    
    # Getting similarity between two files
    similarity = getTokenSimilarityPercentage(tokensFile1, tokensFile2)
    print("Comparing tokens: they are " + str(similarity) +"% similar")


compareFilesWithTokens("prueba1.py", "prueba2.py")
compareFilesAsText("prueba1.py", "prueba2.py")
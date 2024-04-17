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
    print("Comparing character by character: they are " + str(similarity) +"% similar")

# -------Comparing files with tokens--------

# 
def getBuffer(fileName):
    buf = None
    with open(fileName) as file:
        buf = source.Buffer(file.read(), file.name)
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
    for token in lexer.Lexer(buffer, (3,4), engine):
        tokensKindFile.append(token.kind)
        if token.value == None:
            tokensValueFile.append(token.kind)
        else:
            tokensValueFile.append(token.value)
    return tokensKindFile, tokensValueFile

def compareFilesWithTokens(fileName1, fileName2):
    bufferFile1 = getBuffer(fileName1)
    bufferFile2 = getBuffer(fileName2)

    # Engine
    engine = diagnostic.Engine()

    # Getting tokens of file 1
    tokensFile1Kind, tokensFile1Value = getTokensKind(bufferFile1, engine)
    # Getting tokens of file 2
    tokensFile2Kind, tokensFile2Value  = getTokensKind(bufferFile2, engine)
    
    # Getting similarity between two files
    similarityKind = getTokenSimilarityPercentage(tokensFile1Kind, tokensFile2Kind)
    similarityValue = getTokenSimilarityPercentage(tokensFile1Value, tokensFile2Value)
    print("Comparing tokens by kind: they are " + str(similarityKind) +"% similar")
    print("Comparing tokens by value: they are " + str(similarityValue) +"% similar")

files = ["prueba1.py", "prueba2.py", "prueba3.py", "prueba4.py", "prueba5.py"]

for file1 in files:
    for file2 in files:
        if file1 != file2:
            print("\nComparing file " + file1 +" with " + file2)
            compareFilesWithTokens(file1, file2)
            compareFilesAsText(file1, file2)
# parser.py

import sys, re
from pythonparser import source, lexer, diagnostic
import difflib

# -------Comparing files as plain text--------
def getPlainText(file):
    plainText = None
    with file.stream as f:
        plainText = f.read()
    return plainText

def getTextSimilarityPercentage(textFile1, textFile2):
    return difflib.SequenceMatcher(None, textFile1, textFile2).ratio() * 100

def compareFilesAsText(file1, file2):
    textFile1 = getPlainText(file1)
    textFile2 = getPlainText(file2)

    similarity = getTextSimilarityPercentage(textFile1, textFile2)
    return similarity

# -------Comparing files with tokens--------

def getBuffer(file):
    buf = None
    with file.stream as f:
        buf = source.Buffer(f.read(), file.filename)
    return buf

def getTokenSimilarityPercentage(tokensFile1, tokensFile2):
    return difflib.SequenceMatcher(None, tokensFile1, tokensFile2).ratio() * 100

def getTokensKindAndValue(buffer, engine):
    tokensKindFile = []
    tokensValueFile = []
    for token in lexer.Lexer(buffer, (3,4), engine):
        tokensKindFile.append(token.kind)
        if token.value is None:
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
    tokensFile1Kind, tokensFile1Value = getTokensKindAndValue(bufferFile1, engine)
    # Getting tokens of file 2
    tokensFile2Kind, tokensFile2Value  = getTokensKindAndValue(bufferFile2, engine)
    
    # Getting similarity between two files by kind
    similarityKind = getTokenSimilarityPercentage(tokensFile1Kind, tokensFile2Kind)

    # Getting similarity between two files by value
    similarityValue = getTokenSimilarityPercentage(tokensFile1Value, tokensFile2Value)

    return similarityKind, similarityValue

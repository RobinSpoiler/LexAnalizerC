import sys, re
from pythonparser import source, lexer, diagnostic

def getBuffer(fileName):
    buf = None
    with open(fileName) as f:
        buf = source.Buffer(f.read(), f.name)
    return buf


def getSimilarityPercentage(tokensFile1, tokensFile2):
    smallerSize = len(tokensFile1) if len(tokensFile1) < len(tokensFile2) else len(tokensFile2)
    counter = 0
    for index in range(0, smallerSize):
        if tokensFile1[index] == tokensFile2[index]:
            counter += 1
    
    similarity = (counter / smallerSize) * 100
    return similarity


def compareFiles(fileName1, fileName2):
    bufferFile1 = getBuffer(fileName1)
    bufferFile2 = getBuffer(fileName2)

    # Engine
    engine = diagnostic.Engine()

    # Storing tokens
    tokensFile1 = []
    tokensFile2 = []

    # Getting tokens of file 1
    print("Tokens file 1 \n")
    for token in lexer.Lexer(bufferFile1, (3,4), engine):
        print(token.value)
        tokensFile1.append(token.value)

    # Getting tokens of file 2
    print("\nTokens file 2 \n")
    for token in lexer.Lexer(bufferFile2, (3,4), engine):
        print(token.value)
        tokensFile2.append(token.value)
    
    # Getting similarity between two files
    similarity = getSimilarityPercentage(tokensFile1, tokensFile2)
    print("They are " + str(similarity) +"% similar")

    


compareFiles("prueba1.py", "prueba2.py")
    


# Rewriter ?
# rewriter = source.Rewriter(buf)
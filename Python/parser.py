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

def getTextSimilarityPercentage(textFile1, textFile2):
    return difflib.SequenceMatcher(None, textFile1, textFile2).ratio() * 100

def compareFilesAsText(file1, file2):
    textFile1 = getPlainText(file1)
    textFile2 = getPlainText(file2)

    similarity = getTextSimilarityPercentage(textFile1, textFile2)
    print("Comparing character by character: they are " + str(similarity) +"% similar")
    return similarity

# -------Comparing files with tokens--------
def getBuffer(file):
    buf = None
    # Check if the file exists and has a size greater than zero
    if file and file.seekable() and file.tell() > 0:
        # Move the pointer to the beginning of the file
        file.seek(0)
        with io.BytesIO(file.read()) as f:
            # Print file content for debugging
            file_content = f.read()
            buf = source.Buffer(file_content, file.filename)
    else:
        print("Error: File is empty or does not exist.")
    return buf

def getTokenSimilarityPercentage(tokensFile1, tokensFile2):
    return difflib.SequenceMatcher(None, tokensFile1, tokensFile2).ratio() * 100

def getTokensKindAndValue(buffer, engine):
    print("Starting getTokensKindAndValue")
    tokensKindFile = []
    tokensValueFile = []
    tokensList = []
    
    # Print buffer content for debugging
    print("Buffer content:")
    print(buffer.source)
    
    lex = lexer.Lexer(buffer, (3,4), engine)
    print("Lexer object created")
    print("Lexer object:", lex)
    for token in lex:
        print("Inside loop")
        # print("Token:", token)
        # tokensList.append(token)
        tokensList.append((token.kind, str(token.loc)[11:]))
        tokensKindFile.append(token.kind)
        if token.value is None:
            tokensValueFile.append(token.kind)
        else:
            tokensValueFile.append(token.value)
    print("AAAA TOKEN: ", tokensList)
    print("Exiting getTokensKindAndValue")
    return tokensKindFile, tokensValueFile, tokensList



def compareFilesWithTokens(fileName1, fileName2):
    bufferFile1 = getBuffer(fileName1)
    bufferFile2 = getBuffer(fileName2)

    # Engine
    engine = diagnostic.Engine()
    print("engine: ", engine )
    # Getting tokens of file 1
    tokensFile1Kind, tokensFile1Value,tokensList1 = getTokensKindAndValue(bufferFile1, engine)
    # Getting tokens of file 2
    tokensFile2Kind, tokensFile2Value, tokensList2  = getTokensKindAndValue(bufferFile2, engine)
    
    # Getting similarity between two files by kind
    similarityKind = getTokenSimilarityPercentage(tokensFile1Kind, tokensFile2Kind)
    print("Comparing tokens by kind: they are " + str(similarityKind) +"% similar")

    # Getting similarity between two files by value
    similarityValue = getTokenSimilarityPercentage(tokensFile1Value, tokensFile2Value)
    print("Comparing tokens by value: they are " + str(similarityValue) +"% similar")
    tokensList1 = str(tokensList1)
    tokensList2 = str(tokensList2)

    return similarityKind, similarityValue, tokensList1, tokensList2
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

def compareFilesAsText(textFile1, textFile2):
    similarity = getTextSimilarityPercentage(textFile1, textFile2)
    print("Comparing character by character: they are " + str(similarity) +"% similar")
    return similarity

# -------Comparing files with tokens--------
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

# def variables(cleanTokens):
#     highVariables = []
#     for elemento in cleanTokens[0]:
#         if(elemento[0] == 'ident'):
#             highVariables.append(elemento)
#     return highVariables

# def ifStatement(cleanTokens):
#     # print("IF cleanTokens",cleanTokens)
#     highIfelse = []
#     for elemento in cleanTokens[0]: # No se por que aqui se tiene que accesar al elemmento 0
#         # print("0",elemento[0])
#         if(elemento[0] == 'if' or elemento[0] == 'elif' or elemento[0] == 'else'):
#             highIfelse.append(elemento)
#     return highIfelse

# def loops(cleanTokens):
#     # print("Loop cleanTokens",cleanTokens)
#     highLoop = []
#     for elemento in cleanTokens[0]: # No se por que aqui se tiene que accesar al elemmento 0
#         if(elemento[0] == 'while' or elemento[0] == 'for'):
#             highLoop.append(elemento)
#     return highLoop
    

def compareFilesWithTokens(fileName1, fileName2,filecontent1, filecontent2):
    bufferFile1 = getBuffer(filecontent1, fileName1)
    bufferFile2 = getBuffer(filecontent2, fileName2)

    # Engine
    engine = diagnostic.Engine()
    # print("engine: ", engine )
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
    tokensList1 = list(tokensList1)
    tokensList2 = list(tokensList2)

    return similarityKind, similarityValue, tokensList1, tokensList2
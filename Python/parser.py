import sys, re
from pythonparser import source, lexer, diagnostic

# File name that we're going to analyze
fname = "prueba.py"

# Buffer that will store all the content from the file we're reading
buf = None
# Open the file and asign the contest to buffer
with open(fname) as f:
    buf = source.Buffer(f.read(), f.name)

# Engine ?
engine = diagnostic.Engine()

# Rewriter ?
rewriter = source.Rewriter(buf)

# Print all tokens found in buffer
for token in lexer.Lexer(buf, (3,4), engine):
    print(token)
# AnLexC
Analizador léxico para C 


To run:

lex lexer.l

<!-- El parámetro -ll indica al compilador que enlace con la biblioteca de Lex -->
gcc lex.yy.c -o lexer -ll | clang lex.yy.c -o lexer -ll

./lexer


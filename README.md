# AnLexC
Analizador léxico para C 


To run:

lex lexer.l

### El parámetro -ll indica al compilador que enlace con la biblioteca de Lex
gcc lex.yy.c -o lexer -ll | clang lex.yy.c -o lexer -ll

./lexer

### Para leer un file
lex lexer.l

gcc main.c -o analizador_lexico -ll | clang main.c -o analizador_lexico -ll

./analizador_lexico <archivo.c>



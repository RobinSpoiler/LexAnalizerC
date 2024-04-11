# AnLexC
Analizador léxico para C 


To run:

### Correr lex lexer

1. Compilar el archivo .l que contiene las reglas establecidas
   
   lex lexer.l

2. Compilar el archivo .c generado por el lexer. Ocupar el compilador de agrado que acepte C.
   Nota. El parámetro -ll indica al compilador que enlace con la biblioteca de Lex.

   gcc lex.yy.c -o lexer -ll
   clang lex.yy.c -o lexer -ll

3. Ejecutar el archivo lexer para testearlo

  ./lexer

### Para leer un file e identificar el léxico

1. Compilar el archivo .l que contiene las reglas establecidas

   lex lexer.l

2. Compilar el archivo main.c que contine la lógica para usar el lexer con un archivo prueba. Ocupar el compilador de agrado que acepte C.

   gcc main.c -o analizador_lexico -ll
   clang main.c -o analizador_lexico -ll

3. Ejecutar el archivo lexer seguido del archivo prueba

   ./analizador_lexico <archivo.c>



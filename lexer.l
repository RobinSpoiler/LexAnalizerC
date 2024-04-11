%{
#include <stdio.h>
%}

DIGIT       [0-9]
LETTER      [a-zA-Z]
ID          {LETTER}({LETTER}|{DIGIT})*
NUMBER      {DIGIT}+
OPERATOR    [+*-/]

%%

{NUMBER}    { printf("Número: %s\n", yytext); }
{ID}        { printf("Identificador: %s\n", yytext); }
{OPERATOR}  { printf("Operador: %s\n", yytext); }
[ \t\n]     ; // Ignorar espacios en blanco, tabulaciones y saltos de línea
.           { printf("Token desconocido: %s\n", yytext); }

%%

int main() {
    yylex();
    return 0;
}

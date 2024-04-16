%{
#include <stdio.h>
#include <stdlib.h>
%}

DIGIT       [0-9]
LETTER      [a-zA-Z]
ID          {LETTER}({LETTER}|{DIGIT})*
NUMBER      {DIGIT}+
STRING      \"(\\.|[^\"])*\"
OPERATOR    [+*-/]

%x PRINTF

/* Definir palabras reservadas de C */
%%
auto        { printf("Palabra reservada: auto\n"); }
break       { printf("Palabra reservada: break\n"); }
case        { printf("Palabra reservada: case\n"); }
char        { printf("Palabra reservada: char\n"); }
const       { printf("Palabra reservada: const\n"); }
continue    { printf("Palabra reservada: continue\n"); }
default     { printf("Palabra reservada: default\n"); }
do          { printf("Palabra reservada: do\n"); }
double      { printf("Palabra reservada: double\n"); }
else        { printf("Palabra reservada: else\n"); }
enum        { printf("Palabra reservada: enum\n"); }
extern      { printf("Palabra reservada: extern\n"); }
float       { printf("Palabra reservada: float\n"); }
for         { printf("Palabra reservada: for\n"); }
goto        { printf("Palabra reservada: goto\n"); }
if          { printf("Palabra reservada: if\n"); }
int         { printf("Palabra reservada: int\n"); }
long        { printf("Palabra reservada: long\n"); }
register    { printf("Palabra reservada: register\n"); }
return      { printf("Palabra reservada: return\n"); }
short       { printf("Palabra reservada: short\n"); }
signed      { printf("Palabra reservada: signed\n"); }
sizeof      { printf("Palabra reservada: sizeof\n"); }
static      { printf("Palabra reservada: static\n"); }
struct      { printf("Palabra reservada: struct\n"); }
switch      { printf("Palabra reservada: switch\n"); }
typedef     { printf("Palabra reservada: typedef\n"); }
union       { printf("Palabra reservada: union\n"); }
unsigned    { printf("Palabra reservada: unsigned\n"); }
void        { printf("Palabra reservada: void\n"); }
volatile    { printf("Palabra reservada: volatile\n"); }
while       { printf("Palabra reservada: while\n"); }
printf      { printf("Palabra reservada: printf\n"); }
scanf       { printf("Palabra reservada: scanf\n"); }

{STRING}    { printf("String: %s\n", yytext); }

{DIGIT}+"."{DIGIT}+ { printf("Flotante: %s\n", yytext); }

"."{DIGIT}+ { printf("Flotante: %s\n", yytext); }

"printf(\"" {
    printf("Interpolación encontrada: ");
    BEGIN(PRINTF); 
}

<PRINTF>{
    "%d"       { printf("Entero: %s\n", yytext); }
    "%f"       { printf("Flotante: %s\n", yytext); }
    "%s"       { printf("Cadena: %s\n", yytext); }
    "\\n\""    { printf("Fin de la cadena de formato\n"); BEGIN(INITIAL); }
    .          { /* Ignorar otros caracteres dentro de la cadena de formato */ }
}

\;     { printf("Punto y coma encontrado\n"); }
\{     { printf("Llave de apertura encontrada\n"); }
\}     { printf("Llave de cierre encontrada\n"); }
\(     { printf("Paréntesis de apertura encontrado\n"); }
\)     { printf("Paréntesis de cierre encontrado\n"); }
\=     { printf("Igual\n"); }

{NUMBER}    { printf("Número entero: %s\n", yytext); }
{ID}        { printf("Identificador: %s\n", yytext); }
{OPERATOR}  { printf("Operador: %s\n", yytext); }
[ \t\n]     ; // Ignorar espacios en blanco, tabulaciones y saltos de línea
.           { printf("Token desconocido: %s\n", yytext); }
%%

int yywrap() {
    return 1; // Indica a yylex() que hemos terminado de analizar
}
int main() {
    yylex();
    return 0;
}

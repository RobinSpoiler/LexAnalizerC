%{
#include <stdio.h>
#include <stdlib.h>
%}

%{
#define PRINTF 1
#define SCANF 2
#define IF 3
#define ELSE 4
#define WHILE 5
#define FOR 6
#define INT 7
#define FLOAT 8
#define CHAR 9
#define RETURN 10
#define ID 11
#define INTEGER 12
#define FLOATNUMBER 13
#define PLUS 14
#define MINUS 15
#define TIMES 16
#define DIVIDE 17
#define ASSIGN 18
#define EQ 19
#define NEQ 20
#define LT 21
#define LTE 22
#define GT 23
#define GTE 24
#define SEMICOLON 25
#define COMMA 26
#define LPAREN 27
#define RPAREN 28
#define LBRACE 29
#define RBRACE 30
#define LBRACKET 31
#define RBRACKET 32
%}

ws [ \t\n]+
comment "//".*\n

letter [a-zA-Z]
digit [0-9]
identifier {letter}({letter}|{digit})*
integer {digit}+
float ({digit}+\.{digit}*|\.{digit}+)

%%


{ws}   
{comment}

"printf"    { return PRINTF; }
"scanf"     { return SCANF; }
"if"        { return IF; }
"else"      { return ELSE; }
"while"     { return WHILE; }
"for"       { return FOR; }
"int"       { return INT; }
"float"     { return FLOAT; }
"char"      { return CHAR; }
"return"    { return RETURN; }

{identifier} { return ID; }
{integer}    { return INTEGER; }
{float}      { return FLOATNUMBER; }

"+"    { return PLUS; }
"-"    { return MINUS; }
"*"    { return TIMES; }
"/"    { return DIVIDE; }
"="    { return ASSIGN; }
"=="   { return EQ; }
"!="   { return NEQ; }
"<"    { return LT; }
"<="   { return LTE; }
">"    { return GT; }
">="   { return GTE; }
";"    { return SEMICOLON; }
","    { return COMMA; }
"("    { return LPAREN; }
")"    { return RPAREN; }
"{"    { return LBRACE; }
"}"    { return RBRACE; }
"["    { return LBRACKET; }
"]"    { return RBRACKET; }

.      { printf("Token no reconocido\n"); }

%%

int yywrap(void) {
    return 1;
}

// int main() {
//     yylex();
//     return 0;
// }

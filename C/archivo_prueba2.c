#include <stdio.h>
#include <stdlib.h>
#include "lex.yy.c" // Incluye el analizador léxico generado por Lex

extern int yylex(); // Declaración externa de la función yylex()

int main(int argc, char *argv[]) {
    FILE *fp;
    int token;

    fp = fopen(argv[1], "r");
    if (fp == NULL) {
        perror("Error al abrir el archivo");
        return 1;
    }

    // Establece el archivo de entrada para el analizador léxico
    yyin = fp;

    // Ejecuta el analizador léxico hasta que llegue al final del archivo
    while ((token = yylex()) != 0) {
        printf("%d\n", token);
    }

    fclose(fp);
    return 0;
}
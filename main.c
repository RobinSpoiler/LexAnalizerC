#include <stdio.h>
#include <stdlib.h>
#include "lex.yy.c" // Incluye el analizador léxico generado por Lex

extern int yylex(); // Declaración externa de la función yylex()

int main(int argc, char *argv[]) {
    FILE *fp;
    int token;

    if (argc != 2) {
        printf("Uso: %s archivo.c\n", argv[0]);
        return 1;
    }

    fp = fopen(argv[1], "r");
    if (fp == NULL) {
        perror("Error al abrir el archivo");
        return 1;
    }

    // Establece el archivo de entrada para el analizador léxico
    yyin = fp;

    // Ejecuta el analizador léxico hasta que llegue al final del archivo
    while ((token = yylex()) != 0) {
        // No es necesario imprimir tokens individuales aquí,
        // ya que las impresiones están manejadas por las reglas en lexer.l
    }

    fclose(fp);
    return 0;
}
from lexer import getLexer

lexer = getLexer()

# Abrir el archivo .c y leer su contenido
with open('archivo_prueba.c', 'r') as file:
    data = file.read()

# Alimentar el lexer con el contenido del archivo
lexer.input(data)

# Iterar sobre los tokens generados
for token in lexer:
    print(token)
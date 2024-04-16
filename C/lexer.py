import ply.lex as lex

reserved = {
    'printf' : 'PRINTF',
    'auto': 'AUTO',
    'break': 'BREAK',
    'case': 'CASE',
    'char': 'CHAR',
    'const': 'CONST',
    'continue': 'CONTINUE',
    'default': 'DEFAULT',
    'do': 'DO',
    'double': 'DOUBLE',
    'else': 'ELSE',
    'enum': 'ENUM',
    'extern': 'EXTERN',
    'float': 'FLOAT',
    'for': 'FOR',
    'goto': 'GOTO',
    'if': 'IF',
    'int': 'INT',
    'long': 'LONG',
    'register': 'REGISTER',
    'return': 'RETURN',
    'short': 'SHORT',
    'signed': 'SIGNED',
    'sizeof': 'SIZEOF',
    'static': 'STATIC',
    'struct': 'STRUCT',
    'switch': 'SWITCH',
    'typedef': 'TYPEDEF',
    'union': 'UNION',
    'unsigned': 'UNSIGNED',
    'void': 'VOID',
    'volatile': 'VOLATILE',
    'while': 'WHILE'
}

# Lista de tokens
tokens = list(reserved.values()) + [
    'ID',
    'NUMBER',
    'STRING',
    'SEMICOLON',
    'COMMA',
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET'
]

# Reglas para tokens
t_ignore = ' \t\n'

# Definiciones de tokens para palabras reservadas

t_SEMICOLON = r';'
t_COMMA = r','
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

def t_AUTO(t):
    r'auto'
    return t

def t_BREAK(t):
    r'break'
    return t

def t_CASE(t):
    r'case'
    return t

def t_CHAR(t):
    r'char'
    return t

def t_CONST(t):
    r'const'
    return t

def t_CONTINUE(t):
    r'continue'
    return t

def t_DEFAULT(t):
    r'default'
    return t

def t_DO(t):
    r'do'
    return t

def t_DOUBLE(t):
    r'double'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_ENUM(t):
    r'enum'
    return t

def t_EXTERN(t):
    r'extern'
    return t

def t_FLOAT(t):
    r'float'
    return t

def t_FOR(t):
    r'for'
    return t

def t_GOTO(t):
    r'goto'
    return t

def t_IF(t):
    r'if'
    return t

def t_INT(t):
    r'int'
    return t

def t_LONG(t):
    r'long'
    return t

def t_REGISTER(t):
    r'register'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_SHORT(t):
    r'short'
    return t

def t_SIGNED(t):
    r'signed'
    return t

def t_SIZEOF(t):
    r'sizeof'
    return t

def t_STATIC(t):
    r'static'
    return t

def t_STRUCT(t):
    r'struct'
    return t

def t_SWITCH(t):
    r'switch'
    return t

def t_TYPEDEF(t):
    r'typedef'
    return t

def t_UNION(t):
    r'union'
    return t

def t_UNSIGNED(t):
    r'unsigned'
    return t

def t_VOID(t):
    r'void'
    return t

def t_VOLATILE(t):
    r'volatile'
    return t

def t_WHILE(t):
    r'while'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"(\\.|[^\"])*\"'
    return t

# Regla para detectar errores
def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Abrir el archivo .c y leer su contenido
with open('archivo_prueba.c', 'r') as file:
    data = file.read()

# Alimentar el lexer con el contenido del archivo
lexer.input(data)

# Iterar sobre los tokens generados
for token in lexer:
    print(token)
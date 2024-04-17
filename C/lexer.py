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
    'float': 'FLOATTYPE',
    'for': 'FOR',
    'goto': 'GOTO',
    'if': 'IF',
    'int': 'INTTYPE',
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
    'STR',
    'INT', 
    'FLOAT',
    'RWLIBRARY',
    'SEMICOLON',
    'COMMA',
    'ASSIGN',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'COMMENT',
    'MULTILINECOMMENT'
] 

states = (
   ('doubleq','exclusive'),
)

# Reglas para tokens
t_ignore = ' \t\n'

# Definiciones de tokens para palabras reservadas

t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_ASSIGN = r'\='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Busca el valor en el diccionario de palabras reservadas
    return t

def t_RWLIBRARY(t):
    r'\#[include]+\s\<[^0-9]+\>' 
    return t

def t_STR(t):
    r'\".*\"'
    return t

def t_FLOAT(t):
    r'(?:\d*(?:\_\d+)?\.\d*([eE][^_][+-]?[\d_]+)?)|(?:\d+([eE][+-]?\d+))'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d(_\d|\d)*' # A number followed by multiple numbers or multiple sets of underscores+numbers
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'\/\/.*'
    return t

def t_MULTILINECOMMENT(t):
    r'\/\*.*\*\/'
    return t

#Match first "
def t_doubleq(t):
    r'\"'
    t.lexer.begin('doubleq')
    return t

#Rules for doubleq state
def t_doubleq_string(t):
    r'([^\"])'

def t_doubleq_closing(t):
    r'\\\"'

def t_doubleq_final(t):
    r'\''
    t.type = 'STR'
    t.lexer.begin("INITIAL")
    return t

def t_doubleq_error(t):
    pass

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
    
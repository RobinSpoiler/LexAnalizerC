import ply.lex as lex
from keywords import getKeywordRegex
from punctuators import PUNCTUATORS

# Lista de tokens
tokens = [
    'ID',
    # Types
    'STR',
    'INT', 
    'FLOAT',
    'RWLIBRARY',
    # Punctuation
    'PUNCTUATORS',
    # Operation
    'ASSIGN',
    # Comments
    'COMMENT',
    'MULTILINECOMMENT',
    'KEYWORD',
] 

states = (
   ('doubleq','exclusive'),
)

# Reglas para tokens
t_ignore = ' \t\n'

# Definiciones de tokens para palabras reservadas


# # Regresa un regex, donde cada elemento se repite dos veces
# # Por ejemplo: r' \+\+ | \-\- | \*\*
# # ++ -- == && << >> 
# def getRegexDuplicados():
#     DUPLICADOS = ["+", "-", "*", "=", "<", ">", "&", "|", "#"]
#     regex = r''
#     for i in DUPLICADOS:     
#         regex += "\\" + i + "\\" + i + "|"
#     return regex[:-1] 

# regex_individuales = r'[\{\}\(\)\.\[\]\&\*\+\-\~\!\/\%\>\<\^\|\?\:\;\,\.\=\#]'

# regex_compuestos = r'-> | <= | >= | != | \*= | /= | %= | \+= | -= | <<= | >>= | &= | ^= | \|= | <: | :> | <% | %> | %: | %:%: | \.\.\.'

t_PUNCTUATORS = PUNCTUATORS


@lex.TOKEN(getKeywordRegex())
def t_KEYWORD(t):
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
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
    
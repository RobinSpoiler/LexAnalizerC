import ply.lex as lex
from keywords import KEYWORD_REGEX
from punctuators import PUNCTUATOR_REGEX
from integers import INTEGER_CONSTANT_REGEX
from strings import *

# Lista de tokens
tokens = [
    'ID',
    # Types
    'STR',
    'INT', 
    'FLOAT',
    'RWLIBRARY',
    # Punctuation
    'PUNCTUATOR',
    # Operation
    'ASSIGN',
    # Comments
    'COMMENT',
    'MULTILINECOMMENT',
    'KEYWORD',
] 

states = (
    ('singleString','exclusive'),
    ('doubleString','exclusive'),
)

# Reglas para tokens
t_ignore = ' \t\n'


t_PUNCTUATOR = PUNCTUATOR_REGEX

@lex.TOKEN(KEYWORD_REGEX)
def t_KEYWORD(t):
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_RWLIBRARY(t):
    r'\#[include]+\s\<[^0-9]+\>' 
    return t

def t_FLOAT(t):
    r'(?:\d*(?:\_\d+)?\.\d*([eE][^_][+-]?[\d_]+)?)|(?:\d+([eE][+-]?\d+))'
    t.value = float(t.value)
    return t

@lex.TOKEN(INTEGER_CONSTANT_REGEX)
def t_INT(t):
    return t

def t_COMMENT(t):
    r'\/\/.*'
    return t

def t_MULTILINECOMMENT(t):
    r'\/\*.*\*\/'
    return t

@lex.TOKEN(SINGLE_STRING_BEGIN_END_REGEX)
def t_begin_single_string(t):
    t.lexer.begin('singleString')
    t.lexer.str = "'"

@lex.TOKEN(DOUBLE_STRING_BEGIN_END_REGEX)
def t_begin_double_string(t):
    t.lexer.begin('doubleString')
    t.lexer.str = '"'

# ========= STRING LITERALS =========
# == Single-quoted string literals ==

@lex.TOKEN(SINGLE_STRING_ESCAPE_REGEX)
def t_singleString_escape_STR(t):
    t.lexer.str += t.value

@lex.TOKEN(SINGLE_STRING_CONTENT_REGEX)
def t_singleString_content_STR(t):
    t.lexer.str += t.value

@lex.TOKEN(SINGLE_STRING_BEGIN_END_REGEX)
def t_singleString_STR(t):
    t.value = t.lexer.str + t.value
    t.lexer.begin('INITIAL')
    return t

# == Double-quoted string literals ==
@lex.TOKEN(DOUBLE_STRING_ESCAPE_REGEX)
def t_doubleString_escape_STR(t):
    t.lexer.str += t.value

@lex.TOKEN(DOUBLE_STRING_CONTENT_REGEX)
def t_doubleString_content_STR(t):
    t.lexer.str += t.value

@lex.TOKEN(DOUBLE_STRING_BEGIN_END_REGEX)
def t_doubleString_STR(t):
    t.value = t.lexer.str + t.value
    t.lexer.begin('INITIAL')
    return t

# ======== ERROR HANDLERS ==========
def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

def t_singleString_doubleString_error(t):
    print("ERROR with t:", t)

# Construir el lexer
lexer = lex.lex()
    
def getLexer():
    return lexer
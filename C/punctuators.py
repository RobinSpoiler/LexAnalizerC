"""
Punctuators must be one of:
[ ] ( ) { } . ->
++ -- & * + - ~ !
/ % << >> < > <= >= == != ^ | && ||
? : ; ...
= *= /= %= += -= <<= >>= &= ^= |=
, # ##
<: :> <% %> %: %:%:
"""

# Regresa un regex, donde cada elemento se repite dos veces
# Por ejemplo: r' \+\+ | \-\- | \*\*
# ++ -- == && << >> 
def getRegexDuplicados():
    DUPLICADOS = ["+", "-", "*", "=", "<", ">", "&", "|", "#"]
    regex = r''
    for i in DUPLICADOS:     
        regex += "\\" + i + "\\" + i + "|"
    return regex[:-1] 

regex_individuales = r'[\{\}\(\)\.\[\]\&\*\+\-\~\!\/\%\>\<\^\|\?\:\;\,\.\=\#]'

regex_compuestos = r'-> | <= | >= | != | \*= | /= | %= | \+= | -= | <<= | >>= | &= | ^= | \|= | <: | :> | <% | %> | %: | %:%: | \.\.\.'

PUNCTUATORS = r'(' + regex_compuestos + r'|' + getRegexDuplicados() +  r'|' + regex_individuales + r')' 

def verificar_palindromo(texto):
    texto = texto.replace(" ", "").lower()
    invertido = texto[::-1]
    return texto == invertido
entrada = input("Escribe una frase: ")
if verificar_palindromo(entrada):
    print(f"La frase '{entrada}' es un palíndromo")
else:
    print(f"La frase '{entrada}' no es un palíndromo")
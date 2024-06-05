def es_palindromo(cadena):
    cadena = cadena.replace(" ", "").lower()
    return cadena == cadena[::-1]
frase = input("Introduce una frase: ")
if es_palindromo(frase):
    print(f"'{frase}' es un palíndromo")
else:
    print(f"'{frase}' no es un palíndromo")
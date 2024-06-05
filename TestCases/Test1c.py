def es_palabra_palindromo(palabra):
    palabra = palabra.replace(" ", "").lower()
    reverso = palabra[::-1]
    return palabra == reverso
palabra = input("Introduce una palabra o frase: ")
if es_palabra_palindromo(palabra):
    print(f"'{palabra}' es un palíndromo")
else:
    print(f"'{palabra}' no es un palíndromo")
def sumar_digitos(numero):
    suma = 0
    while numero > 0:
        digito = numero % 10
        suma += digito
        numero //= 10
    return suma
def es_numero_valido(num_str):
    return num_str.isdigit() and int(num_str) >= 0
numero = input("Introduce un número positivo: ")
if not es_numero_valido(numero):
    print("El número no es válido. Debe ser un número positivo.")
else:
    numero = int(numero)
    suma = sumar_digitos(numero)
    print(f"La suma de los dígitos de {numero} es {suma}")
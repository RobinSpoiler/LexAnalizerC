def suma_digitos(num):
    total = 0
    while num > 0:
        total += num % 10
        num = num // 10
    return total
def obtener_numero():
    numero = input("Ingrese un número positivo: ")
    while not numero.isdigit() or int(numero) < 0:
        print("Entrada inválida. Por favor ingrese un número positivo.")
        numero = input("Ingrese un número positivo: ")
    return int(numero)
numero = obtener_numero()
suma = suma_digitos(numero)
print(f"La suma de los dígitos del número {numero} es: {suma}")

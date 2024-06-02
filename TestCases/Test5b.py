def calcular_suma_digitos(n):
    suma = 0
    while n != 0:
        suma += n % 10
        n //= 10
    return suma
def solicitar_numero():
    while True:
        num_str = input("Escribe un número positivo: ")
        if num_str.isdigit() and int(num_str) >= 0:
            return int(num_str)
        else:
            print("Entrada no válida. Intenta de nuevo.")
def main():
    numero = solicitar_numero()
    resultado = calcular_suma_digitos(numero)
    print(f"La suma de los dígitos de {numero} es {resultado}")
if __name__ == "__main__":
    main()
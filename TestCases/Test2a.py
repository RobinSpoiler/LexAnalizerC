def es_numero_primo(numero):
    if numero < 2:
        return False
    for i in range(2, int(numero ** 0.5) + 1):
        if numero % i == 0:
            return False
    return True
def obtener_primos_hasta(n):
    primos = []
    for i in range(2, n + 1):
        if es_numero_primo(i):
            primos.append(i)
    return primos
def main():
    n = int(input("Introduce un número: "))
    primos = obtener_primos_hasta(n)
    print(f"Primos hasta {n}: {primos}")
if __name__ == "__main__":
    main()
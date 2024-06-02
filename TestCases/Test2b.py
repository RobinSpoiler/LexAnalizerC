def verificar_primo(n):
    if n < 2:
        return False
    for divisor in range(2, int(n**0.5) + 1):
        if n % divisor == 0:
            return False
    return True
def generar_primos_hasta(n):
    lista_primos = []
    for numero in range(2, n + 1):
        if verificar_primo(numero):
            lista_primos.append(numero)
    return lista_primos
def main():
    n = int(input("Escribe un número: "))
    primos = generar_primos_hasta(n)
    print(f"Lista de números primos hasta {n}: {primos}")
if __name__ == "__main__":
    main()
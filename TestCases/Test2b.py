def verificar_primo(n):
    if n < 2:
        return False
    for divisor in range(2, int(n**0.5) + 1):
        if n % divisor == 0:
            return False
    return True
n = int(input("Escribe un número: "))
lista_primos = []
for numero in range(2, n + 1):
    if verificar_primo(numero):
        lista_primos.append(numero)
print(f"Lista de números primos hasta {n}: {lista_primos}")
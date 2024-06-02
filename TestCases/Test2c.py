def es_primo(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
def primos_hasta_n(n):
    return [num for num in range(2, n + 1) if es_primo(num)]
def main():
    n = int(input("Introduce un número: "))
    print(f"Números primos hasta {n}: {primos_hasta_n(n)}")
if __name__ == "__main__":
    main()
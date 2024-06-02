def fibonacci_hasta_n(n):
    secuencia = [0, 1]
    for _ in range(2, n):
        siguiente = secuencia[-1] + secuencia[-2]
        secuencia.append(siguiente)
    return secuencia
def mostrar_secuencia(secuencia):
    for indice, valor in enumerate(secuencia):
        print(f"Posición {indice}: {valor}")
if __name__ == "__main__":
    n = int(input("Introduce la cantidad de términos de Fibonacci: "))
    if n < 2:
        print("Debe ser al menos 2")
    else:
        secuencia = fibonacci_hasta_n(n)
        mostrar_secuencia(secuencia)
def crear_secuencia_fibonacci(n):
    fib = [0, 1]
    while len(fib) < n:
        siguiente = fib[-1] + fib[-2]
        fib.append(siguiente)
    return fib
def imprimir_secuencia(fib):
    for index, number in enumerate(fib):
        print(f"Índice {index}: {number}")
n = int(input("Ingrese el número de elementos de Fibonacci: "))
if n < 2:
    print("El valor debe ser 2 o más")
else:
    secuencia_fib = crear_secuencia_fibonacci(n)
    imprimir_secuencia(secuencia_fib)
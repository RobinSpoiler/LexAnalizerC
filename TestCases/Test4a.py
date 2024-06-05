def generar_fibonacci(n):
    fibonacci = [0, 1]
    while len(fibonacci) < n:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    return fibonacci
def imprimir_fibonacci(fibonacci):
    for i, num in enumerate(fibonacci):
        print(f"Fibonacci[{i}]: {num}")
n = int(input("Introduce el número de términos de la secuencia de Fibonacci: "))
if n < 2:
    print("El número debe ser mayor o igual a 2")
else:
    fibonacci = generar_fibonacci(n)
    imprimir_fibonacci(fibonacci)
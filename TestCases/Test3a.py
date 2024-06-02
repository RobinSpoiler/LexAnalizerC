def burbuja_ordenar(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            if lista[j] > lista[j+1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
def imprimir_lista(lista):
    for i, valor in enumerate(lista):
        print(f"Elemento {i}: {valor}")
if __name__ == "__main__":
    lista = [int(x) for x in input("Introduce números separados por espacios: ").split()]
    print("Lista original:")
    imprimir_lista(lista)
    burbuja_ordenar(lista)
    print("Lista ordenada:")
    imprimir_lista(lista)
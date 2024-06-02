def ordenar_burbuja(numeros):
    longitud = len(numeros)
    for i in range(longitud):
        for j in range(0, longitud-i-1):
            if numeros[j] > numeros[j+1]:
                numeros[j], numeros[j+1] = numeros[j+1], numeros[j]
def mostrar_lista(numeros):
    for index, numero in enumerate(numeros):
        print(f"Índice {index}: {numero}")
if __name__ == "__main__":
    numeros = list(map(int, input("Ingrese números separados por espacios: ").split()))
    print("Lista antes de ordenar:")
    mostrar_lista(numeros)
    ordenar_burbuja(numeros)
    print("Lista después de ordenar:")
    mostrar_lista(numeros)
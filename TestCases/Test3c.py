def bubble_sort(lista):
    size = len(lista)
    for i in range(size):
        for j in range(0, size-i-1):
            if lista[j] > lista[j+1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
def print_list(lista):
    for idx, num in enumerate(lista):
        print(f"Elemento en índice {idx}: {num}")
lista = [int(x) for x in input("Escriba números separados por espacios: ").split()]
print("Lista antes de ordenar:")
print_list(lista)
bubble_sort(lista)
print("Lista después de ordenar:")
print_list(lista)
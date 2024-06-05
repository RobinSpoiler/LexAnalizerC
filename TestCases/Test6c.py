def obtener_maximo(lista):
    if len(lista) == 0:
        return None
    maximo = lista[0]
    for valor in lista[1:]:
        if valor > maximo:
            maximo = valor
    return maximo
def pedir_lista():
    while True:
        entrada = input("Introduce una serie de números separados por espacios: ")
        try:
            lista = [int(x) for x in entrada.split()]
            return lista
        except ValueError:
            print("Entrada no válida. Asegúrate de introducir solo números separados por espacios.")
lista = pedir_lista()
if lista:
    maximo = obtener_maximo(lista)
    print(f"El número mayor en la lista es: {maximo}")
else:
    print("No se introdujeron números válidos.")
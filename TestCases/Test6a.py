def encontrar_maximo(lista):
    if len(lista) == 0:
        return None
    maximo = lista[0]
    for num in lista:
        if num > maximo:
            maximo = num
    return maximo
lista = []
entrada = input("Introduce números separados por espacios: ")
elementos = entrada.split()
for elemento in elementos:
    if elemento.isdigit() or (elemento.startswith('-') and elemento[1:].isdigit()):
        lista.append(int(elemento))
    else:
        print(f"{elemento} no es un número válido y será ignorado.")
if lista:
    maximo = encontrar_maximo(lista)
    print(f"El número máximo en la lista es {maximo}")
else:
    print("La lista está vacía o no contiene números válidos.")
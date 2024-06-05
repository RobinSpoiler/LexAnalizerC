def max_en_lista(numeros):
    if not numeros:
        return None
    maximo = numeros[0]
    for numero in numeros:
        if numero > maximo:
            maximo = numero
    return maximo
def leer_numeros():
    lista = []
    numeros_str = input("Introduce una lista de números separados por espacios: ")
    for num_str in numeros_str.split():
        try:
            lista.append(int(num_str))
        except ValueError:
            print(f"'{num_str}' no es un número válido y será ignorado.")
    return lista
numeros = leer_numeros()
if numeros:
    maximo = max_en_lista(numeros)
    print(f"El valor máximo en la lista es: {maximo}")
else:
    print("La lista proporcionada está vacía o no contiene números válidos.")
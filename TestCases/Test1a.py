triangulos = [
    (3, 3, 3),
    (4, 4, 5),
    (3, 4, 5)
]
def tipo_triangulo(lado1, lado2, lado3):
    if lado1 == lado2:
        if lado2 == lado3:
            return "Equilátero"
        else:
            return "Isósceles"
    elif lado1 == lado3 or lado2 == lado3:
        return "Isósceles"
    else:
        return "Escaleno"
for lados in triangulos:
    tipo = tipo_triangulo(*lados)
    print(f"El triángulo con lados {lados} es {tipo}")
def determinar_tipo_triangulo(a, b, c):
    lados = {a, b, c}
    if len(lados) == 1:
        return "Equilátero"
    elif len(lados) == 2:
        return "Isósceles"
    else:
        return "Escaleno"
if __name__ == "__main__":
    ejemplos = [
        (5, 5, 5),
        (6, 6, 10),
        (8, 7, 6)
    ]
    for a, b, c in ejemplos:
        tipo = determinar_tipo_triangulo(a, b, c)
        print(f"Triángulo con lados {a}, {b}, {c} es {tipo}")
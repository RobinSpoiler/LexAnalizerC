def clasificar_triangulo(l1, l2, l3):
    lados = [l1, l2, l3]
    conteo = {lado: lados.count(lado) for lado in lados}
    if 3 in conteo.values():
        return "Equilátero"
    elif 2 in conteo.values():
        return "Isósceles"
    else:
        return "Escaleno"
if __name__ == "__main__":
    conjuntos_de_lados = [
        (2, 2, 2),
        (7, 7, 10),
        (3, 4, 6)
    ]
    for l1, l2, l3 in conjuntos_de_lados:
        tipo = clasificar_triangulo(l1, l2, l3)
        print(f"Triángulo con lados {l1}, {l2}, {l3} es {tipo}")
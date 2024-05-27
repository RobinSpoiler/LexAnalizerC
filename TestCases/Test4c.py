def contar_palabras_count(lista_palabras):
    palabras_unicas = set(lista_palabras)
    frecuencia = {}
    for palabra in palabras_unicas:
        frecuencia[palabra] = lista_palabras.count(palabra)
    return frecuencia
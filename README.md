# React + Vite

## Dependencies

- yarn add react-router-dom
- yarn add @emotion/react
- yarn add @mui/material
- yarn add axios
- yarn add @emotion/styled
- yarn add @mui/x-data-grid
- pip install pydot
- pip install graphviz

## Manual para correr la aplicación
1. En la terminal, ir a la carpeta Python
2. Correr el comando python server.py
3. En otra ventana de la termina, ir a la carpeta Front
4. Correr el comando yarn dev
5. En el navegador, pegar la URL que se muestra despues de "Local"

# CODESYNC API
Logica necesaria para que el front-end reciba la informacion de la manera mas simple posible.


## Endpoints de obtención de files
### `/add_file`
#### Descripción
Lee archivos desde una carga de archivos y los sube a una base de datos de SQLAlchemy

#### Método de HTTP
`POST`

#### Parámetros
(Mediante el body de la petición en formato FormData)
| Parámetro   | Tipo            | Obligatorio | Descripción                           |
|------------ | --------------- | ----------- | ------------------------------------- |
| files        | [ FileStorage ] | si          | Archivos a subir                      |

#### Respuesta
En caso de una carga exitosa, se devuelve un código HTTP 200 (OK).
En caso de error, se devuelve un código HTTP 400 (Bad Request).

#### Ejemplo
**Petición**
POST 34.16.137.250:8002/add_file
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
```
{
    "files": [
        <FileStorage: 'Test1a.py' ('text/x-python')>,
        <FileStorage: 'Test1b.py' ('text/x-python')>
    ]
}
```
---
### `/get_files`
#### Descripción
Obtiene un diccionario de diccionarios con atributos de los archivos obtenidos anteriormente.

#### Método de HTTP
`GET`

#### Parámetros
No requiere parámetros.

#### Respuesta
En caso de una solicitud exitosa, se devuelve un código HTTP 200 (OK).
En caso de error, se devuelve un código HTTP 400 (Bad Request).

#### Ejemplo de Respuesta
```
{
    1: {
        'id': 1,
        'filename': 'Test1a.py',
        'content': 'triangulos = [\n    (3, 3, 3),\n    (4, 4, 5),\n    (3, 4, 5)\n]\ndef tipo_triangulo(lado1, lado2...'
    },
    2: {
        'id': 2,
        'filename': 'Test1b.py',
        'content': 'def determinar_tipo_triangulo(a, b, c):\n   ....'
    }
}
```
---
### `/getFileByName`
#### Descripción
Obtiene el contenido de dos archivos comparados según su nombre.

#### Método de HTTP
`GET`

#### Parámetros
| Parámetro  | Tipo   | Obligatorio | Descripción                        |
|------------|--------|-------------|------------------------------------|
| file1      | string | sí          | Nombre del primer archivo a comparar |
| file2      | string | sí          | Nombre del segundo archivo a comparar |

#### Respuesta
En caso de una solicitud exitosa, se devuelve un código HTTP 200 (OK) junto con el contenido de ambos archivos.
En caso de error, se devuelve un código HTTP 400 (Bad Request).

#### Ejemplo de Respuesta
```
{
    'id': 2,
    'filename': 'Test1b.py',
    'content': 'def determinar_tipo_triangulo(a, b, c):\n    lados = {a, b, c}\n    if len(lados) == 1:\n        return "Equilátero"\n    elif len(lados) == 2:\n        return "Isósceles"\n    else:\n        return "Escaleno"\nejemplos = [\n    (5, 5, 5),\n    (6, 6, 10),\n    (8, 7, 6)\n]\nfor a, b, c in ejemplos:\n    tipo = determinar_tipo_triangulo(a, b, c)\n    print(f"Triángulo con lados {a}, {b}, {c} es {tipo}")'
}
```
---
### `/addImages`
#### Descripción
Genera imágenes de árboles de sintaxis y las guarda en la carpeta pública del frontend.

#### Método de HTTP
`GET`

#### Parámetros
No recibe parámetros.

#### Respuesta
En caso de una solicitud exitosa, se devuelve un código HTTP 200 (OK). No hay respuesta tipo JSON.
En caso de error, se devuelve un código HTTP 400 (Bad Request).

---

### `/compare`
#### Descripción
Este es el endpoint principal que compara archivos. Recibe un diccionario de diccionarios en el cuerpo de la solicitud, donde cada diccionario representa un archivo con sus atributos.

#### Método de HTTP
`POST`

#### Parámetros
El cuerpo de la solicitud debe ser un diccionario de diccionarios que representen cada archivo y sus atributos.

#### Respuesta
En caso de una solicitud exitosa, se devuelve un código HTTP 200 (OK) junto con un nuevo diccionario que contiene detalles de los archivos comparados. Cada comparación se hace entre todos los archivos en el diccionario de entrada.
En caso de error, se devuelve un código HTTP 400 (Bad Request).

#### Ejemplo de Solicitud
```
{
    1: {
        'id': 1,
        'filename': 'Test1a.py',
        'content': 'triangulos = [\n    (3, 3, 3),\n    (4, 4, 5),\n    (3, 4, 5)\n]\ndef tipo_triangulo(lado1, la...'
    },
    2: {
        'id': 2,
        'filename': 'Test1b.py',
        'content': 'def determinar_tipo_triangulo(a, b, c):\n    lados = {a, b, c}\n    if len(lados) == 1:\n        retu...'
    }
}
```
#### Ejemplo de Repuesta
```
{
    1: {
        'id': 'Test1a.py vs Test1b.py',
        'file_names': ['Test1a.py', 'Test1b.py'],
        'porcentaje': 37.0
    },
    2: {
        'id': 'Test1b.py vs Test1a.py',
        'file_names': ['Test1b.py', 'Test1a.py'],
        'porcentaje': 39.0
    }
}
```
---
### `/highlight`
#### Descripción
Este endpoint compara dos archivos y devuelve un diccionario de diccionarios que indican los índices del código donde se han encontrado similitudes de plagio.

#### Método de HTTP
`POST`

#### Parámetros
El cuerpo de la solicitud debe ser un diccionario de diccionarios que representen cada archivo y sus atributos.

#### Respuesta
En caso de una solicitud exitosa, se devuelve un código HTTP 200 (OK) junto con un diccionario de diccionarios que indican los índices del código donde se han encontrado similitudes de plagio.
En caso de error, se devuelve un código HTTP 400 (Bad Request).

#### Ejemplo de Solicitud
```
{
    1: {
        'id': 1,
        'filename': 'Test1a.py',
        'content': 'triangulos = [\n    (3, 3, 3),\n    (4, 4, 5),\n    (3, 4, 5)\n]\ndef tipo_triangulo(lado1, ...'
    },
    2: {
        'id': 2,
        'filename': 'Test1b.py',
        'content': 'def determinar_tipo_triangulo(a, b, c):\n    lados = {a, b, c}\n    if len(lados) == 1...)'
    }
}
```
#### Ejemplo de Respuesta
```
{
    'Test1a.py': {
        'semantico': {
            'main': {
                'code': 'triangulos = [\n    (3, 3, 3),\n    (4, 4, 5),\n    (3, 4, 5)\n]\n',
                'tokens': [('ident', '1-11', '1'), ('=', '12-13', '1'), ('[', '14-15', '1'), ('(', '5-6', '2'), ('int', '6-7', '2'), (',', '7-8', '2'), ('int', '9-10', '2'), (',', '10-11', '2'), ('int', '12-13', '2'), (')')],
                'characteristics': {
                    'enteros': {'cantidad': 9, 'location': [{'lineNumber': 2, 'indices': [[6, 7], [9, 10], [12, 13]]}, {'lineNumber': 3, 'indices': [[6, 7], [9, 10], [12, 13]]}, {'lineNumber': 4, 'indices': [[6, 7], [9, 10], [12, 13]]}]},
                    'strings': {'cantidad': 0, 'location': []},
                    'floats': {'cantidad': 0, 'location': []},
                    'identifiers': {'cantidad': 1, 'location': [{'lineNumber': 1, 'indices': [[1, 11]]}]},
                    'loops': {'cantidad': 0, 'location': []},
                    'operators': {'cantidad': 1, 'location': [{'lineNumber': 1, 'indices': [[12, 13]]}]},
                    'arguments': {'cantidad': 0, 'location': []}
                }
            },
            'functions': {
                'code': 'def tipo_triangulo(lado1, lado2, lado3):\n    if lado1 == lado2:\n        if lado2 == lado3:\n            return "Equilátero"\n        else:\n            return "Isósceles"\n    elif lado1 == lado3 or lado2 == lado3:\n        return "Isósceles"\n    else:\n        return "Escaleno"\n',
                'tokens': [('def', '1-4', '6'), ('ident', '5-
```

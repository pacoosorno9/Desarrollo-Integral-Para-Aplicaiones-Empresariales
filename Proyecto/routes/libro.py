'''
    ESTE ARCHIVO CONTIENE TODOS LOS ENDPOINTS
'''
#IMPORTACIONES
from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from models import categoria

#CREACION DE LA INSTANCIA
libro_router = ApiRouter()

# CREACION DE LA CLASE CATEGORIA
class Categoria(BaseModel):
    id: int
    nombre: str

# INGRESO DE DATOS, SE GUARDA PERO AL REINICIAR EL SERVIDOR SE BORRAN LOS DATOS
libros = []
categorias = []
libro_id_counter = 0


# CREACION DE LA CLASE LIBROreCON SUS ATRIBUTOS
class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    año: int
    categoria: str
    nDePaginas: int

#FALTA LA CREACION DE UN SCHEMA EXTRA


# ENDPOINT PARA AGREGAR LIBROS
@app.post('/libros/', tags=['libros'])
def agregarLibros(libro: Libro):
    if not any(cat.nombre == libro.categoria for cat in categorias):
        raise HTTPException(status_code=400, detail="La categoría del libro no existe")
    
    # Calculamos el ID del nuevo libro
    nuevo_id = len(libros) + 1
    libro.id = nuevo_id  # Asignamos el nuevo ID al libro
    libros.append(libro)
    return libro

# ENDPOINT PARA MOSTRAR LOS LIBROS
@app.get('/libros', tags=['libros'])
def get_libros():
    if libros:
        return libros
    else:
        raise HTTPException(status_code=404, detail="No hay libros disponibles")


# ENDPOINT PARA BUSCAR POR ID
@app.get('/libros/{id}', tags=['libros'])
def get_libro_id(id: int):
    for libro in libros:
        if libro.id == id:
            return libro
    raise HTTPException(status_code=404, detail=f"No se encontró el libro con ID {id}")


# ENDPOINT PARA BUSCAR POR CATEGORIA
@app.get('/libros/categoria/{categoria}', tags=['libros'])
def get_libros_por_categoria(categoria: str):
    libros_encontrados = [libro for libro in libros if libro.categoria.lower() == categoria.lower()]
    if libros_encontrados:
        return libros_encontrados
    else:
        raise HTTPException(status_code=404, detail=f"No hay libros en la categoría '{categoria}'")


# ENDPOINT PARA MODIFICAR LIBROS POR SU ID
@app.put('/libros/{id}', tags=['libros'])
def update_libro(id: int, nuevo_libro: Libro):
    if not any(cat.nombre == nuevo_libro.categoria for cat in categorias):
        raise HTTPException(status_code=400, detail="La categoría no existe")
    for index, libro in enumerate(libros):
        if libro.id == id:
            libros[index] = nuevo_libro
            return libros
    raise HTTPException(status_code=404, detail=f"No se encontró el libro con ID {id}")


# ENDPOINT PARA QUITAR LIBROS
@app.delete('/libros/{id}', tags=['libros'])
def delete_libros(id: int = Path(..., title="ID del libro")):
    global libros
    libros = [libro for libro in libros if libro.id != id]
    if libros:
        return libros
    else:
        raise HTTPException(status_code=404, detail="No hay libros disponibles")


# ENDPOINT PARA AGREGAR LAS CATEGORIAS
@app.post('/categorias/', tags=['Categorias'])
def agregaCategorias(categoria: Categoria):
    categorias.append(categoria)
    return categoria


# ENDPOINT PARA PODER ACTUALIZAR LAS CATEGORIAS
@app.put('/categorias/{id}', tags=['categorias'])
def update_categoria(id: int, nueva_categoria: Categoria):
    for libro in libros:
        if libro.categoria == categorias[id - 1].nombre:
            libro.categoria = nueva_categoria.nombre
    categorias[id - 1] = nueva_categoria
    return categorias


# ENDPOINT PARA PODER BORRAR LAS CATEGORIAS
@app.delete('/categorias/{id}', tags=['categorias'])
def delete_categoria(id: int):
    if id <= len(categorias):
        for libro in libros:
            if libro.categoria == categorias[id - 1].nombre:
                raise HTTPException(status_code=400, detail="La categoría está asignada a un libro")
        categoria_borrada = categorias.pop(id - 1)
        return categoria_borrada
    else:
        raise HTTPException(status_code=404, detail=f"No se encontró la categoría con ID {id}")
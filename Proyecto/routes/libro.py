'''
    ESTE ARCHIVO CONTIENE TODOS LOS ENDPOINTS
'''
#IMPORTACIONES
from fastapi import Path, Query, Depends, APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from models.categoria import Categoria as CategoriaModel
from models.libro import Libro as LibroModel
from config.database import Session
from typing import Coroutine, Optional, List
from fastapi.encoders import jsonable_encoder





#CREACION DE LA INSTANCIA
libro_router = APIRouter()

# CREACION DE LA CLASE CATEGORIA
class Categoria(BaseModel):
    id: int
    nombreCategoria: str

#Creacion de la clase Libro
class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    año: int
    categoria: str
    nDePaginas: int

#SCHEMA EXTRA DE LIBROS EJEMPLO
class Config:
    schema_extra = {
        "example":{
            "id"
            "titulo": "Harry Potter",
            "autor": "Marco Polo",
            "año": "2000",
            "categoria": "Fantasia",
            "nDePaginas": "522"
        }
    }


###########    SECCION DE LIBROS       #################

# ENDPOINT PARA AGREGAR LIBROS
@libro_router.post('/libros', tags=['libros'], response_model=dict, status_code=201)
def agregarLibros(libro: Libro) -> dict:
    db = Session()
    nuevo_Libro = LibroModel(**libro.dict())
    for categoria in range(len(categoria)):
        if(nuevo_Libro.categoria == categoria.nombreCategoria):
            print("Hola mundo")
    
    db.add(nuevo_Libro)
    db.commit()
    return JSONResponse(content={"message": "Se ha registrado el libro"})

# ENDPOINT PARA OBTENER TODOS LOS LIBROS
@libro_router.get('/libros', tags=['libros'], response_model=list)
def obtenerTodosLosLibros() -> list:
    db = Session()
    libros = db.query(LibroModel).all()
    return libros

# ENDPOINT PARA OBTENER UN LIBRO POR SU ID
@libro_router.get('/libros/{id}', tags=["libros"])
def get_LibroID (id: int):
    db = Session()
    result = db.query(LibroModel).filter(LibroModel.id == id).first()
    if not result:
            return JSONResponse(status_code=404,  content={'message':'No encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@libro_router.put('/libros/{libro_id}', tags=['libros'], response_model=Libro)
def actualizarLibro(libro: Libro, libro_id: int = Path(..., title="The ID of the libro you want to update")) -> Libro:
    db = Session()
    libro_db = db.query(LibroModel).filter(LibroModel.id == libro_id).first()
    if not libro_db:
        raise HTTPException(status_code=404, detail="Libro not found")
    
    for key, value in libro.dict().items():
        setattr(libro_db, key, value)
    
    db.commit()
    db.refresh(libro_db)
    return libro_db

# ENDPOINT PARA ELIMINAR UN LIBRO
@libro_router.delete('/libros/{libro_id}', tags=['libros'], response_model=dict)
def eliminarLibro(libro_id: int = Path(..., title="")) -> dict:
    db = Session()
    libro = db.query(LibroModel).filter(LibroModel.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro not found")
    
    db.delete(libro)
    db.commit()
    return {"message": "Libro deleted successfully"}




# ###########    SECCION DE CATEGORIAS       #################
# # ENDPOINT PARA AGREGAR LAS CATEGORIAS
@libro_router.post('/categorias', tags=['nombreCategoria'], response_model=dict, status_code=201)
def crear_categorias(categoria: Categoria) -> dict:
    db = Session()
    nueva_categoria=CategoriaModel(**categoria.dict())
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return JSONResponse(status_code=201, content={"message": "Categoria Creada"})

# # Endpoint para obtener todas las categorías
@libro_router.get('/categorias', tags=['categorias'], response_model=list)
def obtenerTodosLosCategorias() -> list:
    db = Session()
    categorias = db.query(CategoriaModel).all()
    return jsonable_encoder(categorias)

# Endpoint para obtener una categoría por su ID
@libro_router.get('/categorias/{categoria_id}', tags=["Categorias"])
def get_CategoriaID (id: int):
    db = Session()
    result = db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
    if not result:
            return JSONResponse(status_code=404,  content={'message':'No encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@libro_router.put('/categorias/{id}', tags=['categorias'])
def update_categoria(id: int, categoria: Categoria):
    db=Session()
    result = db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    result.id = categoria.id
    result.nombreCategoria= categoria.nombreCategoria
    db.commit()

    return JSONResponse(status_code=200, content={'message':'Se ha modificado la pelicula'})

#mEndpoint para eliminar una categoría
@libro_router.delete('/categorias/{id}', tags=('categorias'), response_model=dict(), status_code="200")
def delete_categorias (id: int) -> dict:
    db=Session()
    result = db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={'message':'Se ha borrado la categoria'})














# # # ENDPOINT PARA AGREGAR LIBROS
# @libro_router.post('/libros', tags=['libros'], response_model=dict, status_code=201)
# def agregarLibros(libro: Libro) -> dict:
#      db=Session()
#      nuevo_Libro = LibroModel(**libro.dict())
#      #if(nuevo_Libro.categoria)
#      db.add(nuevo_Libro)
#      db.commit()
#      return JSONResponse(content={"message": "Se ha registrado el libro"})





'''
     if (Session.Query())
     if not any(cat.nombre == libro.categoria for cat in categorias):
         raise HTTPException(status_code=400, detail="La categoría del libro no existe")
# Calculamos el ID del nuevo libro
     nuevo_id = len(libros) + 1
     libro.id = nuevo_id  # Asignamos el nuevo ID al libro
     libros.append(libro)
     return libro
'''




'''

# # ENDPOINT PARA AGREGAR LIBROS
# @app.post('/libros/', tags=['libros'])
# def agregarLibros(libro: Libro):
#     if not any(cat.nombre == libro.categoria for cat in categorias):
#         raise HTTPException(status_code=400, detail="La categoría del libro no existe")
    
#     # Calculamos el ID del nuevo libro
#     nuevo_id = len(libros) + 1
#     libro.id = nuevo_id  # Asignamos el nuevo ID al libro
#     libros.append(libro)
#     return libro

# # ENDPOINT PARA MOSTRAR LOS LIBROS
# @app.get('/libros', tags=['libros'])
# def get_libros():
#     if libros:
#         return libros
#     else:
#         raise HTTPException(status_code=404, detail="No hay libros disponibles")


# # ENDPOINT PARA BUSCAR POR ID
# @app.get('/libros/{id}', tags=['libros'])
# def get_libro_id(id: int):
#     for libro in libros:
#         if libro.id == id:
#             return libro
#     raise HTTPException(status_code=404, detail=f"No se encontró el libro con ID {id}")


# # ENDPOINT PARA BUSCAR POR CATEGORIA
# @app.get('/libros/categoria/{categoria}', tags=['libros'])
# def get_libros_por_categoria(categoria: str):
#     libros_encontrados = [libro for libro in libros if libro.categoria.lower() == categoria.lower()]
#     if libros_encontrados:
#         return libros_encontrados
#     else:
#         raise HTTPException(status_code=404, detail=f"No hay libros en la categoría '{categoria}'")


# # ENDPOINT PARA MODIFICAR LIBROS POR SU ID
# @app.put('/libros/{id}', tags=['libros'])
# def update_libro(id: int, nuevo_libro: Libro):
#     if not any(cat.nombre == nuevo_libro.categoria for cat in categorias):
#         raise HTTPException(status_code=400, detail="La categoría no existe")
#     for index, libro in enumerate(libros):
#         if libro.id == id:
#             libros[index] = nuevo_libro
#             return libros
#     raise HTTPException(status_code=404, detail=f"No se encontró el libro con ID {id}")


# # ENDPOINT PARA QUITAR LIBROS
# @app.delete('/libros/{id}', tags=['libros'])
# def delete_libros(id: int = Path(..., title="ID del libro")):
#     global libros
#     libros = [libro for libro in libros if libro.id != id]
#     if libros:
#         return libros
#     else:
#         raise HTTPException(status_code=404, detail="No hay libros disponibles")


# ENDPOINT PARA AGREGAR LAS CATEGORIAS
@libro_router.post('/categorias/', tags=['Categorias'], response_model=dict, status_code=201)
def crear_categorias(categoria: Categoria) -> dict:
    db = Session()
    nueva_categoria=CategoriaModel(**categoria.dict())
    db.add(nueva_categoria)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Categoria Creada"})


# # ENDPOINT PARA PODER ACTUALIZAR LAS CATEGORIAS
@app.put('/categorias/{id}', tags=['categorias'])
def update_categoria(id: int, nueva_categoria: Categoria):
     for libro in libros:
         if libro.categoria == categorias[id - 1].nombre:
             libro.categoria = nueva_categoria.nombre
     categorias[id - 1] = nueva_categoria
     return categorias


# # ENDPOINT PARA PODER BORRAR LAS CATEGORIAS
# @app.delete('/categorias/{id}', tags=['categorias'])
# def delete_categoria(id: int):
#     if id <= len(categorias):
#         for libro in libros:
#             if libro.categoria == categorias[id - 1].nombre:
#                 raise HTTPException(status_code=400, detail="La categoría está asignada a un libro")
#         categoria_borrada = categorias.pop(id - 1)
#         return categoria_borrada
#     else:
#         raise HTTPException(status_code=404, detail=f"No se encontró la categoría con ID {id}")
'''
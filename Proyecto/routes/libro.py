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
@libro_router.post('/libros', tags=['Libros'], response_model=dict, status_code=201)
def agregar_Libros(libro: Libro) -> dict:
    db = Session()
    nuevo_Libro = LibroModel(**libro.dict())
    db.add(nuevo_Libro)
    db.commit()
    return JSONResponse(content={"message": "Se ha registrado el libro"})

# ENDPOINT PARA OBTENER TODOS LOS LIBROS
@libro_router.get('/libros', tags=['Libros'], response_model=list)
def obtener_Todos_Los_Libros() -> list:
    db = Session()
    libros = db.query(LibroModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# ENDPOINT PARA OBTENER UN LIBRO POR SU ID
@libro_router.get('/libros/{id}', tags=["Libros"])
def obetener_Libros_Por_ID (id: int):
    db = Session()
    result = db.query(LibroModel).filter(LibroModel.id == id).first()
    if not result:
            return JSONResponse(status_code=404,  content={'message':'No encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#ENDPONT PARA ACTUALIZAR LOS LIBROS
@libro_router.put('/libros/{libro_id}', tags=['Libros'], response_model=Libro)
def actualizar_Libros(libro: Libro, libro_id: int = Path(..., title="The ID of the libro you want to update")) -> Libro:
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
@libro_router.delete('/libros/{libro_id}', tags=['Libros'], response_model=dict)
def eliminar_Libros(libro_id: int = Path(..., title="")) -> dict:
    db = Session()
    libro = db.query(LibroModel).filter(LibroModel.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro not found")
    
    db.delete(libro)
    db.commit()
    return {"message": "Libro deleted successfully"}




# ###########    SECCION DE CATEGORIAS       #################
# # ENDPOINT PARA AGREGAR LAS CATEGORIAS
@libro_router.post('/categorias', tags=['Categorias'], response_model=dict, status_code=201)
def crear_Categorias(categoria: Categoria) -> dict:
    db = Session()
    nueva_categoria=CategoriaModel(**categoria.dict())
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return JSONResponse(status_code=201, content={"message": "Categoria Creada"})

# # Endpoint para obtener todas las categorías
@libro_router.get('/categorias', tags=['Categorias'], response_model=list)
def obtener_Todos_Los_Categorias() -> list:
    db = Session()
    categorias = db.query(CategoriaModel).all()
    return jsonable_encoder(categorias)

# Endpoint para obtener una categoría por su ID
@libro_router.get('/categorias/{categoria_id}', tags=["Categorias"])
def get_Categoria_Por_ID (id: int):
    db = Session()
    result = db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
    if not result:
            return JSONResponse(status_code=404,  content={'message':'No encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#ENDPOINT PARA ACTUALIZAR LAS CATEGORIAS
@libro_router.put('/categorias/{id}', tags=['Categorias'])
def actualizar_Categoria(id: int, categoria: Categoria):
    db=Session()
    result = db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    result.id = categoria.id
    result.nombreCategoria= categoria.nombreCategoria
    db.commit()

    return JSONResponse(status_code=200, content={'message':'Se ha modificado la pelicula'})

#Endpoint para eliminar una categoría
@libro_router.delete('/categorias/{id}', tags=['Categorias'], response_model=dict(), status_code="200")
def eliminar_Categorias (id: int) -> dict:
    db=Session()
    result = db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'No encontrado'})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={'message':'Se ha borrado la categoria'})
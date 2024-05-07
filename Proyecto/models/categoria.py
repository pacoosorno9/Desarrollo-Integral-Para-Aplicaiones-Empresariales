'''
    ESTE ARCHIVO ES PARA LA CREACION DE LA BASE DE DATOS DE LAS CATEGORTIAS
'''
#IMPORTACIONES
from config.database import Base
from sqlalchemy import Column, Integer, String, Float

#CREACION DE LA TABLA CATEGORIA CON SUS ATRIBUTOS
class Categoria (Base):
    __tablename__ = 'Categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
'''
ESTE ARCHIVO ES PARA LA CREACION DE LA BASE DE DATOS DE LOS LIBROS  
'''
#IMPORTACIONES
from config.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey

#CREACION DE LA TABLA LIBRO CON SUS ATRIBUTOS
class Libro(Base):

    __tablename__ = 'libros'

    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    autor = Column(String)
    año = Column(Integer)
    categoria = Column(String, ForeignKey('Categorias.nombreCategoria'))
    nDePaginas = Column(Integer)
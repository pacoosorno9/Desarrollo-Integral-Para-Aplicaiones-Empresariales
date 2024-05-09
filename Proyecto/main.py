# IMPORTACION DE LIBRERIAS
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from routes.libro import libro_router

# # CREACION DE LA INSTANCIA
app = FastAPI()

# TITULO DE LA APP
app.title = "Proyecto Primer Parcial"

# #INCLUIR LOS DEMAS ARCHIVOS
app.include_router(libro_router)

Base.metadata.create_all(bind=engine)

# ENDPOINT DE PRUEBA
@app.get('/', tags=['Inicio'])
def mensaje():
    return HTMLResponse('<h1>Hola Mundo</h1>')

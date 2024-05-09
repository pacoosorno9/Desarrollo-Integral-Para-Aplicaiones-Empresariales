'''
    ESTE ARCHIVO ES PARA CONFIGURAR LA BASE DE DATOS, SE CONFIGURA EL MOTOR A UTILIZAR, PARA QUE PUEDA FUNCIONAR SE DEBE DE INSTALAR SQLALCHEMY EN EL PROYECTO.
'''
#IMPORTACIONES
import os 
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import declarative_base

sqlite_file_name = '../database.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"
engine = create_engine(database_url, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
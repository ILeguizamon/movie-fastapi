#Conexion a la base de datos

import os #Permite utilizar funciones para interactuar con nuestro sistema operativo
from sqlalchemy import create_engine #crea conexiones con las bases de datos
from sqlalchemy.orm.session import sessionmaker #utiliza clases declarativas
from sqlalchemy.ext.declarative import declarative_base 

sqliteName = 'movies.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))
databaseUrl = f"sqlite:///{os.path.join(base_dir, sqliteName)}"

engine = create_engine(databaseUrl, echo = True)

Session = sessionmaker(bind = engine)


Base = declarative_base()

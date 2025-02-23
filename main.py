#Se usa para ejecutar una aplicación web en FastAPI utilizando Uvicorn como servidor ASGI. 
#IMPORTANTE, Para ejecutar el servidor, se usa: venv\Scripts\activate  # Windows & luego, uvicorn main:app --reload 

#uvicorn: Es el servidor ASGI (Asynchronous Server Gateway Interface) que ejecuta aplicaciones web escritas con frameworks como FastAPI o Starlette.

#main:app: Aquí se le indica a Uvicorn qué archivo y objeto ejecutar.
    #main: Es el nombre del archivo Python donde se encuentra la aplicación FastAPI (por ejemplo, main.py). 
    #app: Es el nombre del objeto FastAPI dentro de ese archivo. En tu caso, en el archivo main.py, deberías tener algo como app = FastAPI().  

# --reload: Este parámetro le dice a Uvicorn que recargue automáticamente la aplicación cada vez que detecte cambios en el código.
# --port 4000: Especifica el puerto en el que el servidor debe escuchar las peticiones.

'''
¿Cuál es el propósito principal de FastAPI?
- FastAPI está diseñado específicamente para facilitar y acelerar la creación de APIs en Python, aprovechando la sintaxis de tipo de Python para una mayor seguridad y eficiencia.

¿Cómo se define un modelo Pydantic en FastAPI para especificar la estructura de los datos?
-En FastAPI, los modelos Pydantic se definen creando una clase que hereda de BaseModel y especificando los campos y sus tipos.

¿Qué función desempeña el tema principal de la seccion? - AUTENTICACIÓN
-Generar Tokens

API:
-Una API es un intermediario que facilita la comunicación entre aplicaciones o servicios. No es una aplicación por sí misma, sino una herramienta que las aplicaciones usan para interactuar con otras aplicaciones o sistemas.
'''


from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from bd.database import engine, Base
from routers.movie import routerMovie #Importo el objeto de mi movie.py de mi carpeta routers.
from routers.users import login_user 
import os

app = FastAPI( #Es el nombre del objeto FastAPI.
        title = 'Aprendiendo FastApi',
        description = 'Una api en los primeros pasos',
        version = '0.0.1'
        )

#rutas (Movie & User)
app.include_router(routerMovie)
app.include_router(login_user)

Base.metadata.create_all(bind = engine)

@app.get('/', tags = ['Inicio']) 
def read_root():
    return HTMLResponse('<h2> Hola mundo!</h2>')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host = "0.0.0", port = port)








'''
Pydantic:
-Biblioteca de python en conjunto con FastAPI para la validación de datos, validaciones automaticas (basadas en definiciones de modelos), conversión de tipos.
'''

'''
METODOS HTTP (protocolo que define un conjunto de metodos de peticiones que indica la accion que se desea realizar para un recurso determinado del servidor)

POST: crear un recurso nuevo.
PUT: modificar un recurso existente.
GET: consultar información de un recurso.
DELETE: eliminar un recurso.

Todo esto se lo conoce como CRUD:
C = Create
R = Read
U = Update
D = Delete


El 200 OK es un código de estado HTTP que indica que la solicitud fue procesada con éxito.
'''

'''
def get_movies_by_category(category: str):
    filtered_movies = [movie for movie in movies if movie['category'].lower() == category.lower()]
    return filtered_movies

'''
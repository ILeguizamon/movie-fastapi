#Rutas que tengan que ver solamente con movies.

from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.security import HTTPBearer
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

routerMovie = APIRouter()


#Protege rutas
#la clase BearerJWT sirve para proteger rutas en FastAPI con autenticación basada en tokens JWT
class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)  # Obtiene el token de la cabecera "Authorization"
        data = validateToken(auth.credentials)  # Valida el token con la función validateToken()
        if data['email'] != 'ivanleguizamonx1@gmail.com':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')


#Clase de python que hereda de BaseModel y esto me va a servir para poder realizar la validación correspondiente.
#Validar datos
class Movie(BaseModel):
    id: Optional[int] = None #El campo id puede ser un número entero o puede no estar presente (None). el campo id puede ser un número entero o puede no estar presente (None)
    title: str    = Field(default = 'Titulo de la pelicula', min_length = 5, max_length = 60) # es una declaración en Pydantic, que se usa en FastAPI para validar datos en modelos.
    overview: str = Field(default = 'Descripción de la pelicula', min_length = 15, max_length = 60)
    year: int     = Field(default = '2023')
    rating: float = Field(ge = 1, le = 10) # validación de Pydantic: -ge (greater or equal) = 1 → No puede ser menor que 1.
    category: str = Field(min_length = 3, max_length = 100, default = 'Aquí va la categoría')

#TIP: con CTRL + D, selecciono lo que quiero eliminar y cambiar todas a la vez.

#Agrupo los endpoint en un solo tag de Movies
#WTF dependencies = [Depends(BearerJWT())] -  Protege el endpoint con un middleware de autenticación JWT, es decir, solo los usuarios con un token JWT válido podrán acceder
#Consultas a la bd, devolviendo todos los registros.
@routerMovie.get('/movies', tags = ['Movies'], dependencies = [Depends(BearerJWT())]) #Creación de endpoint que estara disponible en la ruta /movies, que al acceder a él, devovlera la lista de peliculas que hayas definido en la variable movies.
def get_movies(): # Define la función que maneja la solicitud GET. Cuando se hace una petición GET a la ruta /movies
    db = Session()
    data = db.quey(ModelMovie).all() #queremos todos los registros de peliculas en la bd.
    return JSONResponse(content= jsonable_encoder(data))



#Parámetros de Ruta
#Validaciones de prámetros
#Codigos de estado
#Consultas a la bd, filtrando por id.
@routerMovie.get('/movies/{id}', tags = ['Movies'], status_code = 200) #creo una nueva ruta para que el usuario busque la pelicula por ID.
def get_movie(id: int = Path(ge = 1, le = 100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first() # Consulta a la bd, y que me devuelva el primer resultado.
    if not data:
        return JSONResponse(status_code = 404, content = {'message':'Recurso no encontrado'})
    return JSONResponse(status_code = 200, content = jsonable_encoder(data))


#Parámetros de Queary - FastAPI detecta que si no le paso un parámetro, esta busqueda en una busqueda por query.
#Validación para Querys.
#Buscar por category en la bd.
@routerMovie.get('/movies/', tags = ['Movies'])
def get_movies_by_category(category: str = Query(min_length = 3, max_length = 100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    return JSONResponse(status_code = 200, content = jsonable_encoder(data))


#JSONResponse: Se utiliza para devolver respuestas con datos en formato JSON
# - content: Especifica el contenido de la respuesta. En este caso, estamos enviando un mensaje en formato JSON con una clave message.



#Metodo POST - Creación de nuevas peliculas.
#Respuestas (JSONResponse)
#Codigos de estado
@routerMovie.post('/movies/', tags = ['Movies'], status_code = 201)
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.dict()) #Pasamos todos los parametros y lo convertimos en un diccionario.
    db.add(newMovie)
    db.commit()
    return JSONResponse(status_code = 201, content = {'message': 'se ha cargado una nueva pelicula', 'movie': [movie.dict() for m in movie]})




#Metodo PUT 
#Validaciones de prámetros
#Respuestas (JSONResponse)
#Codigos de estado
#Actualizar registros en la bd.
@routerMovie.put('/movies/{id}', tags = ['Movies'], status_code = 200)
def update_movie(id: int, movie: Movie):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code = 404, content = {'message':'No se encontro el recurso'})
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()
    return JSONResponse(content = {'message': 'Se ha modificado la pelicula'})




#Metodo DELETE
#Busca de mi lista la que coincida con la ID a eliminar.
#Respuestas (JSONResponse)
#Codigos de estado
#Eliminar registros de mi bd.
@routerMovie.delete('/movies/{id}', tags = ['Movies'], status_code = 200)
def delete_movie(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code = 404, content = {'message':'No se encontro el recurso'})
    db.delete(data)
    db.commit()
    return JSONResponse(content = {'message': 'Se ha eliminado una pelicula', 'pelicula eliminada': jsonable_encoder(data)})
        
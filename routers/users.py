from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from routers.movie import routerMovie 
from user_jwt import createToken, validateToken

login_user = APIRouter()

class User(BaseModel):
    email: str
    password: str


@login_user.post('/login', tags = ['authentication'])
def login(user: User):
    if user.email == 'ivanleguizamonx1@gmail.com' and user.password == '123':
        token: str = createToken(user.dict())
        print(token)
        return JSONResponse(content = token)
import jwt
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def createToken(data: dict):
    token: str = jwt.encode(payload=data, key=SECRET_KEY, algorithm='HS256')
    return token

def validateToken(token: str) -> dict:
    data: dict = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
    return data

from pydantic import BaseModel

class AdminLogin(BaseModel):
    login: str
    password: str
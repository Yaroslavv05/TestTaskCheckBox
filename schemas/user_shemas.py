from pydantic import BaseModel
 
class Token(BaseModel):
    access_token: str
    token_type: str
    
class CreateUser(BaseModel):
    name: str
    username: str
    password: str
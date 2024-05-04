from pydantic import BaseModel

'''
Token: Pydantic model for representing an access token, including the access token itself and its type.

CreateUser: Pydantic model for validating data required to create a user, including name, username, and password.
'''

class Token(BaseModel):
    access_token: str
    token_type: str
    
class CreateUser(BaseModel):
    name: str
    username: str
    password: str
from pydantic import BaseModel,EmailStr

class UserSchema(BaseModel):
    fullname: str
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Rey Shazni",
                "username": "ruymisterio",
                "password": "weakpassword"
            }
        }

class UserLoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "ruymisterio",
                "password": "weakpassword"
            }
        }
        
users = []
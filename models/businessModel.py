from pydantic import BaseModel

class Bussiness(BaseModel):
    bussiness_name:str
    bussiness_descr:str
    bussiness_address:str
    bussiness_contact:str
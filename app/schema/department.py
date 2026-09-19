from pydantic import BaseModel , ConfigDict 
class DepartmentCreate(BaseModel):
    name:str
    
class DepartmentShow(BaseModel):
    id:int
    name:str
    
    model_config=ConfigDict(from_attributes=True)
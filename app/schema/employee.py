from pydantic import BaseModel , EmailStr , ConfigDict
class EmployeeCreate(BaseModel):
    name :str
    email:EmailStr
    department_id:int
    
class EmployeeREad(BaseModel):
    id:int
    name:str
    email:EmailStr
    department_id:int
    
    model_config=ConfigDict(from_attributes=True)
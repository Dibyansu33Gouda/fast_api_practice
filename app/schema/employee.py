from pydantic import BaseModel , EmailStr , ConfigDict
from .department import DepartmentShow

class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department_id: int

class EmployeeREad(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: DepartmentShow

    model_config = ConfigDict(from_attributes=True)
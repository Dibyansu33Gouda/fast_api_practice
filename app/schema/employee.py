from pydantic import BaseModel , EmailStr , ConfigDict , Field
from .department import DepartmentShow

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1 , max_length=100)
    email: EmailStr
    department_id: int

class EmployeeREad(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: DepartmentShow

    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel , EmailStr , ConfigDict , Field
from .department import DepartmentShow

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1 , max_length=100)
    email: EmailStr
    department_id: int
    phone_number : str | None=None

class EmployeeREad(BaseModel):
    id: int
    name: str
    email: EmailStr
    Phone_number : str | None=None
    department: DepartmentShow

    model_config = ConfigDict(from_attributes=True)
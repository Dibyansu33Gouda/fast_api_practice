from fastapi import FastAPI , HTTPException , Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

from app.db.session import get_session
from app.models.employee import Employee
from app.schema.employee import EmployeeCreate , EmployeeREad
from app.models.departments import Department


router = APIRouter(prefix="/employees" , tags=["employees"])

@router.post("/",response_model=EmployeeREad , status_code=201)
async  def create_employee(payload:EmployeeCreate , session:AsyncSession = Depends(get_session)):
    department= await session.get(Department , payload.department_id)
    if department is None:
        raise HTTPException(status_code=404 , detail="Department not found")
    emplyee=Employee(name=payload.name , email=payload.email , department_id=payload.department_id)
    session.add(emplyee)
    await session.commit()
    await session.refresh(emplyee)
    return emplyee

@router.get("/",response_model=list[EmployeeREad])
def list_employee(session:AsyncSession = Depends(get_session)):
    result= await session.execute(Select(Employee))
    return result.scalars().all()

@router.get()
    
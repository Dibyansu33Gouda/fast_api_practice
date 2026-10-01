from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.dependencies import get_department_or_404, get_employee_or_404
from app.db.session import get_session
from app.models.employee import Employee
from app.schema.employee import EmployeeCreate , EmployeeREad


router = APIRouter(prefix="/employees" , tags=["employees"])

@router.post("/",response_model=EmployeeREad , status_code=201)
async  def create_employee(payload:EmployeeCreate , session:AsyncSession = Depends(get_session)):
    await get_department_or_404(payload.department_id, session)
    emplyee=Employee(**payload.model_dump())
    session.add(emplyee)
    await session.commit()
    await session.refresh(emplyee,attribute_names=['department'])
    return emplyee

@router.get("/",response_model=list[EmployeeREad])
async def list_employee(session:AsyncSession = Depends(get_session)):
    result=await session.execute(
        select(Employee).options(selectinload(Employee.department))
    )
    employees=result.scalars().all()
    return employees

@router.get("/{employee_id}",response_model=EmployeeREad)
async def get_employee(employee: Employee = Depends(get_employee_or_404)):
    return employee
   
@router.put("/{employee_id}",response_model=EmployeeREad) 
async def update_employee(payload:EmployeeCreate , 
                    session: AsyncSession = Depends(get_session),
                    employee: Employee = Depends(get_employee_or_404)
                    ):
                        employee.name=payload.name
                        employee.email=payload.email
                        employee.department = await get_department_or_404(payload.department_id, session)

                        await session.commit()
                        return employee
@router.delete("/{employee_id}", status_code=204)
async def delete_employee(employee: Employee = Depends(get_employee_or_404), session:AsyncSession = Depends(get_session)):
    await session.delete(employee)
    await session.commit()                   

    
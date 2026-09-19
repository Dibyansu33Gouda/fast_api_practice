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
async def list_employee(session:AsyncSession = Depends(get_session)):
    result= await session.execute(Select(Employee))
    return result.scalars().all()
    return result.scalars().all()

@router.get("/{employee_id}",response_model=EmployeeREad)
async def get_employee(employee_id:int , session: AsyncSession = Depends(get_session)):
    employee = await session.get(Employee , employee_id)
    if employee is None:
        raise HTTPException(status_code=404 , detail="employee doesn't exist")
        
    return employee
   
@router.put("/{employee_id}",response_model=EmployeeREad) 
async def update_employee(employee_id:int , 
                    payload:EmployeeCreate , 
                    session: AsyncSession = Depends(get_session)
                    ):
                        employee=await session.get(Employee , employee_id)
                        if employee is None:
                            raise HTTPException(status_code=404 , detail="employee not found ")
                        
                        department=await session.get(Department , payload.department_id)
                        if department is None:
                            raise HTTPException(status_code=404 , detail="department not found")
                        employee.name=payload.name
                        employee.email=payload.email
                        employee.department_id=payload.department_id                            

                        await session.commit()
                        await session.refresh(employee)
                        return employee
@router.delete("/{employee_id}", status_code=204)
async def delete_employee(employee_id: int, session: AsyncSession = Depends(get_session)):
    employee = await session.get(Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    await session.delete(employee)
    await session.commit()                   

    
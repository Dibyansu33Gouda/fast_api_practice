from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import Select



from app.db.session import get_session
from app.models.departments import Department
from app.models.employee import Employee


async def get_department_or_404(department_id : int , session : AsyncSession = Depends(get_session)) -> Department:
    department=await session.get(Department , department_id)
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Department not found")
    return department
    
    
async def get_employee_or_404(employee_id:int , session: AsyncSession = Depends(get_session))->Employee:
    result = await session.execute(
            Select(Employee)
            .where(Employee.id == employee_id)
            .options(selectinload(Employee.department))
        )
    employee = result.scalars().first()
    if employee is None:
        raise HTTPException(status_code=404, detail="employee doesn't exist")
    
    return employee
    
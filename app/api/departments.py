from fastapi import FastAPI , APIRouter , Depends , HTTPException , status  
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select 
from app.db.session import get_session
from app.models.departments import Department
from app.schema.department import DepartmentCreate , DepartmentShow

router= APIRouter(prefix="/departments" , tags=["departments"])

@router.post("/" , response_model=DepartmentShow , status_code=201)

async def   create_department(payload:DepartmentCreate ,session:AsyncSession = Depends(get_session)):
   department=Department(name=payload.name)
   session.add(department)
   
   await session.commit()
   await session.refresh(department)
   
   return department

@router.get("/",response_model=list[DepartmentShow])
async def list_Department(session:AsyncSession = Depends(get_session)):
   result=await session.execute(select(Department))
   return result.scalars().all()


@router.get("/{department_id}",response_model=DepartmentShow)
async def get_department(department_id:int , session:AsyncSession = Depends(get_session)):
   department=await session.get(Department , department_id)
   if not department:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Department not found")
   return department

@router.put("/{department_id}" , response_model=DepartmentShow)
async def update_department(department_id:int , 
                            payload:DepartmentCreate,
                            session:AsyncSession = Depends(get_session)):
   department=await session.get(Department , department_id)
   if department is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Department not found")
   department.name = payload.name
   await session.commit()
   await session.refresh(department)
   return department

@router.delete("/{department_id}" , status_code=204)
async def delete_Department(department_id:int ,
                            session:AsyncSession = Depends(get_session)
                            
                        ):
   department=await session.get(Department,department_id)
   if department is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
   await session.delete(department)
   await session.commit()

